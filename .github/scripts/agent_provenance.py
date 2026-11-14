#!/usr/bin/env python3
"""Apply self-declared AI provenance labels from PR and review body markers.

This runs only trusted code from agentic-template. The event payload is data;
no pull-request checkout or shell evaluation is involved.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen


LABELS = {
    "authored-with:claude-code": ("8B5CF6", "PR prepared with Claude Code"),
    "authored-with:codex": ("0E8A16", "PR prepared with Codex"),
    "reviewed-with:claude-code": ("6F42C1", "PR reviewed with Claude Code"),
    "reviewed-with:codex": ("1D76DB", "PR reviewed with Codex"),
}
AGENTS = {"Claude Code": "claude-code", "Codex": "codex"}


def labels_for_event(event_name: str, event: dict) -> tuple[int, list[str]]:
    """Return PR number and labels requested by exact, standalone body lines."""
    if event_name == "pull_request":
        number = event["pull_request"]["number"]
        body = event["pull_request"].get("body") or ""
        prefix, label_prefix = "AI-Authored-With: ", "authored-with:"
    elif event_name == "pull_request_review":
        number = event["pull_request"]["number"]
        body = event["review"].get("body") or ""
        prefix, label_prefix = "AI-Reviewed-With: ", "reviewed-with:"
    else:
        raise ValueError(f"unsupported event: {event_name}")

    labels = []
    for line in body.splitlines():
        if line.startswith(prefix):
            agent = line.removeprefix(prefix)
            if agent in AGENTS:
                label = label_prefix + AGENTS[agent]
                if label not in labels:
                    labels.append(label)
    return number, labels


def request(method: str, path: str, token: str, payload: dict | None = None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = Request(
        "https://api.github.com" + path,
        data=data,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urlopen(req, timeout=20) as response:
        return json.load(response)


def ensure_label(repo: str, name: str, token: str):
    path = f"/repos/{repo}/labels/{quote(name, safe='')}"
    try:
        request("GET", path, token)
        return
    except HTTPError as error:
        if error.code != 404:
            raise
    color, description = LABELS[name]
    try:
        request(
            "POST", f"/repos/{repo}/labels", token,
            {"name": name, "color": color, "description": description},
        )
    except HTTPError as error:
        if error.code != 422:  # Another run may have created it concurrently.
            raise


def main():
    event_name = os.environ["GITHUB_EVENT_NAME"]
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
    number, labels = labels_for_event(event_name, event)
    if not labels:
        print("No AI provenance marker; leaving labels unchanged.")
        return
    repo = os.environ["GITHUB_REPOSITORY"]
    token = os.environ["GH_TOKEN"]
    for label in labels:
        ensure_label(repo, label, token)
    request("POST", f"/repos/{repo}/issues/{number}/labels", token, {"labels": labels})
    print(f"PR #{number}: added {', '.join(labels)}")


if __name__ == "__main__":
    main()
