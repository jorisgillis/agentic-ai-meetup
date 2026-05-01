# Agentic AI Meetup — Research Output

---

## Part 1: Terminology Taxonomy

### 1.1 The Big Picture: AI Agent vs Agentic AI

These two terms are often used interchangeably but have a meaningful
distinction (per arXiv 2505.10468, OECD, MIT Sloan, Springer):

| Term | Definition | Scope |
|------|-----------|-------|
| **AI Agent** | A software entity that perceives its environment, reasons, and acts autonomously to achieve a specific goal. It uses tools, executes actions, and may interact with users. | Single-task, reactive, modular. A building block. |
| **Agentic AI** | A paradigm where multiple coordinated AI agents collaborate with persistent memory, dynamic task decomposition, and self-organized autonomy. | Multi-domain, proactive, adaptive. The system of systems. |

**Key insight:** All agentic AI contains AI agents, but not all AI
agents constitute agentic AI. A chatbot is an agent. A fleet of agents
that autonomously triages, debugs, and deploys a fix is agentic AI.

Sources:
- arXiv: "AI Agents vs. Agentic AI: A Conceptual Taxonomy" (2505.10468)
- OECD: "Can we create a clear understanding of what agentic AI is and does?"
- MIT Sloan: "Agentic AI, explained"
- Springer: "Agentic AI: a comprehensive survey of architectures" (2025)

---

### 1.2 Core Terminology — Unified Across Coding Agents

| # | Term | Definition | Claude Code | GitHub Copilot |
|---|------|-----------|-------------|----------------|
| 1 | **Coding Agent** | An autonomous AI system that writes, executes, tests, and iterates on code in a feedback loop. The top-level entity a developer interacts with. | Claude Code (the CLI) | Copilot coding agent (in VS Code / CLI) |
| 2 | **Model** | The LLM that powers the agent's reasoning. The "brain." It generates text/code but cannot act on its own. | Claude Sonnet/Opus/Haiku | GPT-4.1 / GPT-5.x |
| 3 | **Harness** | Everything around the model that makes it a useful agent: system prompts, tool definitions, state management, orchestration logic, guardrails, feedback loops. **Agent = Model + Harness.** | Claude Code's runtime (system prompt + CLAUDE.md + tools + hooks + settings) | Copilot's runtime (system prompt + copilot-instructions.md + tools + setup steps) |
| 4 | **Agent Loop** | The core cycle that drives autonomous behavior: plan -> act (write code) -> execute -> observe results -> correct -> repeat. Also called "agentic loop" or "engineering loop." | Built into Claude Code | Built into Copilot agent mode |
| 5 | **Tool** | A specific, atomic function the agent can call. Stateless, provided by the harness. Examples: bash, file read, grep, API call, web search. | Built-in tools (bash, view, edit, grep, glob, lsp, etc.) | Built-in tools (bash, view, edit, grep, glob, etc.) |
| 6 | **Skill** | A self-contained, reusable capability that extends the agent with domain-specific instructions. Has a trigger description, step-by-step instructions, and optionally bundled scripts/tools. Think of it as a "recipe" the agent follows. | Skill (SKILL.md in `.claude/skills/`) | Skill (skill files in project, with description + instructions) |
| 7 | **MCP Server** | An external tool provider using the Model Context Protocol — an open standard (by Anthropic, now Linux Foundation) for connecting AI models to external data sources and tools via JSON-RPC 2.0. Architecture: Host -> Client -> Server. Like USB: standardized plug-and-play interface. | Configured in `.claude/settings.json` under `mcpServers` | Configured in VS Code settings / copilot config |
| 8 | **Sub-agent** | A child agent spawned by the main agent to handle a subtask in a separate context. Enables parallelism and scope isolation. Has its own tool access and may use a different (cheaper/faster) model. | `task` tool: explore, task, general-purpose, code-review agents | Background agents / task delegation |
| 9 | **Orchestrator** | The part of the harness that coordinates multiple sub-agents: assigns work, manages dependencies, merges outputs. The "project manager" inside the agent. | Built into Claude Code (spawns sub-agents, manages context) | Built into Copilot (manages agent delegation) |
| 10 | **Command** | A user-triggered shortcut that invokes a specific skill or workflow. Like an alias for a complex prompt. | Slash commands (`/command-name`), stored as `.claude/commands/*.md` | Slash commands, chat commands |
| 11 | **Hook** | Event-driven automation that fires at lifecycle events (session start, before/after tool use, file change). Can run scripts, enforce guardrails, trigger workflows. | Hooks in `.claude/settings.json` (PreToolUse, PostToolUse, etc.) | copilot-setup-steps.yml, pre/post actions |
| 12 | **Context Priming** | Pre-loading relevant information into the agent's context before it starts working. Reduces hallucination and improves accuracy. | CLAUDE.md (project memory), skill output, `--add-dir` flag | copilot-instructions.md, custom instructions |
| 13 | **Eval** | A repeatable test measuring how well a skill/agent performs. Input -> expected behavior -> score. The "TDD of prompt engineering." | JSON-based evals (evals/evals.json with prompt + expectations) | Custom eval scripts / frameworks |
| 14 | **Plugin** | (Legacy/evolving) An add-on connecting the agent to external services. In modern practice, this role is split between MCP servers (for tool access) and skills (for workflow logic). | `.claude-plugin/plugin.json` (older concept) | Extensions / integrations |

Sources:
- Anthropic: modelcontextprotocol.io, claude.com/docs
- Martin Fowler: "Harness engineering for coding agent users" (martinfowler.com)
- Anthropic: "Harness design for long-running apps" (anthropic.com/engineering)
- LangChain: "The Anatomy of an Agent Harness"
- Addy Osmani: "The Code Agent Orchestra"
- latent.space: "Agent Engineering: Harness Patterns & IMPACT Framework"
- Simon Willison on "agentic coding" (willison.name)

---

### 1.3 The Kitchen Analogy (for the session)

| Concept | Kitchen Analogy | Example |
|---------|----------------|---------|
| Model | The chef | Claude Sonnet, GPT-5 |
| Harness | The kitchen (layout, workflow, rules) | System prompt, CLAUDE.md, tool config, hooks |
| Agent Loop | The cooking process (prep -> cook -> taste -> adjust -> repeat) | plan -> code -> run -> observe -> fix |
| Skill | A recipe (reusable, composable, domain-specific) | "Ticket Prep", "Code Review for Python" |
| Tool | A utensil (fork, knife, pan) | bash, grep, file read, web search |
| MCP Server | A kitchen appliance you plug in (blender, dishwasher) | GitHub MCP, Jira MCP, Postgres MCP |
| Sub-agent | A sous-chef you delegate to | "explore this module", "run these tests" |
| Command | A shortcut on the recipe card ("Press button 3 for espresso") | `/review`, `/ticket-prep PA-1234` |
| Hook | A kitchen timer or smoke alarm (event-driven) | "Before any bash command, check for destructive ops" |
| Eval | A taste test with a scorecard | "Did it find the right files? 5/6 expectations pass" |

**Headline:** *The model is the chef. The harness is the kitchen. Your job is to build a great kitchen.*

---

### 1.4 Definitions Floating Around the Internet (raw comparison)

