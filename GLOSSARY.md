# Comprehension metrics

Measuring how much a human engaged with and oversaw a coding agent's work, read from human-agent transcripts.

## Language

**Session**:
One transcript of a human working with a coding agent.
_Avoid_: Conversation, run, trajectory

**Episode**:
A span within a session that starts when the agent delivers something the human could review and ends at the next human turn that moves on.

**Pilot sample**:
The single set of 50 sessions on which the labeling codebook, the episode segmentation rule and the judge model are all chosen; its labeled episodes are drawn from these sessions.
_Avoid_: Pilot set, labeling pilot, judge pilot

**Transluce replication**:
Re-running Transluce's published overselling rubric on the SWE-chat sessions they analyzed, to show this project's setup reproduces their results before it measures anything new.
_Avoid_: Reward hacking replication, misalignment replication
