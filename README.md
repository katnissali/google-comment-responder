# Google Comment Responder


Use Codex/ChatGPT from within the Google Suite. Codex will respond to all comments starting with "AGENT:" using all context available from the original environment. Codex can continue threads by responding to responses.

**WARNING:** Codex comments appear as if they come from you. However, responses always begin with `CODEX:`.

Trigger with:
`@Google Comment Responder Respond <link>.`

## Requirements
- Google Drive access/tools to read or reply to comments.
- Access to relevant context to answer comments.

## Codex/ChatGPT App Installation

Open the public listing and choose **Install plugin**:

https://chatgpt.com/plugins/plugins_6a735aa8168481918043403ac8a1e18f

This is the supported install path for ChatGPT and Codex app users. It installs the currently published public version from the OpenAI Plugins Directory. Installation via the OpenAI Plugins Directory does not require manual updating. Manage or uninstall the plugin from the Plugins tab.


## Codex CLI Installation

Google Comment Responder is not currently available to install from Codex CLI's public plugin browser. OpenAI marketplace has not been updated since the plugin was published, so it is not yet available via the CLI public marketplace. 

Until it is updated, **install manually from GitHub**.


## Manual GitHub Usage

**Install:**

```bash
codex plugin marketplace add katnissali/google-comment-responder --ref main
codex plugin add google-comment-responder@google-comment-responder
```

**Update:**

```bash
codex plugin marketplace upgrade google-comment-responder
codex plugin add google-comment-responder@google-comment-responder
```

**Uninstall:**
```bash
codex plugin remove google-comment-responder@google-comment-responder
codex plugin marketplace remove google-comment-responder
```
