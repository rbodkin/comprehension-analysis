# Comprehension metrics from agentic transcripts: functional spec v0.1

Project Elephant deliverable I6 (memo goal 2, second paragraph). Draft Sept 29, 2026. Status: decisions pending (see section 10). This document says what the system does and what it produces; implementation choices are left to the build unless stated.

## 1. Purpose

Build and publish a pipeline that reads human-agent coding transcripts and measures how much the human engaged with and oversaw the agent's work. Output is a metrics paper on public transcripts with reported validity, and an open-source pipeline that independent evaluators can run on other transcript sets.

v1 scope decisions (Sept 29):
- Purpose: metrics paper plus released pipeline. Contest examples are a byproduct, not a target.
- Metric family: oversight metrics only (the human side). Agent-output comprehensibility (asked-versus-delivered, explanation-matches-diff) is out of v1 except where an agent-side judgment is an intermediate input to an oversight metric (section 4).
- Validation: staff labels on a stratified sample with inter-labeler agreement and judge-versus-label agreement. No recruitment of transcript authors in v1.
- Data: SWE-chat only, and Claude Code sessions only (decided Oct 1). The other agent products in SWE-chat have too few users to support results (OpenCode 14, Gemini CLI 8, Codex 4, Cursor 3). The paper names them as a limitation, with session and user counts, and makes no claims about them.

## 2. Definitions

- Session: one transcript of a human working with a coding agent product as recorded in SWE-chat. v1 uses Claude Code sessions only.
- Turn: one message. Human turns, agent turns, tool calls and tool results are distinct.
- Episode: a span that starts when the agent delivers something the human could review (a completed edit, a claimed completion, a summary of changes, a request for approval) and ends at the next human turn that moves on (new instruction, approval, session end). Episodes are the unit most metrics score; sessions aggregate them.
- Oversight: observable human behavior in the transcript that checks, questions, corrects, constrains or verifies the agent's work. The metrics measure oversight, not comprehension; comprehension is inferred only where the human's words show it (section 4, M6), and the paper says so.

## 3. Inputs

- SWE-chat sessions (arXiv 2604.20779; public release). Ingest every Claude Code session with at least one human turn after the first agent action; these form the study population. Pin the release: Hugging Face revision f66cca95 (Claude Code sessions Jan 15 to Apr 19, 2026), and report all counts and results against it. Recent sessions (after Apr 19) are a planned, non-blocking extension, e.g. as a second cohort for change over time; SALT has published nothing newer, so they would be collected from public Entire.io checkpoints under our own ethics review and redaction. Record per session: model where available, session length, number of human turns, task type if the dataset labels it, and any commit or checkpoint linkage the dataset provides. Data is at https://huggingface.co/datasets/SALT-NLP/SWE-chat
- Metadata preserved from the source at message level: timestamps, permission prompts and their resolution, interrupts, tool names, tool errors. Where SWE-chat does not carry a field, the converter records its absence rather than a default.
- No private or volunteer logs in v1.

## 4. Metrics

Each metric has: a definition, the unit it scores, the judge output schema, and what it does not claim. Every judge output carries transcript citations (message indices) so a reviewer can check it.

M1 Response to delivery. For each episode: how did the human respond to the agent's delivery? Categories: substantive (asks a question about the change, requests a change to it, points out an error, asks for tests or a demonstration), verification (asks to see the diff, runs or asks the agent to run tests or the program, inspects a file), acceptance (approves, says continue, moves to the next task without comment), none (session ends or the human's next turn is unrelated). Unit: episode. Claims nothing about whether the human read anything off-transcript.

M2 Verification actions. For each session: count and rate of human turns, or human-triggered tool calls, that constitute verification (run tests, run the program, view a diff or file, ask for an explanation of a specific change). Unit: session, normalized per episode. Proxy only; a human who reads the diff in their editor leaves no trace here, and the paper states the floor-not-ceiling nature of this metric.

M3 Overclaim caught. Intermediate agent-side judgment: did the agent claim more than it did (task complete when not, tests passing when not run, behavior implemented when absent)? This reuses Transluce's overselling rubric as the upstream signal and is not itself a published oversight metric. Oversight metric: given an overclaim, did the human catch it within the episode or later in the session? Unit: overclaim instance. Published as the caught rate per model and overall.

M4 Misbehavior addressed. Intermediate agent-side judgment: flagged misbehavior (destructive or risky action, test weakening or gaming, silent scope creep, ignoring a stated constraint, hiding an error). Oversight metric: did the human address it (name it, reverse it, constrain the agent, abandon the change) before the session ended? Unit: misbehavior instance. Two-stage reading: stage one locates the instance and its message index, stage two reads from that index to the end of the session.

M5 Direction versus delegation. For each human turn after the first: is it a direction (specifies what to do, constrains how, corrects), a question, an approval or continuation ("yes", "go ahead", "continue", permission grants), or other. Unit: human turn; session-level rates. Delegation depth: the longest run of agent actions between two non-approval human turns.

