# Comment Responder Template

Reusable Codex plugin for safely replying to existing Google Drive comment threads.

The plugin is intentionally generic. It does not include private document IDs, company-specific links, credentials, or built-in project assumptions.

## What it includes

- A Codex plugin manifest at `plugins/comment-responder-template/.codex-plugin/plugin.json`
- A reusable skill at `plugins/comment-responder-template/skills/comment-responder-template/SKILL.md`
- A repo marketplace at `.agents/plugins/marketplace.json`

## Install

In the ChatGPT desktop app, open Plugins and install Comment Responder Template from the marketplace.

Start a new Codex task after installing so the skill is available.

## Updating

When changing the plugin:

1. Edit the files under `plugins/comment-responder-template/`.
2. Bump the `version` in `plugins/comment-responder-template/.codex-plugin/plugin.json`.
3. Commit and push the change.

Users should update the plugin from the marketplace when a new version is available, then start a new Codex task.

## Requirements

Users need their own Google Drive access/tools for the plugin to read or reply to comments. The plugin does not grant access to documents by itself.