#### "Agent"
| Source | Definition |
|--------|-----------|
| Anthropic | An AI system that can use tools, maintain state, and work autonomously toward a goal |
| OpenAI | A system that uses a model to execute multi-step tasks using tools |
| Google DeepMind | An entity that perceives, reasons, and acts in an environment |
| LangChain | A system that uses an LLM to determine which actions to take and in what order |
| Academic (arXiv) | A software entity with autonomy, reactivity, proactivity, and social ability |

#### "Skill"
| Source | Definition |
|--------|-----------|
| Claude Code | A markdown file (SKILL.md) with trigger description + instructions that the agent follows for a specific domain task |
| GitHub Copilot | A modular capability file with description and instructions, invokable by the agent |
| Microsoft Semantic Kernel | A unit of AI capability — can be a prompt function or native code function |
| Amazon Bedrock Agents | An action group — a collection of APIs the agent can invoke |

#### "Tool"
| Source | Definition |
|--------|-----------|
| Anthropic (MCP spec) | A capability exposed by an MCP server that the model can invoke; has a name, description, and JSON schema for parameters |
| OpenAI (function calling) | A function description provided to the model; model outputs structured arguments, client executes |
| LangChain | A callable that wraps a function with a description for the LLM to use |
| Claude Code runtime | A built-in function (bash, view, edit, grep, etc.) the agent can call during the agent loop |

#### "Harness"
| Source | Definition |
|--------|-----------|
| Martin Fowler (2025) | The system of guides and guardrails that surrounds a coding agent, including feedforward guides and feedback sensors |
| Anthropic (2025) | The design choices that make an agent reliable for long-running tasks: state, tools, constraints, verification |
| latent.space | All non-model infrastructure: prompts, tools, state, orchestration, memory, hooks |
| arXiv (2604.25850) | Observability-driven patterns for reliable agent execution |

#### "MCP" (Model Context Protocol)
| Source | Definition |
|--------|-----------|
| modelcontextprotocol.io | An open standard for connecting AI models to external data sources and tools. Uses JSON-RPC 2.0 with a Host -> Client -> Server architecture |
| Wikipedia | A protocol created by Anthropic (Nov 2024), solving the NxM integration problem. Adopted by Anthropic, OpenAI, Google, Microsoft |
| Linux Foundation (Dec 2025) | Governance transferred to LF; enterprise features include zero-trust, auditing, horizontal scaling |

---

## Part 2: Additional Agent/Skill Ideas

### Your existing 5:

| # | Name | Level | Core idea |
|---|------|-------|-----------|
| a | Code Reviewer | Worked out | Python-specific code review |
| b | Ticket Prep | Worked out | Map Jira ticket -> relevant codebase files |
| c | Journal Buddy | Idea + evals | Log work, generate standup summary |
| d | PR Review | Idea + evals | Rank PRs by contribution opportunity |
| e | Commit Ghostwriter | Free-form | Write "why"-based commit messages |

### 7 new ideas:

#### f. Dependency Upgrade Scout
**Level:** Idea + evals
**What it does:** Scans `package.json` / `pom.xml` / `requirements.txt` for outdated dependencies. For each, fetches the changelog, assesses breaking-change risk, and outputs a prioritized upgrade plan with migration notes.
**Why it's good for a workshop:** Bounded scope, real developer pain. Eval: "Did it correctly identify the breaking changes in the changelog? Did it miss any critical deprecations?"
**Eval ideas:**
- Given a known outdated `package.json`, does it flag the dep with a known breaking change?
- Does the migration plan mention the specific API change?
- Does it correctly mark non-breaking minor bumps as low risk?

#### g. Test Gap Finder
**Level:** Idea + evals
**What it does:** Analyzes recent commits or a specific module, cross-references with existing test files, and identifies untested code paths. Suggests specific test cases to write.
**Why it's good for a workshop:** Developers feel this pain daily. Combines code analysis with reasoning.
**Eval ideas:**
- Given a module with 3 public methods and tests for only 1, does it identify the 2 untested ones?
- Does it suggest meaningful test scenarios (not just "test method X")?
- Does it find the corresponding test file or suggest where to create one?

#### h. Release Notes Drafter
**Level:** Worked out (pre-build it)
**What it does:** Runs `git log` since last tag, categorizes commits/PRs into features, fixes, chores, breaking changes. Writes user-facing release notes. Can target different audiences (developer vs. end-user).
**Why it's good for a workshop:** Simple git + summarization. Participants can add: audience modes, conventional commit parsing, link to PRs, emoji categorization.
**Extension ideas for participants:**
- Add "breaking changes" section with migration steps
- Generate both technical and user-facing versions
- Integrate with GitHub Releases API to auto-publish

#### i. Onboarding Guide Generator
**Level:** Free-form
**What it does:** Given a directory or module, generates a "How This Works" guide: architecture overview, key files with descriptions, data flow, common gotchas, "start here" pointers for new developers.
**Why it's good for a workshop:** Creative, open-ended. Every participant's output will be different. No single "right answer."
**Discussion prompt:** What makes a good onboarding guide? How do you eval "helpfulness" for a new team member?

#### j. Context Switcher / "Where Was I?"
**Level:** Idea + evals
**What it does:** When switching branches or resuming work after a break, it summarizes: what you were working on (from git log + branch diff), what changed since you left (new commits by others), what's still TODO (from TODO comments, open test failures, uncommitted changes).
**Why it's good for a workshop:** Every developer knows the pain of context switching. Very relatable.
**Eval ideas:**
- Given a branch with 5 recent commits by the user, does the summary capture the main theme?
- Does it mention uncommitted changes?
- Does it flag conflicts with main branch changes?

#### k. Incident Postmortem Writer
**Level:** Free-form
**What it does:** After a production incident, gathers: recent deploys (git log), error logs (if accessible), related PRs, and timeline of events. Drafts a structured postmortem: timeline, what happened, root cause, impact, action items.
**Why it's good for a workshop:** Complex, multi-source. Great for advanced participants who want to integrate multiple tools/APIs. Open discussion: how do you eval a postmortem?

#### l. Refactor Radar
**Level:** Worked out (pre-build it)
**What it does:** Scans a codebase for code smells: long methods (>50 lines), high coupling (file imports >10 others), duplicated logic (similar code blocks), deeply nested conditionals. Prioritizes by impact/effort. Suggests specific refactoring steps with before/after reasoning.
**Why it's good for a workshop:** Can be pre-built with basic detection heuristics. Participants add new smell detectors: "detect God classes", "find methods with too many parameters", "flag missing error handling."
**Extension ideas for participants:**
- Add language-specific smells (Python: mutable default args; Java: raw types)
- Score by "blast radius" (how many files depend on the smelly code)
- Suggest specific design patterns to apply

### Bonus ideas (in case participants want more):

| # | Name | One-liner | Level |
|---|------|-----------|-------|
| m | **Flaky Test Detective** | Analyzes CI history to find tests that pass/fail non-deterministically, hypothesizes root causes (timing, ordering, shared state) | Idea + evals |
| n | **API Contract Checker** | Validates that code changes don't break OpenAPI/Swagger specs; alerts on undocumented endpoints or type drift | Idea + evals |
| o | **Migration Assistant** | Guides framework/library upgrades (e.g., React 17->18, Spring Boot 2->3) by scanning for breaking patterns and auto-suggesting rewrites | Free-form |
| p | **Documentation Drift Detector** | Compares code behavior with its documentation; flags stale/wrong docs | Idea + evals |
| q | **Meeting Notes -> Tickets** | Takes raw meeting notes and extracts actionable tickets with acceptance criteria, priority, and assignee suggestions | Free-form |