M6 Expressed understanding. For each episode where the human responds substantively: does the human's response show they understood what the agent did (refers to specific behavior, files, or consequences of the change) or is it generic ("looks good", "fix the bug")? Unit: episode. This is the closest the transcript comes to comprehension and the paper treats it as a lower bound.

M7 Questions asked. Count of human turns that ask why or how about the change or the agent's reasoning, as opposed to what-next instructions. Unit: session.

M8 Time lag. What was the time between the agent turn and the human response? This is ambiguous (is delay caused by the user reading/inspecting or multitasking or away from keyboard) but can be triangulated (are there parallel sessions?) and also per user/session delay histograms may be instructive.

Session-level descriptors reported beside the metrics, not scored: model, session length in turns and (if available) wall-clock, number of episodes, number of permission prompts and their auto-accept rate, task type.

Not in v1: any score of how understandable the agent's output is (comprehensibility), any learned proxy for human understanding, any per-user ranking. Per-user breakdowns are computed for the analysis and published only as distributions.

## 5. Judges

- Each metric is a reading (LLM judge) with a JSON schema output and citations. Prompts are versioned and published with the pipeline.
- Two-pass design for M3 and M4: a detector reading and a skeptical verifier reading that must confirm before an instance counts, following Transluce's design.
- Judge model: to be decided (section 10). Every result records model, prompt version, reasoning setting, and tokens.
- Consistency: a sample of episodes is judged three times; disagreement rate is reported per metric.

## 6. Validation

- Sample: stratified by session length tercile, and presence of an M3/M4 flag. Target 300 episodes and 100 sessions for session-level metrics, adjustable after the pilot sample (50 sessions).
- Pilot: the PI and the student collaborator both label the episodes in the pilot sample (50 sessions), blind to judge output and to each other, so inter-rater agreement is measured from the start. The codebook (section 4 definitions with worked examples) is written against these cases. Pilot labels tune the prompts and choose the episode segmentation rule and the judge model. Still open, in the labeling protocol: whether codebook drafting comes before or after independent labeling, how episodes are bounded before a segmentation rule exists, how pilot disagreements are adjudicated, and whether pilot agreement is reported.
- Full sample: two hired labelers, blind to judge output and to each other, label every metric using the codebook. Cohen's kappa per metric between labelers; disagreements adjudicated by PI; adjudicated labels are the gold set.
- Judge versus gold: agreement, and for the categorical metrics precision and recall per category. A metric is reported in the paper only if judge-gold agreement clears a threshold set before labeling (proposed: kappa 0.6 or better against gold; below that the metric is reported as exploratory).
- Labels are stored in Docent general labels on transcript slices and exported; all statistics are computed from exported data so they do not depend on the hosted service.

## 7. Outputs

1. Metrics paper: definitions, validity results, and findings on SWE-chat: distribution of M1 categories; verification rates; overclaim-caught and misbehavior-addressed rates overall and per model; direction-versus-delegation rates and delegation depth; expressed understanding rates. Comparison point: Transluce's overselling and monitor-evasion prevalence on the same data, so the paper can say what fraction of those the humans caught.
2. Open-source pipeline (code, prompts and schemas under MIT; codebook, labeling protocol, docs and labels under CC BY 4.0; see CONTRIBUTING.md): a converter from SWE-chat's raw Claude Code transcripts to Docent's AgentRun format, preserving metadata, behind a format-adapter interface so converters for other agent products can be added; the metric readings as versioned prompts and schemas; the codebook; the labeling protocol; analysis notebooks that go from DQL export to the paper's tables; a backend interface so the Docent dependency can be swapped for a local pipeline.
3. Public Docent collection with the readings and citations, so readers can inspect any cited episode. Transluce allows this (Oct 2); it carries SWE-chat's ODC-By attribution.
4. A dated forward claim for the registry (E1): the expected direction of these metrics over the next year.

## 8. Architecture (functional)

- Convert: source logs to AgentRun/Transcript/ChatMessage with metadata; offline join of any commit or checkpoint data as run metadata; episode segmentation computed offline and stored as message-index ranges in run metadata.
- Analyze: Docent Analysis Plans; DQL step selects episodes or turns, reading step scores them; results in reading_results.
- Label: Docent general labels on transcript slices by two labelers; export.
- Aggregate: DQL export to pandas; validity statistics; figures.
- Everything reproducible from the exported tables and the versioned prompts.

## 9. Non-goals and safeguards

- No comprehensibility scoring of agent output beyond the M3/M4 intermediates, which are not published as metrics.
- No learned model trained on the labels (I5 stays parked).
- No identification of individual users; SWE-chat's user identifiers are hashed on ingest and per-user statistics are published as distributions only.
- Publication review for capability uplift before release, per the memo's risks section; the expected content (how humans oversee agents) is low-risk, and the review checks the intermediates.

## 10. Decisions

