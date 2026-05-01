---
name: ticket-prep
description: >
  Prepare your codebase context from a Jira ticket. Use this skill whenever a user mentions a Jira ticket
  (like PA-1234, DF-567, or any PROJECT-NUMBER pattern), wants to understand what code is relevant to a
  ticket, asks to "prep" or "prepare" for working on a ticket, or says things like "what files do I need
  to touch for this ticket". Also trigger when users paste Jira URLs, ask to explore code related to a
  bug/feature described in a ticket, or want a head-start before implementing a Jira issue. Even if they
  just say "I'm working on PA-1234", invoke this skill to load the right context.
---

# Ticket Prep

Read a Jira ticket and explore the codebase to find the files most likely relevant to implementing it.
The output is a prioritized table of files with relevance scores and reasoning.

## How it works

1. **Fetch the ticket** from Jira using the bundled Python script
2. **Analyze the ticket** to extract key concepts, components, and technical clues
3. **Explore the codebase** systematically to find related files
4. **Output a ranked table** of relevant files

## Step 1: Fetch the Jira Ticket

Run the bundled script to fetch ticket data. It needs three environment variables: `JIRA_URL`, `JIRA_EMAIL`, and `JIRA_TOKEN`.

```bash
python <skill-path>/scripts/fetch_jira_ticket.py <TICKET-KEY>
```

If environment variables aren't set, tell the user what they need:
- `JIRA_URL` — their Jira Cloud URL (e.g. `https://trendminer.atlassian.net`)
- `JIRA_EMAIL` — the email on their Jira account
- `JIRA_TOKEN` — an API token from https://id.atlassian.com/manage-profile/security/api-tokens

The script outputs JSON with the ticket's summary, description, comments, subtasks, and linked issues.

## Step 2: Analyze the Ticket

From the ticket JSON, extract:

- **Keywords and domain concepts** — e.g. "export", "search results", "calculation", "comparison"
- **Component names** — anything that looks like a module, service, or class name
- **File paths or code references** — developers often mention specific files or classes in comments
- **The type of change** — bug fix (look for existing behavior), feature (look for extension points), refactor (look for the code to refactor)
- **Acceptance criteria** — these hint at which behaviors/endpoints/UI components are involved

Build a mental model of what parts of the codebase are likely involved before searching.

## Step 3: Explore the Codebase

Use a layered search strategy, starting broad and narrowing down. The goal is to be thorough without drowning in noise.

### Layer 1: Project structure
Get the lay of the land. Understand how the project is organized — what are the top-level modules, where does source code live, what build system is used. This context is essential for interpreting search results.

### Layer 2: Keyword search
Search for the key terms extracted from the ticket. Use `grep` with the most specific terms first. Look for:
- Class/file names that match domain concepts
- Method names related to the described behavior
- Configuration files mentioning relevant features
- Test files (these often reveal which production files are involved)

### Layer 3: Code structure navigation
Once you find candidate files, trace their connections:
- What does this file import/depend on?
- What calls into this file?
- Are there corresponding test files?
- Are there configuration files that wire this component?

Use code intelligence tools (LSP goToDefinition, findReferences, incomingCalls) when available — they're more precise than text search.

### Layer 4: Git history (optional but powerful)
If the ticket key appears in commit messages, check what files were touched in related commits:
```bash
git log --all --oneline --grep="<TICKET-KEY>" | head -10
```
Then for each relevant commit:
```bash
git diff-tree --no-commit-id --name-only -r <sha>
```
This is especially useful for follow-up tickets where earlier work already touched the right files.

## Step 4: Output the Results

Present a markdown table sorted by relevance (high → low):

```
| File | Relevance | Reason |
|------|-----------|--------|
| src/main/java/.../ExportService.java | 🔴 High | Core export logic mentioned in ticket description |
| src/test/.../ExportServiceTest.java | 🔴 High | Tests for the export behavior being fixed |
| src/main/java/.../SearchController.java | 🟡 Medium | Entry point that triggers the export |
| src/main/java/.../config/ExportConfig.java | 🟢 Low | Configuration — may need changes if new export type |
```

**Relevance levels:**
- 🔴 **High** — Almost certainly needs changes, or is directly referenced by the ticket
- 🟡 **Medium** — Likely involved, either as a dependency or as context needed to understand the change
- 🟢 **Low** — Possibly relevant, worth knowing about but may not need changes

After the table, add a brief **Summary** explaining:
- What the ticket is about (one sentence)
- The main area of the codebase affected
- Any risks or dependencies worth noting (e.g. "this touches a shared utility used by 5 other services")

## Tips for accuracy

- **Prefer precision over recall.** A table with 8 highly relevant files is better than 30 files that "might" be related. Developers lose trust when the list is full of noise.
- **Tests matter.** Always look for test files corresponding to production files. If a test file exists, it belongs in the table — the developer will need to update it.
- **Don't ignore config.** Build files (pom.xml, build.gradle), CI configs, and property files are relevant when the ticket involves dependencies, feature flags, or deployment.
- **Read the comments.** Jira comments often contain the most specific technical guidance — a developer might have written "this is in SearchXlsxExportGenerator" which saves a lot of searching.
