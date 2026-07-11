# Learnings Log

What worked, what didn't, and what we learned along the way.

| Date | Category | Context | Learning | Action Taken |
|------|----------|---------|----------|--------------|
| 2026-07-11 | Worked | Local write file | Omitting `ArtifactMetadata` block when writing files outside the brain directory is required to write directly to the local project workspace. | Wrote workspace files without ArtifactMetadata. |
| 2026-07-11 | Didn't Work | Subagent execution | Spawning multiple self-agents in parallel can trigger 429 rate limit errors (RESOURCE_EXHAUSTED) under quota-constrained environments. | Cleaned up subagents and processed remaining file creation sequentially. |

## Categories
- **Worked**: Approaches or patterns that proved effective
- **Didn't Work**: Approaches that failed or caused issues
- **Pattern**: Useful patterns to follow in similar situations
- **Anti-Pattern**: Patterns to avoid — they cause problems

## How to Use This File
- Add a row after each significant development session.
- Be specific: what was tried, what happened, what we do differently now.
- Reference task IDs and file paths when applicable.
- Review this file when starting similar work to avoid repeating mistakes.
- Never delete entries — they are historical record.
