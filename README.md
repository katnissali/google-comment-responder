# Comment Responder Template

Mirrored Codex interface on Google suite products using comment threads.

## What it includes

- A Codex plugin manifest at `plugins/comment-responder-template/.codex-plugin/plugin.json`
- A reusable skill at `plugins/comment-responder-template/skills/comment-responder-template/SKILL.md`
- A repo marketplace at `.agents/plugins/marketplace.json`

## Install

Add this repository as a Codex plugin marketplace, then install the plugin:

```bash
codex plugin marketplace add katnissali/comment-responder-template --ref main
codex plugin add comment-responder-template@comment-responder-template
```

Start a new Codex task after installing so the skill is available.

## Uninstall

Remove the installed plugin:

```bash
codex plugin remove comment-responder-template@comment-responder-template
```

If you also want to remove the marketplace source:

```bash
codex plugin marketplace remove comment-responder-template
```

## Requirements

Users need Google Drive access/tools for the plugin to read or reply to comments. The plugin does not grant access to documents by itself.
