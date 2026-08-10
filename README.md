# Google Comment Responder

Mirrored Codex interface on Google Suite products using comment threads.

## What it includes

- A Codex plugin manifest at `plugins/google-comment-responder/.codex-plugin/plugin.json`
- A reusable skill at `plugins/google-comment-responder/skills/google-comment-responder/SKILL.md`
- A repo marketplace at `.agents/plugins/marketplace.json`

## Install from the public marketplace

Open the public listing and choose **Install plugin**:

https://chatgpt.com/plugins/plugins_6a735aa8168481918043403ac8a1e18f

This is the recommended path for ChatGPT/Codex app users. It installs the currently published public version from the Plugins Directory.

## Manual install from GitHub

Add this repository as a Codex plugin marketplace, then install the plugin in Codex CLI:

```bash
codex plugin marketplace add katnissali/google-comment-responder --ref main
codex plugin add google-comment-responder@google-comment-responder
```

## Update a manual GitHub install

```bash
codex plugin marketplace upgrade google-comment-responder
codex plugin add google-comment-responder@google-comment-responder
```

Start a new Codex CLI task after installing so the skill is available.

## Desktop app

Use the public marketplace link above for the desktop app. The manual GitHub commands are mainly for Codex CLI testing or development installs.

## Git push automation

Pushing to `main` runs `.github/workflows/plugin-package.yml`. The workflow validates the plugin source, checks that the plugin does not contain configured forbidden text, builds a ZIP with unique build metadata, uploads it as a GitHub Actions artifact, and creates or updates a GitHub issue with the manual OpenAI Platform publishing checklist.

The OpenAI public Plugins Directory does not update directly from this repository. Public updates still go through the OpenAI Platform submission portal: upload the ZIP artifact, review the draft, complete policy attestations, submit for review, and publish the approved version from the portal.

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