Decided Sept 29:
- Substrate: Docent hosted with bring-your-own keys for v1. The pipeline keeps a backend interface so the released code does not depend on it. Confirmed with Transluce (Oct 2): a public collection of our readings is allowed, with SWE-chat's ODC-By citation. The free quota is $25 a week, so the judge runs use our own key through OpenRouter, which Docent supports for BYO. Scripted readings, blind label sets and label export are supported features, and REST exports aren't capped. Still unanswered: whether Transluce's own overselling labels can be redistributed.
- M3/M4 prevalence: reported, not only the caught/addressed rates. Overclaim and misbehavior prevalence is re-measured with our rubrics so the caught rates have a matched denominator, and compared with Transluce's published rates as a consistency check. This means the M3/M4 intermediates are published metrics; section 4's "not itself a published oversight metric" is superseded for prevalence, and section 9's safeguard applies to comprehensibility scoring only, which stays out.
- Labeling (revised Oct 1): the PI and the student collaborator both label the pilot sample, replacing "PI labels the pilot alone". Two hired labelers do the full 300-episode sample once the codebook is stable, with Ron adjudicating disagreements; full-sample kappa is between the two hired labelers. Section 6 reflects this; protocol details are still open.
- License (decided Oct 1): code, prompts and schemas stay MIT, the norm among the nearest related projects (SWE-chat, Inspect, METR, SWE-bench). Apache 2.0 isn't needed because the pipeline calls Docent's SDK without copying its code. The codebook, labeling protocol, docs and labels are CC BY 4.0, and anything released with SWE-chat text also carries its ODC-By attribution. Contributors keep their copyright and contribute under these licenses; no CLA.
- Agent products (decided Oct 1): v1 measures Claude Code only, on every qualifying Claude Code session in the pinned SWE-chat release (HF revision f66cca95). Recent sessions are a later extension and don't block v1. The Transluce replication draws only from the Claude Code sessions Transluce analyzed. Results are broken down per model within Claude Code.
- Transluce replication path (decided Oct 1): every replication run is a hosted-Docent reading; rendering outside Docent with the SDK is ruled out. The gate run copies Transluce's converted runs into our own collection and re-runs their overselling reading exactly (Opus 5, high effort, 16k max new tokens, one rollout, same context config). It counts only if each session's input token count matches Transluce's. The Sonnet 5.5 run reads the same copied runs. A converter check validates our own ingest. It runs a structural diff on all sessions, then about 300 stratified sessions are re-read at the gate setting. The pass bar is that agreement with the gate is no worse than the gate's agreement with Transluce's published labels. The pilot starts only after the gate and the converter check both pass. Thresholds are set in advance (issue #10).
- Replication thresholds (decided Oct 2): the gate is a ballpark check on a pre-registered sample of 311 Claude Code sessions with published labels (Transluce's 4,788 minus the Codex sessions, the 239 pending results and the 19 sessions over 1M input tokens). The sample is stratified by Transluce's `tough_call`: 10% of tough calls and 5% of the rest. It passes if population-weighted Cohen's kappa against Transluce's labels on the same sessions is at least 0.6 and weighted overselling prevalence is within 5 points. There is no per-model test. Before launch, 20 sessions must match Transluce's input token counts exactly (on the direct Anthropic route). In the full run, more than 1% mismatched voids the gate. On failure: check the settings, read about 20 disagreements, fix, and re-run once. A second failure stops the gate, and the PI decides whether the pilot proceeds with the gap reported. Gate attempts are capped at $600. The converter check judges the same 311 sessions through our ingest. It passes if weighted kappa against the gate run is at most 0.10 below the gate's kappa against Transluce, and prevalence is within 5 points of the gate run.

Still open:
1. Judge model and reasoning setting (cost versus quality; Transluce used Opus-class with high reasoning). Proposal: pilot on 50 sessions with two candidate models, pick by agreement with pilot labels and cost.
2. Kappa threshold for reporting a metric as validated (proposed 0.6).
3. Paper venue and the date that sets the schedule (memo milestone: comprehension metrics published in months 4-6).

## 11. Open questions for the build

- SWE-chat's exact schema: which fields exist for timestamps, permission prompts, model identity, and commit linkage. Determines which descriptors in section 4 are available.
- Episode segmentation rule: heuristic on agent-turn content (claimed completion, summary, approval request) versus a judge reading; pilot both on 50 sessions and pick by agreement with labelers.
- Whether Docent's transcript_slice can address episodes that span tool-result messages cleanly, or whether episodes need to be materialized as separate transcripts.
- Handling of multi-task sessions where the human moves on without reviewing: counted as M1 "none" or excluded; pilot decides.

## References

- Docent assessment (this folder): docent-assessment.md
- Transluce, Measuring coding agent misalignment in the wild (Aug 2026): https://transluce.org/docent/blog/coding-agent-behaviors
- SWE-chat: https://arxiv.org/abs/2604.20779
- Elephant deliverable tracker, row I6
