# Comprehension metrics

Measuring how much a human engaged with and oversaw a coding agent's work, read from human-agent transcripts.

## Language

**Session**:
One transcript of a human working with a coding agent.
_Avoid_: Conversation, run, trajectory

**Agent product**:
The coding tool a human works with in a session, such as Claude Code.
_Avoid_: Agent (on its own), harness, CLI

**Model**:
The LLM behind an agent product in a session; one session can involve several models.
_Avoid_: Agent (on its own)

**Episode**:
A span within a session that starts when the agent delivers something the human could review and ends at the next human turn that moves on.

**Study population**:
Every Claude Code session in the pinned, recent SWE-chat snapshot that has at least one human turn after the first agent action.
_Avoid_: Dataset, corpus

**Pilot sample**:
The single set of 50 sessions on which the labeling codebook, the episode segmentation rule and the judge model are all chosen; its labeled episodes are drawn from these sessions.
_Avoid_: Pilot set, labeling pilot, judge pilot

**Transluce replication**:
Re-running Transluce's published overselling rubric on the Claude Code sessions they analyzed, to show this project's setup reproduces their results before it measures the study population.
_Avoid_: Reward hacking replication, misalignment replication
