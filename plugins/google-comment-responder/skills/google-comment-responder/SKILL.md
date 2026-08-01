---
name: google-comment-responder
description: Reusable workflow for responding to existing document comment threads. Use when Codex needs to scan comments on one or more documents, filter by configurable markers such as `AGENT:`, draft concise replies, post replies only to eligible existing threads, resolve threads only when asked, avoid deleting comments, and verify writeback. Works as a generic workflow for Google Drive comments or any connector/API that exposes comment threads, authors, status, replies, and pagination.
---

# Google Comment Responder

## Overview

Use this skill to run a configurable comment responder without embedding any person-, company-, document-, or project-specific IDs. Treat all targets, author filters, markers, evidence sources, and write rules as per-run configuration gathered from the user request, local instructions, or an explicit config file.

Treat eligible comments as another input surface for Codex. Once a thread passes the configured eligibility filters, interpret the latest eligible comment as the user's request and execute it with the same resources and instruction hierarchy available in an ordinary Codex prompt: user request, local instruction files such as `AGENTS.md`, memory, configured skills, connected apps/tools, documents, repositories, prior notes, and any explicit resources. Do not limit the answer to the target document unless the request or policy says to.

## Required Configuration

Before reading or writing comments, identify these settings:

- Target files: stable file IDs, URLs, or exact paths. Prefer stable IDs over names when available.
- Comment tool: the connector/API that can list, reply to, resolve, or read back comments.
- Eligibility marker: labels such as `AGENT:`, `BOT:`, `REVIEW:`, or another requested string.
- Author filter: if no author name is provided, try to infer it from all available resources before asking. Use connector metadata such as `author.me: true`, a `whoami` result, the authenticated profile/email, document comment authors, local instructions, explicit config, or other provided context. If the author is still unknown or ambiguous, ask before replying. The user or config can adjust this later, including allowing multiple authors.
- Status filter: usually unresolved and non-deleted threads only.
- Skip markers: phrases such as `do not respond`, `ignore`, or any user-specified exclusion.
- Evidence sources: all available resources that would normally be available for the same Codex prompt, including documents, attachments, repositories, memory, local instructions such as `AGENTS.md`, configured skills/tools, prior notes, and current comments. For factual asks, prefer live primary sources and use memory or prior notes as leads rather than final evidence when verification is practical.
- Surrounding context: nearby document text around each comment anchor, quote, slide, cell, or section.
- Write policy: draft-only, post replies, resolve after replying, or report-only.
- Output format: counts, replied thread IDs, skipped reasons, and unresolved blockers.

If a required setting is missing and a reasonable default would risk writing the wrong comment, ask one concise question before posting.

## Generic Config Shape

Use this shape when the user asks to save or describe a reusable responder:

```yaml
targets:
  - id: "<stable-file-id-or-url>"
    type: "<doc|sheet|slide|file|other>"
    label: "<human-readable-label>"
eligibility:
  marker: "AGENT:"
  author_filter:
    default: "running_user"
    infer_if_missing: true
    allowed_authors: []
    ask_if_unknown: true
    allow_multiple_authors: true
  unresolved_only: true
  non_deleted_only: true
  skip_markers:
    - "do not respond"
    - "ignore"
write_policy:
  mode: "draft-then-post"
  reply_to_existing_threads_only: true
  allow_resolve: false
  allow_delete: false
pagination:
  page_size: 100
  require_exhaustive_scan: true
verification:
  reread_after_write: true
  report_thread_ids: true
context:
  read_surrounding_text: true
```

Do not ship a config with real private file links unless the user explicitly asks for a project-specific responder.

## Workflow

1. Read the task rules.
   - Read the user request and any local instruction file that applies to the current workspace.
   - Treat each eligible comment as the task prompt for that thread, subject to the configured filters and write policy.
   - Use the same instruction hierarchy and available resources that Codex would use for a normal user prompt, including memory, `AGENTS.md`, local instructions, tools, skills, files, connected apps, and explicitly provided resources.
   - Let explicit user instructions decide scope and write policy.
   - Do not add project-specific memory to reusable workflows unless the user asks for a project-specific plugin.

2. Confirm the tool can do the job.
   - Use the native connector/API for the target file system when possible.
   - Make sure it can list comments, inspect thread status, write replies, and reread threads.
   - If it cannot create native anchors, do not create new top-level inline comments. Existing-thread replies are usually okay.