---

## Part 3: Eval Frameworks & Standards

### 3.1 What is an eval?

An eval is a repeatable test that answers: **"Does my skill/agent do the right thing?"**

It's the TDD of prompt engineering. Just as you write tests before (or alongside) code, you write evals before (or alongside) skills.

### 3.2 Anatomy of a skill eval (from your Ticket Prep project)

```json
{
  "skill_name": "ticket-prep",
  "evals": [
    {
      "id": 1,
      "prompt": "I need to work on PA-3467. Can you prep the codebase for me?",
      "expected_output": "A markdown table of relevant files...",
      "files": [],
      "expectations": [
        "The output includes a markdown table with File, Relevance, and Reason columns",
        "The file SearchXlsxExportGenerator.java appears with High relevance",
        "At least one test file is included in the table",
        "The output contains a brief summary section"
      ]
    }
  ]
}
```

**The four pieces:**
1. **`prompt`** — what the user says (input)
2. **`expected_output`** — human-readable description of what "good" looks like
3. **`expectations`** — checkable assertions (verified by LLM-as-judge or string match)
4. **`files`** — optional context files to pre-load

### 3.3 Five levels of eval sophistication

| Level | Approach | How it works | Best for | Example |
|-------|----------|-------------|----------|---------|
| 1 | **String/pattern matching** | Check if output contains specific strings, patterns, or structure | Structured output (tables, JSON, file names) | "Output contains `SearchXlsxExportGenerator.java`" |
| 2 | **LLM-as-judge** | A second LLM grades the output against expectations on a rubric | Subjective quality, reasoning, tone | "Rate 1-5: Does the summary correctly identify the main area of the codebase?" |
| 3 | **Execution-based** | Run the output (code, commands) and check results | Code generation, automation skills | "The generated test file compiles and 3/3 tests pass" |
| 4 | **Human-in-the-loop** | Human annotators score on a rubric | Nuanced tasks, calibrating automated judges | "Developer rates the file table as 'useful' or 'not useful'" |
| 5 | **A/B + statistical** | Compare two skill versions on same inputs, track win rate with variance analysis | Iterative improvement, prompt optimization | "V2 of the skill scores higher on 70% of eval cases (p<0.05)" |

### 3.4 Eval framework landscape (2025-2026)

| Framework | Type | Best for | Key feature | Install |
|-----------|------|----------|-------------|---------|
| **Promptfoo** | Open-source CLI | Prompt iteration, red-teaming, CI/CD | YAML test definitions, 500+ adversarial attack vectors, multi-model testing | `npm install -g promptfoo` |
| **DeepEval** | Open-source Python | Agent/code testing | "Pytest for LLMs", 50+ built-in metrics, CI/CD integration | `pip install deepeval` |
| **Braintrust** | Commercial (free tier) | Team collaboration, production monitoring | Annotation UI, experiment versioning, score diffs, tracing | braintrust.dev |
| **Ragas** | Open-source Python | RAG pipeline evaluation | Faithfulness, context relevance, answer relevance metrics | `pip install ragas` |
| **LangSmith** | Commercial | LangChain ecosystems, observability | Dataset curation, detailed tracing, human feedback | smith.langchain.com |
| **Inspect AI** | Open-source (UK AISI) | Safety and capability evals | Structured eval framework, sandboxed execution, government-backed | `pip install inspect-ai` |

### 3.5 Recommended strategy for the workshop

**Use the lightweight JSON format** (as in your ticket-prep project):

- No framework to install
- Agent-native (the coding agent itself can read and grade evals)
- Portable (works with Claude Code, Copilot, or any agent)
- Easy to understand for beginners

**Running evals in practice:**

1. The agent reads the eval JSON
2. For each case, it runs the skill with the given prompt
3. It checks each expectation against the output (string match or LLM-as-judge)
4. Reports pass/fail per expectation + overall score

**When to graduate to a framework:**

| Signal | Framework |
|--------|-----------|
| 50+ eval cases, YAML scales better | **Promptfoo** |
| Team needs annotation/review workflow | **Braintrust** |
| Want CI/CD gating on eval scores | **DeepEval** + pytest |
| Evaluating RAG pipelines | **Ragas** |
| Need tracing + observability | **LangSmith** |
| Government/safety compliance | **Inspect AI** |

### 3.6 Evals as Guardrails vs Optimization Targets

The eval JSON on its own is just data. It becomes powerful when you wire it into a **loop**. There are two fundamentally different loops:

#### A) Guardrail: "Don't ship a regression"

This is the defensive use case. You change your skill (edit the SKILL.md, tweak the prompt, update a bundled script) and want to make sure you didn't break anything.

```
+-------------------------------------------------+
|  Developer edits SKILL.md                       |
|       v                                         |
|  Run eval suite (all cases)                     |
|       v                                         |
|  Score each expectation (string match or judge) |
|       v                                         |
|  +-------------+    +------------------+        |
|  | All pass?   |-Y-->| Ship the change  |        |
|  +-------------+    +------------------+        |
|       | N                                       |
|       v                                         |
|  Block: show which expectations regressed       |
|       v                                         |
|  Developer fixes SKILL.md, re-runs              |
+-------------------------------------------------+
```

**How to implement this concretely:**

**Option 1: Agent-native (no framework)**
Ask the coding agent itself to run the evals:
```
"Read skills/evals/evals.json. For each eval case, run the ticket-prep skill
with the given prompt. Then check each expectation against the output. Report
a pass/fail table. Fail if any expectation that previously passed now fails."
```
This works because the coding agent can invoke the skill, observe the output, and judge expectations — it's an agent evaluating itself (or a different agent evaluating a skill).

**Option 2: CI/CD with Promptfoo**
Convert the eval JSON to Promptfoo YAML and gate your pipeline:
```yaml
# promptfooconfig.yaml
prompts:
  - file://skills/SKILL.md
tests:
  - vars:
      input: "I need to work on PA-3467. Can you prep the codebase for me?"
    assert:
      - type: contains
        value: "SearchXlsxExportGenerator.java"
      - type: llm-rubric
        value: "The output contains a markdown table with File, Relevance, and Reason columns"
```
```bash
promptfoo eval --fail-under 100   # gate: 100% of assertions must pass
```
Wire this into GitHub Actions / GitLab CI so PRs that regress the skill get blocked.

