#!/usr/bin/env python3
"""Fetch a Jira Cloud ticket and output its details as structured JSON.

Required environment variables:
  JIRA_URL    - Your Jira Cloud instance URL (e.g. https://mycompany.atlassian.net)
  JIRA_EMAIL  - The email associated with your Jira account
  JIRA_TOKEN  - An API token generated from https://id.atlassian.com/manage-profile/security/api-tokens

Usage:
  python fetch_jira_ticket.py PA-3467
"""

import json
import os
import sys
import urllib.request
import urllib.error
import base64


def get_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        print(f"Error: {name} environment variable is not set.", file=sys.stderr)
        print(f"Set it with: export {name}=<value>", file=sys.stderr)
        sys.exit(1)
    return value


def fetch_ticket(ticket_key: str) -> dict:
    jira_url = get_env("JIRA_URL").rstrip("/")
    email = get_env("JIRA_EMAIL")
    token = get_env("JIRA_TOKEN")

    # Build auth header
    credentials = base64.b64encode(f"{email}:{token}".encode()).decode()
    headers = {
        "Authorization": f"Basic {credentials}",
        "Accept": "application/json",
    }

    # Fetch the issue with relevant fields
    fields = "summary,description,comment,subtasks,issuelinks,labels,status,issuetype,priority"
    url = f"{jira_url}/rest/api/3/issue/{ticket_key}?fields={fields}&expand=renderedFields"

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Error: Ticket {ticket_key} not found.", file=sys.stderr)
        elif e.code == 401:
            print("Error: Authentication failed. Check JIRA_EMAIL and JIRA_TOKEN.", file=sys.stderr)
        elif e.code == 403:
            print("Error: Access denied. Your token may lack permissions for this project.", file=sys.stderr)
        else:
            print(f"Error: HTTP {e.code} — {e.reason}", file=sys.stderr)
        sys.exit(1)

    fields_data = data.get("fields", {})
    rendered = data.get("renderedFields", {})

    # Extract description text from Atlassian Document Format
    description = _extract_adf_text(fields_data.get("description"))
    rendered_description = rendered.get("description", "")

    # Extract comments
    comments = []
    comment_data = fields_data.get("comment", {})
    for c in comment_data.get("comments", []):
        comments.append({
            "author": c.get("author", {}).get("displayName", "Unknown"),
            "body": _extract_adf_text(c.get("body")),
            "created": c.get("created", ""),
        })

    # Extract subtasks
    subtasks = []
    for st in fields_data.get("subtasks", []):
        subtasks.append({
            "key": st.get("key", ""),
            "summary": st.get("fields", {}).get("summary", ""),
            "status": st.get("fields", {}).get("status", {}).get("name", ""),
        })

    # Extract linked issues
    links = []
    for link in fields_data.get("issuelinks", []):
        link_type = link.get("type", {}).get("name", "")
        if "outwardIssue" in link:
            linked = link["outwardIssue"]
            direction = link.get("type", {}).get("outward", "relates to")
        elif "inwardIssue" in link:
            linked = link["inwardIssue"]
            direction = link.get("type", {}).get("inward", "relates to")
        else:
            continue
        links.append({
            "key": linked.get("key", ""),
            "summary": linked.get("fields", {}).get("summary", ""),
            "relationship": direction,
            "status": linked.get("fields", {}).get("status", {}).get("name", ""),
        })

    result = {
        "key": data.get("key", ticket_key),
        "summary": fields_data.get("summary", ""),
        "status": fields_data.get("status", {}).get("name", ""),
        "type": fields_data.get("issuetype", {}).get("name", ""),
        "priority": fields_data.get("priority", {}).get("name", ""),
        "labels": fields_data.get("labels", []),
        "description": description,
        "rendered_description": rendered_description,
        "comments": comments,
        "subtasks": subtasks,
        "linked_issues": links,
    }

    return result


def _extract_adf_text(adf_node) -> str:
    """Recursively extract plain text from Atlassian Document Format."""
    if adf_node is None:
        return ""
    if isinstance(adf_node, str):
        return adf_node
    if isinstance(adf_node, dict):
        if adf_node.get("type") == "text":
            return adf_node.get("text", "")
        parts = []
        for child in adf_node.get("content", []):
            parts.append(_extract_adf_text(child))
        return "\n".join(filter(None, parts))
    return ""


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <TICKET-KEY>", file=sys.stderr)
        print(f"Example: {sys.argv[0]} PA-3467", file=sys.stderr)
        sys.exit(1)

    ticket = fetch_ticket(sys.argv[1])
    print(json.dumps(ticket, indent=2))
