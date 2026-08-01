# OpenAI Plugin Submission Listing Draft

## Submission Type

Skills only

## Plugin Details

- Plugin name: Google Comment Responder
- Package name: google-comment-responder
- Developer identity: Emma Arenstein
- Category: Productivity
- Repository: https://github.com/katnissali/google-comment-responder
- Website URL: https://github.com/katnissali/google-comment-responder
- Support URL: https://github.com/katnissali/google-comment-responder/issues
- Privacy policy URL: https://github.com/katnissali/google-comment-responder/blob/main/PRIVACY.md
- Terms URL: https://github.com/katnissali/google-comment-responder/blob/main/TERMS.md

## Short Description

Reply to doc comments safely

## Long Description

Google Comment Responder helps Codex respond to existing Google Drive, Docs, Sheets, and Slides comment threads using a careful, auditable workflow. It guides Codex to scan all configured comment threads, filter only eligible requests, read nearby document context, draft concise replies, write only to existing threads, avoid deleting comments, resolve only when explicitly asked, and verify writeback.

This is a skills-only plugin. It does not provide its own Google OAuth connector, store user data, or grant document access. Users must already have appropriate Google Drive tools and permissions in their ChatGPT or Codex environment.

## Starter Prompts

- Use Google Comment Responder to respond to unresolved AGENT: comments in this Google Doc.
- Use Google Comment Responder to draft replies for selected comment threads without posting them.
- Use Google Comment Responder to scan these documents and report which comment threads need more evidence before replying.

## Reviewer Notes

- The plugin contains one bundled skill: google-comment-responder.
- The plugin is intentionally generic and includes no private document IDs, company links, credentials, or project-specific assumptions.
- The plugin relies on the user's existing Google Drive/Docs comment-capable tools and permissions.
- Google product names are used descriptively. This plugin is not affiliated with or endorsed by Google.
- The plugin is designed to reply to existing comment threads only; it should not create detached top-level comments.
