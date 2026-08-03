# Google Comment Responder

Mirrored Codex interface on Google Suite products using comment threads.

## What it includes

- A Codex plugin manifest at `plugins/google-comment-responder/.codex-plugin/plugin.json`
- A reusable skill at `plugins/google-comment-responder/skills/google-comment-responder/SKILL.md`
- A repo marketplace at `.agents/plugins/marketplace.json`

## Install in Codex CLI

Add this repository as a Codex plugin marketplace, then install the plugin in Codex CLI:

```bash
codex plugin marketplace add katnissali/google-comment-responder --ref main
codex plugin add google-comment-responder@google-comment-responder
```

## Update

```bash
codex plugin marketplace upgrade google-comment-responder
codex plugin add google-comment-responder@google-comment-responder
```

Start a new Codex CLI task after installing so the skill is available.

## Desktop app

The GitHub marketplace commands above install the plugin for Codex CLI. They may not install the plugin into the ChatGPT/Codex desktop app. For the desktop app, use a workspace share link from an already-installed copy, or install from the official Plugins Directory after the plugin is submitted and approved.

## Uninstall from Codex CLI

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
