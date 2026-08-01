# Google Comment Responder

Mirrored Codex interface on Google Suite products using comment threads.

## What it includes

- A Codex plugin manifest at `plugins/google-comment-responder/.codex-plugin/plugin.json`
- A reusable skill at `plugins/google-comment-responder/skills/google-comment-responder/SKILL.md`
- A repo marketplace at `.agents/plugins/marketplace.json`

## Install

Add this repository as a Codex plugin marketplace, then install the plugin:

```bash
codex plugin marketplace add katnissali/google-comment-responder --ref main
codex plugin add google-comment-responder@google-comment-responder
```

Start a new Codex task after installing so the skill is available.

## Uninstall

Remove the installed plugin:

```bash
codex plugin remove google-comment-responder@google-comment-responder
```

If you also want to remove the marketplace source:

```bash
codex plugin marketplace remove google-comment-responder
```

## Requirements

Users need Google Drive access/tools for the plugin to read or reply to comments. The plugin does not grant access to documents by itself.