3. Read every in-scope comment thread.
   - Fetch every target in scope.
   - Use the connector's supported page size; if unknown, use 100 or lower.
   - Keep paging each target until the continuation token is empty or `null`.
   - If a comment page appears clipped or truncated, rerun with smaller pages and keep paging before deciding the scan is complete.
   - Preserve thread IDs, comment IDs, authors, timestamps, quoted text, anchors, resolved/deleted status, and existing replies.

4. Keep only eligible threads.
   - Keep existing threads that match the configured marker.
   - Apply the status, deletion, author, and skip-marker filters.
   - If no author name or filter is provided, infer the intended author from all available resources before asking. In Google Drive comment data, prefer `author.me: true` when present; otherwise use connector identity/profile data such as display name or email, local instructions, explicit config, document comment authors, or other provided context.
   - If the author is still unknown or ambiguous after checking available resources, ask the user which author or authors to include before replying.
   - Allow the user or config to override the default author filter with one or more explicit allowed authors.
   - Check prior replies before drafting so already-answered threads are not duplicated.
   - Treat a thread as answered when a later non-deleted reply already satisfies the latest eligible ask, even if the thread is still unresolved.
   - Because some comment APIs post agent replies as the authenticated user, decide whether a prior reply answers the thread from reply content, timestamp, and action, not author identity alone.

5. Understand each eligible comment.
   - Use the comment text as the source of truth for what needs answering.
   - Read surrounding document context before drafting: anchored or quoted text, nearby paragraph, slide, cell range, heading, or section.
   - Use all available resources that would normally be available for the same request in Codex, not only the target document.
   - Prefer primary or attached sources over broad search. For requests asking for examples, links, source locations, or current facts, actively look up the specific artifact instead of answering generically.
   - State uncertainty plainly when evidence is incomplete.
   - If no reliable evidence is available, either draft an uncertainty reply or ask the user, depending on the write policy.

6. Draft all replies first.
   - Prepare every reply before posting any of them.
   - Keep replies short, direct, and scoped to the comment.
   - Use one reply per thread unless a small follow-up is needed to fix rendering or a broken link.
   - Do not edit the document body unless the user separately asks for body edits.

7. Write only the allowed updates.
   - Reply to existing eligible threads only.
   - Do not delete comments unless the user explicitly asks to delete them.
   - Resolve threads only when the user asks to resolve, clean up, close, or mark handled.
   - If resolving after replying, use the resolve action so the comment history stays preserved.

8. Verify the writeback.
   - Reread every written thread.
   - Confirm the reply text, thread ID, and final status.
   - If a write failed or readback is unavailable, report that as incomplete.

9. Report what happened.
   - Include the number of target files fully scanned.
   - Include the number of eligible threads found.
   - List replied thread IDs, or say that no replies were posted.
   - Summarize skipped threads by reason, such as resolved, deleted, author mismatch, skip marker, already answered, or blocked by missing evidence/tool access.
   - Say whether pagination reached the end for every target.
   - Say whether writeback was verified.

## Reply Style

- Prefix every drafted or posted comment reply with `CODEX:`. If a reply already starts with `CODEX:`, do not add a second prefix.
- Keep replies concise and useful inside the thread.
- Answer the latest ask, not every historical aside in the thread.
- When a reply references a file, document, comment thread, issue, PR, source, or other linkable artifact, include the link using the target system's supported formatting. Do not add unrelated links just to increase link count.
- Prefer plain visible URLs when the comment system mangles rich formatting.
- Do not over-explain the workflow in the comment reply itself.

## Safety Rules

- Never infer target files from a similar prior project when the current task gives different targets.
- Never call setup, configuration, or partial search a completed responder run.
- Never silently skip an eligible thread because evidence is inconvenient. Report the blocker or draft an uncertainty reply according to policy.
- Never reuse a continuation token from another target or a prior scan.
- Never answer comments outside the configured marker and author filters.
- Never delete comment content as a substitute for resolving or replying.

## Verification Checklist

Before the final response, confirm:

1. Every target reached the end of pagination or the incomplete target is named.
2. Only eligible existing threads were answered.
3. No comment was deleted unless explicitly requested.
4. No document body edits were made unless explicitly requested.
5. All posted replies were reread successfully, or failures are named.
6. The final report includes counts, replied thread IDs, skipped reasons, and remaining blockers.
