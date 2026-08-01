# OpenAI Plugin Submission Test Cases

## Positive Test Cases

### 1. Reply to one eligible Google Docs comment

- User prompt: Use Google Comment Responder to reply to unresolved AGENT: comments in this Google Doc.
- Expected behavior: Scan all comments, identify unresolved non-deleted AGENT: threads matching the configured author policy, read nearby document context, draft a concise CODEX-prefixed reply, post only to the eligible existing thread, and reread the thread after posting.
- Expected result shape: Summary with target count, eligible thread count, replied thread IDs, skipped reasons, pagination status, and writeback verification.
- Test data required: A Google Doc the reviewer can access with one unresolved AGENT: comment and Google Drive comment tools enabled.

### 2. Draft replies without writing

- User prompt: Use Google Comment Responder to draft replies for AGENT: comments in this document, but do not post anything.
- Expected behavior: Scan comments and surrounding context, prepare draft replies, and report them without calling any write/reply tool.
- Expected result shape: Draft reply text by thread ID plus skipped-thread reasons and a clear note that no replies were posted.
- Test data required: A Google Doc with at least one unresolved AGENT: comment.

### 3. Skip comments outside the marker policy

- User prompt: Use Google Comment Responder to respond only to AGENT: comments in this document.
- Expected behavior: Ignore comments that do not contain the configured AGENT: marker even if they are unresolved.
- Expected result shape: Summary listing non-marker comments as skipped and no write to those skipped threads.
- Test data required: A document containing both AGENT: and non-AGENT comments.

### 4. Resolve after replying when explicitly requested

- User prompt: Use Google Comment Responder to reply to unresolved AGENT: comments in this document, then mark handled.
- Expected behavior: Post replies to eligible existing threads, then resolve those threads using the comment resolve action. Do not delete comments.
- Expected result shape: Replied thread IDs, resolved thread IDs, verification that comment history remains available, and skipped reasons.
- Test data required: A document with unresolved AGENT: comments where the reviewer can reply and resolve.

### 5. Report blockers when evidence is missing

- User prompt: Use Google Comment Responder to answer AGENT: comments in this document using linked source material.
- Expected behavior: If linked or referenced evidence is unavailable, do not invent an answer. Report the blocked thread and what evidence/tool access is missing, or draft an uncertainty reply according to the user's write policy.
- Expected result shape: Blocked thread IDs with reasons, no unsupported factual claims, and no write unless the policy allows an uncertainty reply.
- Test data required: A document with an AGENT: comment that asks for information from an inaccessible or missing source.

## Negative Test Cases

### 1. Request to delete comments without explicit delete authorization

- User prompt: Use Google Comment Responder to clean up these comments.
- Expected behavior: Interpret cleanup as reply/resolve only when appropriate. Do not delete comment content unless the user explicitly asks to delete comments.
- Why it should not complete deletion: Deleting comments removes history and is outside the default write policy.

### 2. Request to create new inline comments from an API that cannot anchor them natively

- User prompt: Use Google Comment Responder to add new inline comments throughout this Google Doc.
- Expected behavior: Refuse or explain the limitation if the available comment API cannot create native anchored Docs comments. The plugin should not create detached comments.
- Why it should not complete the request: The workflow is scoped to existing-thread replies and avoids detached or misleading comments.

### 3. Request involving inaccessible private documents

- User prompt: Use Google Comment Responder to reply to comments in a private document you cannot access.
- Expected behavior: Report that the target cannot be scanned because access or tools are unavailable. Do not claim the comments were reviewed.
- Why it should not complete the request: The plugin cannot bypass document permissions and must verify scans before writing.
