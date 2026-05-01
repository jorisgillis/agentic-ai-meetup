# Agentic AI Meetup @ Corda

Repository with my sources, slides, and exercises for a hands-on
session during the first edition of the Agentic AI Meetup @ Corda.

## Exercises

### Code Reviewer

	A Pythonic Code Reviewer, that is well-aware of the PEP8 Python Style
	Guide. 
	
This skill will review a Python code base and make sure that the code
is good from a general software engineering standpoint and is
idiomatic Python.

#### Extension Ideas

- Different programming language
- Turn into a subagent

### Commit Ghostwriter

	A good commit message is all about the "why" of a change. 
	The what is captured by the code changes. But why did you 
	choose a specific algorithm, architecture or path? And why
	did we need this change in the software? 
	
Writing a good commit message is hard. This Ghostwriter will suggest
commit messages that focus on the why of a change.

#### Extension Ideas

- Adopt to your personal/company's git commit message style
- Add a hook that verifies the commit message when a git commit is
  triggered by the coding agent.

### Journal Buddy

	Standup time! What did I do yesterday? 
	If you spend a lot of time in Claude Code and recognize yourself
	in this standup scenario, then Journal Buddy can help. Whenever
	you want you can check in with Journal Buddy and tell him what
	you are doing. 
	Tomorrow you simply ask Journal Buddy for a summary of your day.

#### Extension Ideas

- Add a hook to trigger Journal Buddy on the end of a session, or when
  a git commit is issued.
- Extend the question set of Journal Buddy.
- Let Journal Buddy generate a dashboard of your worklog.

### Ticket Prep

	Based on a ticket number, reads the ticket from Jira and finds a list 
	of files that probably need editing to complete the ticket.

Both an agent and a skill. I've started out with a skill (using the
[skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)
skill). Used evals to improve the skill and then turned it into an
agent.

The benefit of the agent is that it has its own context, hence, it can
search through a codebase as much as it likes, and returns (normally)
a relatively small table with files that will likely be touched. Thus,
not polluting the main context of the coding agent.

This agent also has a script to communicate with Jira. This is to keep
the scope minimal. Obviously a Jira MCP would also work here, and be
more reusable in the coding agent.

## Slides

The slides used during the meetup.

## Research Output

A Markdown containing research from Claude, directed by me on the
topics discussed during the meetup.


