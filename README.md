# Google Comment Responder


## Requirements
- Google Drive access/tools to read or reply to comments.
- Access to relevant context to answer comments.

## Codex/ChatGPT App Installation

Open the public listing and choose **Install plugin**:

https://chatgpt.com/plugins/plugins_6a735aa8168481918043403ac8a1e18f

This is the supported install path for ChatGPT and Codex app users. It installs the currently published public version from the OpenAI Plugins Directory. Installation via the OpenAI Plugins Directory does not require manual updating. Manage or uninstall the plugin from the Plugins tab.


## Manual GitHub Installation

Use if the public marketplace install via CLI is unavailable, buggy, or not installing correctly. Add this GitHub repository as a Codex plugin marketplace, then install the plugin:

```bash
codex plugin marketplace add katnissali/google-comment-responder --ref main
codex plugin add google-comment-responder@google-comment-responder
```

Requires **manual updates**.

## Updates

Installation via public marketplace does not need manual updates.

```bash
codex plugin marketplace upgrade google-comment-responder
codex plugin add google-comment-responder@google-comment-responder
```

## Uninstall

If installed manually via GitHub, uninstall with:

```bash
codex plugin remove google-comment-responder
codex plugin marketplace remove google-comment-responder
```