**Option 3: Git hook (lightweight)**
A pre-commit or pre-push hook that runs the eval suite locally:
```bash
#!/bin/bash
# .git/hooks/pre-push
claude --skill ticket-prep --eval skills/evals/evals.json --fail-on-regression
```
(Conceptual — the exact CLI flags depend on your agent's eval runner.)

---

#### B) Optimization Target: "Make the skill better"

This is the offensive use case. You have a skill that scores 4/6 on expectations and you want to get it to 6/6 — or you want to compare two versions and pick the better one.

```
+------------------------------------------------------+
|  Start with SKILL.md v1                              |
|       v                                              |
|  Run eval suite -> Score: 4/6 expectations pass       |
|       v                                              |
|  Analyze failures: which expectations fail? Why?     |
|       v                                              |
|  Edit SKILL.md v2 (tweak instructions, add steps)    |
|       v                                              |
|  Run eval suite -> Score: 5/6                         |
|       v                                              |
|  Repeat until score plateaus or reaches target       |
|       v                                              |
|  (Optional) Run v1 vs v2 on 20 cases -> v2 wins 75%  |
|       v                                              |
|  Ship v2                                             |
+------------------------------------------------------+
```

**Three ways to do this:**

**1. Manual iteration (most common today)**
You are the optimizer. Read the failing expectations, reason about why the skill's output missed them, and edit the SKILL.md accordingly. This is the "prompt engineering" loop — evals just make it measurable instead of vibes-based.

**2. Agent-assisted optimization**
Ask the coding agent to optimize its own skill:
```
"Read skills/SKILL.md and skills/evals/evals.json.
Run all eval cases. For each failing expectation, analyze why it failed.
Then propose edits to SKILL.md that would fix the failures WITHOUT
breaking the passing expectations. Apply the edits, re-run evals,
and report the before/after scores."
```
This is the "agent improving its own recipes" pattern. It works surprisingly well for instruction-based skills because the agent can reason about what instructions would produce better output.

**3. Automated optimization (DSPy-style)**
For advanced use: treat the skill prompt as a parameter and the eval score as a loss function. Frameworks like DSPy can automatically search the prompt space to maximize the eval score. This is overkill for a workshop but worth mentioning:
```python
# Pseudocode
for iteration in range(10):
    candidate_skill = mutate(current_skill)       # tweak instructions
    score = run_evals(candidate_skill, eval_cases) # measure
    if score > best_score:
        best_score = score
        current_skill = candidate_skill            # keep improvement
```

---

#### C) The Feedback Matrix: Guardrail x Optimization combined

In practice, you use both loops together. Here's the complete workflow:

| Phase | What you do | Eval role |
|-------|------------|-----------|
| **1. Write evals first** | Define what "good" looks like before writing the skill | Specification |
| **2. Build skill v1** | Write SKILL.md, run evals, iterate until score is acceptable | Optimization target |
| **3. Ship & gate** | Add evals to CI/CD or pre-commit hook | Guardrail |
| **4. Evolve** | Add new eval cases as you discover edge cases in production | Expanding the guardrail |
| **5. Improve** | Periodically re-optimize the skill against the growing eval suite | Optimization target again |

This is **Eval-Driven Development (EDD)** — the TDD equivalent for AI skills:
- Evals are your tests
- The skill (SKILL.md) is your implementation
- The eval score is your coverage metric
- CI gating is your test suite requirement

---

#### D) Practical example: Ticket Prep eval-as-guardrail

Using the existing `ticket-prep` evals, here's what a concrete guardrail run looks like:

```
Eval run: ticket-prep (3 cases, 17 expectations)
-----------------------------------------------

Case 1: "I need to work on PA-3467..."
  [/] Output includes markdown table with File, Relevance, Reason columns
  [/] SearchXlsxExportGenerator.java appears with High relevance
  [/] SearchRequestExportGenerator.java appears with High relevance
  [/] At least one test file included
  [/] CalculationType.java appears in the table
  [/] Output contains brief summary section
  Score: 6/6

Case 2: "Hey, I'm picking up PA-3436..."
  [/] Output includes markdown table
  [/] ComparisonType.java appears with High relevance
  [x] ComparisonController appears in table  <- REGRESSION
  [/] CalculationType.java appears
  [/] At least one test file included
  [/] Output contains brief summary
  Score: 5/6

Case 3: "Prepping for PA-3375..."
  [/] Output includes markdown table
  [/] IndexFilesService.java appears with High relevance
  [/] IndexFilesServiceTest.java appears
  [/] pom.xml appears in table
  [/] Output contains brief summary
  Score: 5/5

-----------------------------------------------
Overall: 16/17 expectations passed (94.1%)
Status: [x] FAIL — 1 regression detected

Regression detail:
  Case 2, Expectation 3: "ComparisonController appears in table"
  -> Output mentioned ComparisonService but not ComparisonController
  -> Likely cause: SKILL.md Layer 3 (code navigation) didn't trace
    incoming calls to the controller level
```

This output tells you exactly what to fix in the SKILL.md — and that's the optimization loop kicking in.

### 3.8 Deep Dive: DSPy and Automated Skill Optimization

#### What is DSPy?

**DSPy** (Declarative Self-improving Python) is an open-source framework from Stanford NLP that treats prompt engineering as a **compilation problem** rather than an art form. Instead of hand-crafting prompts, you declare *what* you want (input -> output contract) and DSPy's optimizers automatically search for the best prompt/instructions to achieve it.

**Core idea:** Prompts are parameters. Eval scores are the loss function. Optimization is search.

```
Traditional prompt engineering:     DSPy approach:
                                    
  Human writes prompt               Human declares intent
       v                                 v
  Try it, check output              DSPy generates prompt candidates
       v                                 v
  Tweak wording manually            DSPy evaluates each on your data
       v                                 v
  Repeat (vibes-based)              DSPy picks the best (data-driven)
```

**GitHub:** github.com/stanfordnlp/dspy
**Install:** `pip install dspy-ai`

---

#### How DSPy works internally

DSPy has three core concepts:

**1. Signatures** — Declare the input/output contract (not the prompt):
```python
import dspy

# "Given a context and question, produce an answer"
class QA(dspy.Signature):
    context = dspy.InputField()
    question = dspy.InputField()
    answer = dspy.OutputField()
```

**2. Modules** — Compose signatures into programs:
```python
class MyAgent(dspy.Module):
    def __init__(self):
        self.qa = dspy.Predict(QA)
    
    def forward(self, context, question):
        return self.qa(context=context, question=question)
```

**3. Optimizers (Teleprompters)** — Automatically find the best prompt:

| Optimizer | What it optimizes | How it works |
|-----------|------------------|-------------|
| **BootstrapFewShot** | Few-shot examples | Tries different subsets of examples in the prompt, picks the set that maximizes your eval metric |
| **MIPRO** | Instructions + examples | Rewrites the instruction text itself (e.g., "Summarize" -> "Write a concise summary focusing on key facts"), evaluates each variant |
| **BootstrapFewShotWithRandomSearch** | Few-shot examples | Like BootstrapFewShot but with random search over larger candidate space |
| **COPRO** | Instructions | Coordinates multiple prompt proposals, evaluates, selects |

The optimization loop:
```
for each candidate prompt:
    run the program on all eval cases
    score outputs against eval metric
    track best-scoring prompt
return best prompt
```

---

#### Applying DSPy to skill improvement

Here's where it gets interesting for your meetup. A SKILL.md is
essentially a long instruction prompt. DSPy can optimize it — but
there's a conceptual gap to bridge:

**DSPy operates at the LLM API level** (it sends prompts to an LLM and
evaluates responses), while **a coding agent skill operates at the
harness level** (the agent reads SKILL.md, then executes a multi-step
workflow with tools).

There are three ways to connect them:

##### Approach 1: Optimize the SKILL.md instructions directly

Treat the SKILL.md as a DSPy "instruction" parameter and your eval
JSON as the metric:

```python
import dspy

# The "program" is: give the agent a ticket, get back a file table
class TicketPrepSkill(dspy.Signature):
    """Given a Jira ticket description, identify the most relevant 
    codebase files and output a ranked markdown table."""
    ticket_description = dspy.InputField()
    file_table = dspy.OutputField(desc="Markdown table with File, Relevance, Reason")

class TicketPrepProgram(dspy.Module):
    def __init__(self):
        self.predict = dspy.Predict(TicketPrepSkill)
    
    def forward(self, ticket_description):
        return self.predict(ticket_description=ticket_description)

# Define metric from your eval expectations
def ticket_prep_metric(prediction, example):
    score = 0
    output = prediction.file_table
    for expected_file in example.expected_files:
        if expected_file in output:
            score += 1
    if "| File" in output and "| Relevance" in output:
        score += 1
    return score / (len(example.expected_files) + 1)

# Load your eval cases as DSPy examples
eval_cases = [
    dspy.Example(
        ticket_description="PA-3467: Export search results to XLSX...",
        expected_files=["SearchXlsxExportGenerator.java", 
                       "SearchRequestExportGenerator.java"]
    ).with_inputs("ticket_description"),
]

# Optimize!
from dspy.teleprompt import MIPRO
optimizer = MIPRO(metric=ticket_prep_metric, num_candidates=10)
optimized = optimizer.compile(TicketPrepProgram(), trainset=eval_cases)

# The optimized program now has better instructions
print(optimized.predict.signature.instructions)
```

**What happens:** MIPRO generates 10 different instruction wordings
for the TicketPrepSkill signature, evaluates each against your eval
cases, and returns the best-scoring one. You then take those optimized
instructions and incorporate them into your SKILL.md.

**Limitation:** This optimizes a single LLM call, not the full
multi-step agent workflow (fetching the ticket, searching code,
tracing dependencies). It's useful for optimizing *how the agent
reasons about the ticket*, not the workflow orchestration.

##### Approach 2: Optimize individual steps of the skill

Break your SKILL.md into its constituent steps and optimize each one
independently:

```python
# Step 2 of Ticket Prep: "Analyze the ticket"
class AnalyzeTicket(dspy.Signature):
    """Extract keywords, component names, file references, change type,
    and acceptance criteria from a Jira ticket."""
    ticket_json = dspy.InputField()
    keywords = dspy.OutputField(desc="Domain concepts and technical terms")
    components = dspy.OutputField(desc="Module, service, or class names mentioned")
    change_type = dspy.OutputField(desc="bug fix, feature, or refactor")

# Step 3 of Ticket Prep: "Decide search strategy"  
class PlanSearch(dspy.Signature):
    """Given extracted ticket concepts and a project structure overview,
    produce a search plan: which grep patterns to try, which directories
    to explore, which code navigation steps to take."""
    keywords = dspy.InputField()
    components = dspy.InputField()
    project_structure = dspy.InputField()
    search_plan = dspy.OutputField(desc="Ordered list of search actions")
```

Optimize each step with its own metric. This gives you fine-grained
control: maybe Step 2 is already great but Step 3 needs work.

##### Approach 3: Use DSPy as an offline skill-improvement tool

Instead of integrating DSPy into the agent's runtime, use it as a
**development-time tool** to find better instructions:

1. Take your SKILL.md
2. Extract the key instruction paragraphs
3. Run MIPRO/COPRO to find better phrasings
4. Manually review the suggestions and update SKILL.md
5. Run your regular evals to confirm improvement

This is the most pragmatic approach — it uses DSPy as a "prompt
optimizer" that you consult periodically, not as a runtime dependency.

---

#### DSPy vs. agent-assisted optimization

| Aspect | DSPy optimization | Agent-assisted ("optimize yourself") |
|--------|-------------------|--------------------------------------|
| **How it works** | Systematic search over prompt space with scored candidates | Agent reads failing evals, reasons about fixes, edits SKILL.md |
| **Strengths** | Exhaustive, data-driven, reproducible | Understands multi-step workflows, can fix orchestration logic |
| **Weaknesses** | Optimizes single LLM calls, not tool-use workflows | Non-deterministic, may introduce new regressions |
| **Best for** | Optimizing reasoning/analysis instructions | Fixing workflow bugs (missing search patterns, wrong tool use) |
| **Cost** | Many LLM calls per optimization run (10-100x eval cases x candidates) | One agent session per optimization attempt |
| **Setup** | Requires Python wrapper, DSPy install, metric function | Zero setup — just ask the agent |

**Recommendation for your workshop:** Start with agent-assisted optimization (zero setup, immediately accessible). Mention DSPy as the "graduate to this when you're serious about systematic improvement" option. The key insight is:

> **Agent-assisted = the agent is both the optimizer and the optimized (fast, intuitive, but fuzzy)**
> **DSPy = a separate optimizer systematically improves the agent's instructions (slower, rigorous, data-driven)**

---

#### Practical limitations of DSPy for skill optimization

1. **Multi-step gap:** DSPy optimizes LLM calls, not tool-using
   workflows. A skill that runs `grep`, reads files, and calls APIs
   has behavior that depends on *tool outputs*, not just prompt
   wording. DSPy can't optimize "run grep with a better pattern" — it
   can only optimize "given these grep results, reason better about
   them."

2. **Cost:** Each optimization run makes `num_candidates x
   num_eval_cases` LLM calls. With 10 candidates and 20 eval cases,
   that's 200 API calls per optimization round. Fine for offline
   improvement; too expensive for continuous optimization.

3. **Black-box instructions:** DSPy-optimized instructions can be
   opaque. MIPRO might produce "Given the ticket metadata and codebase
   structure, systematically identify files by cross-referencing
   acceptance criteria with module boundaries" — which is
   better-scoring but less readable than your hand-written
   instructions. You may need to manually blend DSPy suggestions with
   human-readable prose.

4. **Eval quality bottleneck:** DSPy is only as good as your
   metric. If your eval expectations are too loose, DSPy will find
   prompts that game the metric without genuinely improving
   quality. Garbage evals in -> garbage optimization out.

---

#### References

- Stanford NLP: github.com/stanfordnlp/dspy
- DSPy paper: "DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines" (Khattab et al., 2023)
- MIPRO paper: "Optimizing Instructions and Demonstrations for Multi-Stage Language Model Programs" (Opsahl-Ong et al., 2024)
- Practical guide: dspy-docs.vercel.app

### 3.9 Tips for writing good expectations

1. **Be specific but not brittle** — Good "contains a table with File
   column" FAIL "the third line starts with |"
2. **Test behavior, not wording** — GOOD "mentions the risk of shared
   utilities" FAIL "says exactly 'this touches a shared utility'"
3. **Include negative cases** — "does NOT recommend files from
   unrelated modules"
4. **Cover edge cases** — what happens with a vague ticket? An empty
   codebase? A ticket with no description?
5. **Grade on a rubric** — partial credit matters. 4/6 expectations
   passing is useful signal, not a "fail."
6. **Write evals first** — just like TDD, writing expectations before
   the skill forces you to think about what "good" looks like.

---

## Part 4: Operationalizing Agents with GitHub Agentic Workflows

### 4.1 What are GitHub Agentic Workflows?

GitHub Agentic Workflows (GAW) is a framework by GitHub Next and
Microsoft Research that lets you run coding agents (Copilot, Claude,
Codex) **inside GitHub Actions** — triggered by events (issue opened,
PR created, schedule) or manually. Workflows are defined in **simple
markdown files** with natural language instructions, then compiled to
GitHub Actions YAML.

**The key idea:** Move agents from interactive CLI sessions into
**automated, event-driven pipelines** with built-in security
guardrails. This is how you go from "I run an agent on my laptop" to
"agents continuously improve my repository."

**Sources:**
- github.github.com/gh-aw/
- blog.frankel.ch/agentic-github-workflows/

---

### 4.2 How it works

```
+------------------------------------------------------------------+
|  1. AUTHOR: Write a markdown workflow (.md)                      |
|     - Natural language instructions                              |
|     - Permissions (read-only for agent)                          |
|     - Safe output declarations (what the agent may create)       |
|                                                                  |
|  2. COMPILE: gh aw compile                                       |
|     - Markdown -> GitHub Actions YAML (.lock.yml)                 |
|     - Schema validation, expression safety, SHA pinning          |
|     - Security scanning (actionlint, zizmor, poutine)            |
|                                                                  |
|  3. TRIGGER: GitHub event or schedule fires the workflow         |
|     - Issue opened, PR created, comment posted, daily cron, etc. |
|                                                                  |
|  4. EXECUTE: Agent runs in isolated container                    |
|     - Read-only GitHub token (cannot push, delete, merge)        |
|     - Network firewall (domain allowlist, egress proxy)          |
|     - Zero secrets in the agent process                          |
|     - Agent produces structured artifact (not direct writes)     |
|                                                                  |
|  5. REVIEW: Threat detection scans the artifact                  |
|     - AI-powered scan for prompt injection, leaked creds,        |
|       malicious code patterns                                    |
|     - If suspicious -> workflow fails, nothing written            |
|                                                                  |
|  6. APPLY: Separate write job (scoped permissions) applies output|
|     - Creates issue, opens PR, adds comment, adds labels         |
|     - Hard limits enforced (e.g., max 1 issue per run)           |
|     - Title prefixes, label constraints                          |
+------------------------------------------------------------------+
```

---

### 4.3 Example: Daily Status Report

A complete workflow in markdown:

```markdown
---
on:
  schedule: daily
permissions:
  contents: read
  issues: read
  pull-requests: read
safe-outputs:
  create-issue:
    title-prefix: "[team-status] "
    labels: [report, daily-status]
    close-older-issues: true
---

## Daily Issues Report

Create an upbeat daily status report for the team as a GitHub issue.

## What to include
- Recent repository activity (issues, PRs, discussions, releases, code changes)
- Progress tracking, goal reminders and highlights
- Project status and recommendations
- Actionable next steps for maintainers
```

That's it. The agent reads the repo, analyzes activity, and creates an issue. The `safe-outputs` block constrains what it can do (one issue, specific prefix, specific labels).

---

### 4.4 The five security layers

GAW uses defense-in-depth to ensure a compromised or confused agent can't do damage:

| Layer | What it does | What it prevents |
|-------|-------------|-----------------|
| **1. Read-only token** | Agent's GitHub token has only read permissions | Agent can't push code, delete branches, merge PRs |
| **2. Zero secrets** | Agent process never receives write tokens, API keys, or credentials | Compromised agent has nothing to steal |
| **3. Container + network firewall** | Agent runs in isolated container; all outbound traffic goes through Squid proxy with domain allowlist | Data exfiltration, calling unexpected servers |
| **4. Safe outputs** | Agent writes to a structured artifact, not directly to GitHub. A separate gated job applies permitted actions with hard limits | Agent can't create 1000 issues or push arbitrary code |
| **5. Threat detection** | AI-powered scan of agent's proposed output before it's applied — checks for prompt injection, leaked credentials, malicious patterns | Subtle attacks that pass structural checks |

---

### 4.5 Real-world use case: Parsing release notes (from Frankel's blog)

Nicolas Fränkel describes a compelling real-world case:

**Problem:** A colleague manually reads release notes for each product version to identify deprecations, breaking changes, and removed plugins. This is tedious, error-prone, and doesn't scale across versions.

**Why deterministic automation fails:** Release notes are semi-structured prose, not machine-readable data. Regex and structured parsing can't reliably extract deprecation information from natural language.

**Why an agentic workflow fits:** An LLM agent can *understand* the release notes, extract structured information, and produce consistent output — exactly the sweet spot for agents.

**The workflow:** On trigger, the agent reads the release notes, extracts deprecation data, and creates a PR updating the configuration files. The documentation workflow similarly creates PRs to update README, wiki, Copilot instructions, and changelog whenever relevant code changes.

**Lessons learned (from Frankel):**
1. You edit the `.md` file but GitHub runs the compiled `.yml` — don't forget to compile (`gh aw compile`)
2. You can't auto-compile in a workflow (security implications) — use a CI check that fails if compiled output is stale
3. GitHub Marketplace actions aren't available inside agentic workflows — you need to reimplement basics
4. Line endings matter (Windows vs Ubuntu runners) — use `.gitattributes`

---

### 4.6 How this connects to skills and evals

GitHub Agentic Workflows are the **operationalization layer** for the skills you build:

| Development phase | Where it happens | What you use |
|------------------|-----------------|-------------|
| **Build the skill** | Local, interactive (Claude Code / Copilot CLI) | SKILL.md, scripts, manual testing |
| **Test the skill** | Local or CI | Eval JSON, LLM-as-judge, string matching |
| **Operationalize the skill** | GitHub Agentic Workflows | Markdown workflow, scheduled/event triggers, safe outputs |
| **Monitor the skill** | GitHub Actions logs, threat detection | Workflow run history, artifact inspection |

**The progression:**
1. You write a "Code Reviewer" skill and test it interactively
2. You write evals and gate on them
3. You wrap it in a GAW workflow: "On every PR, run the code reviewer agent and post review comments"
4. The security layers ensure the agent can only *read* the PR and *propose* comments — a human or the safe-outputs gate decides what actually gets posted

---

### 4.7 Getting started

```bash
# Install the gh aw extension
gh extension install github/gh-aw

# Initialize in your repo
gh aw init

# Add a sample workflow
gh aw sample daily-report

# Compile markdown to Actions YAML
gh aw compile

# Trigger a manual run
gh workflow run <workflow-name>
```

**Requirements:**
- GitHub fine-grained token with *Copilot requests* permission
- GitHub Actions enabled on the repo
- The `GITHUB_COPILOT_TOKEN` secret set in the repo

---

### 4.8 Relevance for the meetup

GAW is a perfect "next step" to show participants after they've built
a skill:

> "You just built a skill that works in your terminal. Now imagine it runs every morning at 8am, reviews yesterday's PRs, and posts a summary issue — with guardrails that prevent it from doing anything you didn't explicitly allow."

It bridges the gap between **"cool demo"** and **"production
automation"**, and the security architecture is a great discussion
point: how do you trust an agent to act on your repo?

**Possible demo:** Show the daily status report workflow running on a
real repo — from markdown definition through compiled YAML to the
resulting issue.

---

### 4.9 APM: Dependency Management for AI Agents

If GitHub Agentic Workflows is *how you run* agents in production,
**APM** (Agent Package Manager) is *how you distribute and govern*
their configuration. Created by Microsoft, APM is the `package.json` /
`requirements.txt` for AI agent setups.

**Sources:**
- microsoft.github.io/apm/
- github.com/microsoft/apm

#### The problem APM solves

Today, every developer configures their coding agent
differently. Skills, instructions, prompts, plugins, MCP servers — all
set up manually, per machine, per project. Nothing is:
- **Portable** — "works on my machine" but not yours
- **Reproducible** — no lockfile, no version pinning
- **Governed** — no way for a security team to control what agents can use

APM fixes all three with a single manifest file.

#### How it works

```yaml
# apm.yml — ships with your project (like package.json)
name: your-project
version: 1.0.0
dependencies:
  apm:
    # Skills from any GitHub repository
    - anthropics/skills/skills/frontend-design
    - microsoft/GitHub-Copilot-for-Azure/plugin/skills/azure-compliance
    # A full package with rules, skills, prompts, hooks...
    - microsoft/apm-sample-package#v1.0.0
    # Plugins
    - github/awesome-copilot/plugins/context-engineering#v2.1
    # Agents
    - github/awesome-copilot/agents/api-architect.agent.md
    # From GitLab, Azure DevOps, any git host — with version pinning
    - git: https://gitlab.com/acme/coding-standards.git
      path: instructions/security
      ref: v2.0
  mcp:
    # MCP servers — installed into every detected client
    - name: io.github.github/github-mcp-server
      transport: http
```

New developer joins the team:
```bash
git clone <org/repo> && cd <repo> && apm install
```

**That's it.** Copilot, Claude Code, Cursor, OpenCode, Codex, Gemini —
every agent harness is configured with the right context and
capabilities.

#### The three promises

| Promise | What it means | How it works |
|---------|-------------|-------------|
| **Portable by manifest** | One `apm.yml` declares everything; `apm install` reproduces it everywhere | Transitive dependency resolution like npm/pip. `apm.lock.yaml` pins exact versions + integrity hashes. Works across Copilot, Claude, Cursor, Codex, Gemini. Install from GitHub, GitLab, Bitbucket, Azure DevOps, any git host. |
| **Secure by default** | Agent context is executable — a prompt is a program for an LLM. APM treats it that way. | `apm install` scans for hidden Unicode and tampering before agents read packages. Lockfile records content hashes for full provenance. Transitive MCP servers require explicit consent (trust boundary). `apm audit` reports the full chain of trust. |
| **Governed by policy** | Security teams define what's allowed; every `apm install` enforces it | `apm-policy.yml` allow-lists sources, scopes, and primitive types. Tighten-only inheritance: enterprise -> org -> repo. Published bypass contract for exceptions. `apm audit --ci` wires into GitHub branch protection rulesets. |

#### What APM can manage

APM handles all agent primitives in a single manifest:

| Primitive | Description | Example |
|-----------|------------|---------|
| **Skills** | SKILL.md files with instructions and scripts | `anthropics/skills/skills/frontend-design` |
| **Instructions** | AGENTS.md / CLAUDE.md / copilot-instructions.md | `acme/coding-standards/instructions/security` |
| **Prompts** | Reusable prompt templates | `acme/prompts/review.prompt.md` |
| **Agents** | Full agent configurations | `github/awesome-copilot/agents/api-architect.agent.md` |
| **Hooks** | Event-driven automation scripts | Lifecycle hooks (pre-tool, post-tool, etc.) |
| **Plugins** | Agent plugins (e.g., Copilot plugin.json) | `github/awesome-copilot/plugins/context-engineering` |
| **MCP Servers** | Model Context Protocol servers | `io.github.github/github-mcp-server` |

#### APM + agentrc

APM also integrates with **agentrc** (github.com/microsoft/agentrc), a
tool that analyzes your codebase and generates tailored agent
instructions — architecture, conventions, build commands — from real
code, not templates. Use agentrc to author high-quality instructions,
then package them with APM to share across your org.

#### Getting started

```bash
# Install (macOS/Linux)
curl -sSL https://aka.ms/apm-unix | sh

# Or via Homebrew
brew install microsoft/apm/apm

# Add packages to your project
apm install microsoft/apm-sample-package#v1.0.0

# Add an MCP server (wired into all detected agent clients)
apm install --mcp io.github.github/github-mcp-server --transport http

# Audit for security issues
apm audit

# CI/CD gate
apm audit --ci
```

#### How GAW and APM complement each other

| Concern | GitHub Agentic Workflows | APM |
|---------|-------------------------|-----|
| **What it does** | Runs agents in production (CI/CD) | Manages agent configuration (dependencies) |
| **Analogy** | GitHub Actions (the runner) | npm/pip (the package manager) |
| **Scope** | One repo's automation workflows | Any repo's agent setup |
| **Security model** | Runtime: sandboxing, firewalls, safe outputs | Supply chain: scanning, lockfiles, policies |
| **Governance** | Per-workflow permissions and safe-output limits | Org-wide policy enforcement (`apm-policy.yml`) |

**Together they form the full operationalization stack:**
1. **APM** declares what skills, instructions, and MCP servers your
   project needs — pinned, scanned, governed
2. **GAW** runs those skills as automated workflows — sandboxed,
   firewalled, gated

Or in the kitchen analogy:

> APM is the **pantry management system** — it ensures every kitchen has the same approved ingredients, sourced from trusted suppliers, at the right versions. GAW is the **kitchen schedule** — it ensures the chef (agent) cooks at the right time, with guardrails that prevent fires.

---

### 4.10 Claude Plugins: Packaging and Distributing Agent Capabilities

If GAW is how you *run* agents in CI/CD and APM is how you *manage
dependencies* across agents, **Claude Plugins** are how you *package
and distribute* capabilities specifically within the Claude Code
ecosystem.

**Source:** code.claude.com/docs/en/plugins

#### What is a Claude Plugin?

A plugin is a self-contained directory that bundles skills, agents,
hooks, MCP servers, LSP servers, monitors, and settings into a single
distributable unit. It gets a **namespace** (e.g.,
`/ticket-prep:analyze`) so it can't conflict with other plugins or
project-level skills.

```
my-plugin/
|-- .claude-plugin/
|   |-- plugin.json          # Manifest: name, description, version, author
|-- skills/
|   |-- code-review/
|       |-- SKILL.md          # Skills the plugin provides
|-- agents/                   # Custom sub-agent definitions
|-- hooks/
|   |-- hooks.json            # Event-driven automation
|-- monitors/
|   |-- monitors.json         # Background watchers (tail logs, watch files)
|-- .mcp.json                 # MCP server configurations
|-- .lsp.json                 # LSP server configurations
|-- bin/                      # Executables added to PATH
|-- settings.json             # Default settings when plugin is active
|-- README.md
```

#### The plugin manifest

```json
{
  "name": "ticket-prep",
  "description": "Prepare codebase context from a Jira ticket",
  "version": "1.0.0",
  "author": {
    "name": "Joris Gillis"
  }
}
```

| Field | Purpose |
|-------|---------|
| `name` | Unique identifier and skill namespace. Skills are prefixed: `/ticket-prep:analyze` |
| `description` | Shown in the plugin manager when browsing/installing |
| `version` | If set, users only get updates when you bump this. If omitted, every git commit counts as a new version |
| `author` | Attribution |

#### Standalone skills vs plugins

| Aspect | Standalone (`.claude/`) | Plugin |
|--------|------------------------|--------|
| **Skill names** | `/hello` | `/plugin-name:hello` (namespaced, no conflicts) |
| **Scope** | One project | Shareable across projects, teams, community |
| **Distribution** | Copy files manually | Install via marketplace (`/plugin install`) |
| **Versioning** | Git history | Explicit version field or commit SHA |
| **Best for** | Personal workflows, quick experiments | Team standards, community distribution, reusable packages |

**Rule of thumb:** Start with standalone skills in `.claude/skills/`. When a skill proves useful and needs sharing, promote it to a plugin.

#### What a plugin can contain

| Component | Location | Purpose |
|-----------|---------|---------|
| **Skills** | `skills/<name>/SKILL.md` | Extend Claude with domain-specific workflows |
| **Agents** | `agents/` | Custom sub-agent definitions (system prompts, tool restrictions, model overrides) |
| **Hooks** | `hooks/hooks.json` | Event handlers: PreToolUse, PostToolUse, session lifecycle |
| **MCP Servers** | `.mcp.json` | External tool integrations via Model Context Protocol |
| **LSP Servers** | `.lsp.json` | Language server configs for code intelligence |
| **Monitors** | `monitors/monitors.json` | Background watchers that notify Claude on events (e.g., `tail -F ./logs/error.log`) |
| **Executables** | `bin/` | Scripts/binaries added to PATH while plugin is active |
| **Settings** | `settings.json` | Default config (e.g., activate a custom agent as the main thread) |

#### Distribution: Marketplaces

Plugins are distributed through **marketplaces** — curated lists of plugins hosted in git repositories:

```bash
# Install from the official Anthropic marketplace
/plugin install ticket-prep

# Install from a team/private marketplace
/plugin install ticket-prep@my-team-marketplace

# Or via CLI
claude --plugin-dir ./my-plugin   # local testing
```

**Marketplace types:**
- **Official Anthropic marketplace** — submit via claude.ai/settings/plugins/submit
- **Team/org marketplace** — a private git repo with a plugin index (great for internal standards)
- **Community marketplaces** — third-party curated collections

**Also installable via `npx skills`** (the cross-agent CLI by Vercel):
```bash
npx skills add anthropics/skills/skills/frontend-design
# or with APM:
apm install anthropics/skills/skills/frontend-design
```

#### Development workflow

```bash
# 1. Create plugin structure
mkdir -p my-plugin/.claude-plugin my-plugin/skills/review

# 2. Write manifest
cat > my-plugin/.claude-plugin/plugin.json << 'EOF'
{
  "name": "my-plugin",
  "description": "Code review with team standards",
  "version": "1.0.0"
}
EOF

# 3. Write a skill
cat > my-plugin/skills/review/SKILL.md << 'EOF'
---
description: Review code against team coding standards
---
Review the code for...
EOF

# 4. Test locally (loads without installing)
claude --plugin-dir ./my-plugin

# 5. In-session: reload after edits
/reload-plugins

# 6. Test your skill
/my-plugin:review
```

#### Migrating from standalone to plugin

If you already have skills in `.claude/skills/` that you want to share:

| Standalone | Plugin equivalent |
|-----------|------------------|
| `.claude/skills/review/SKILL.md` | `my-plugin/skills/review/SKILL.md` |
| `.claude/commands/deploy.md` | `my-plugin/commands/deploy.md` |
| Hooks in `.claude/settings.json` | `my-plugin/hooks/hooks.json` |
| MCP in `.claude/settings.json` | `my-plugin/.mcp.json` |

Add a `.claude-plugin/plugin.json` manifest and you're done.

#### How plugins fit in the operationalization stack

| Layer | Tool | What it does |
|-------|------|-------------|
| **Package** | **Claude Plugins** | Bundle skills, agents, hooks, MCP servers into a namespaced, distributable unit |
| **Distribute** | **Plugin Marketplaces** / **APM** | Share across teams and projects; install in one command |
| **Govern** | **APM policies** / **Managed settings** | Control which plugins are allowed org-wide |
| **Run** | **GitHub Agentic Workflows** | Execute plugins in automated, sandboxed CI/CD pipelines |

Or continuing the kitchen analogy:

> A plugin is a **boxed meal kit** — it comes with the recipe (skill), the special utensils (scripts/bin), the appliance settings (MCP/LSP config), and the timer instructions (hooks/monitors). You install the kit in your kitchen (project), and the chef (agent) knows how to use everything inside it.

---

## Part 5: Suggested Session Structure

| Block | Duration | Content |
|-------|----------|---------|
| **Intro** | 15 min | Terminology walkthrough with kitchen analogy. Show anatomy of a skill (SKILL.md, scripts, evals). |
| **Demo** | 10 min | Live demo of Ticket Prep — show end-to-end: trigger -> fetch -> analyze -> output. Show an eval run. |
| **Hands-on** | 60-90 min | Participants pick their level: |
| | | **Level A:** Extend a worked-out skill (add feature to Code Reviewer, Release Notes Drafter, or Refactor Radar) |
| | | **Level B:** Build a skill from an idea + eval scaffold (pick from: Journal Buddy, PR Review, Dep Scout, Test Gap Finder, Context Switcher) |
| | | **Level C:** Free-form (bring your own idea, or pick: Onboarding Guide, Incident Postmortem, Commit Ghostwriter) |
| **Eval writing** | included in hands-on | Every participant writes at least 2-3 eval cases for their skill |
| **Show & tell** | 15 min | 2-3 participants demo what they built + their evals |

---

## References

### Terminology & Architecture
- modelcontextprotocol.io — MCP specification
- martinfowler.com/articles/harness-engineering.html — Harness engineering
- anthropic.com/engineering/harness-design-long-running-apps — Harness design
- langchain.com/blog/the-anatomy-of-an-agent-harness — Harness anatomy
- addyosmani.com/blog/code-agent-orchestra/ — Multi-agent orchestration
- morphllm.com/agent-engineering — Agent engineering patterns
- arxiv.org/abs/2505.10468 — AI Agents vs Agentic AI taxonomy
- arxiv.org/abs/2604.25850 — Observability-driven harness engineering

### Eval Frameworks
- promptfoo.dev — Promptfoo
- docs.confident-ai.com — DeepEval
- braintrust.dev — Braintrust
- docs.ragas.io — Ragas
- smith.langchain.com — LangSmith
- inspect.ai-safety-institute.org.uk — Inspect AI

### Coding Agent Docs
- code.claude.com/docs — Claude Code documentation
- code.claude.com/docs/en/plugins — Claude Plugins guide
- code.claude.com/docs/en/skills — Claude Skills guide
- code.claude.com/docs/en/discover-plugins — Plugin discovery & marketplaces
- code.claude.com/docs/en/plugins-reference — Full plugin technical reference
- docs.github.com/en/copilot — GitHub Copilot documentation
- refactix.com/claude-code-power-user-guide — Claude Code skills, hooks, subagents guide
- agentskills.io — Agent Skills open standard (originally by Anthropic)

### GitHub Agentic Workflows
- github.github.com/gh-aw/ — Official documentation & architecture
- github.github.com/gh-aw/introduction/architecture/ — Security architecture deep dive
- blog.frankel.ch/agentic-github-workflows/ — Real-world use case & lessons learned
- githubnext.com/projects/continuous-ai — Continuous AI concept (GitHub Next)

### APM (Agent Package Manager)
- microsoft.github.io/apm/ — Official documentation
- github.com/microsoft/apm — Source code & roadmap
- github.com/microsoft/agentrc — Agent instruction generator (companion tool)
- agentskills.io — Agent Skills standard
- agents.md — AGENTS.md standard
