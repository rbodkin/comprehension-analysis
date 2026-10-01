# SWE-chat schema and existing Docent converters

Resolves issue #3 (child of #2). Researched 2026-10-01.

Sources:
- **Raw release.** Hugging Face `SALT-NLP/SWE-chat`, revision `f66cca95` (last modified 2026-04-29). I downloaded all six parquet tables and read their schemas and contents, and audited the structure of 30 raw transcripts: four per agent label, two for Copilot CLI. HF access was granted partway through the work.
- **Docent conversion.** Transluce's public collection `2588573f-daa3-4130-9bce-e60ba5db04c1`, read with anonymous DQL. I pulled all 5,058 transcripts and reduced them to message skeletons.
- **The paper.** arXiv 2604.20779 v1.
- **GitHub.** `SALT-NLP/SWE-chat`, `neulab/agent-data-protocol` and `letta-ai/trajectory`.

How each claim was established:
- "Measured" means I computed it from the data.
- "Documented" means the dataset card or the paper states it.
- "Inferred" means I reasoned it from the evidence and did not verify it directly.

## Short answer

- **The raw release is much richer than the Docent conversion.** The raw per-session transcripts (`transcripts/*.jsonl`) carry per-event timestamps, permission mode, `is_error`, tool-interrupt flags, structured patches, queue events, subagent traffic and Codex approval/sandbox policy. The parquet `conversations` table flattens these into rows and keeps timestamps, tool names, queue operations and LLM-annotated intent/pushback labels. It drops `is_error` and permission mode.
- **Transluce's Docent conversion drops every per-message timestamp.** This alone rules out M8 (time lag) if we work from Docent.
- **The Docent conversion keeps the other signals we need.**
  - Kept: tool names, tool errors (`error` field, Claude Code only), interrupt and permission-rejection text, model identity, and commit/checkpoint linkage (commits without patches).
  - Partial: permission mode (in 347 of 4,845 Claude Code sessions).
  - Dropped: prompt-level intent and pushback labels.
- **Converter status.**
  - Transluce's converter code is not public.
  - SALT's GitHub repo says "data and code coming soon" and holds only a README.
  - One public converter exists: `neulab/agent-data-protocol` converts SWE-chat to ATIF, which is the Harbor format that Docent imports natively. It is built from the parquet `conversations` table, drops timestamps, and gets nothing usable for Codex, because the parquet has no Codex agent rows.
  - None of the existing converters preserves the §3 message-level metadata. We will have to write our own, starting from the raw JSONL.
- **Sessions that qualify under spec §3** (at least one genuine human prompt after the first agent turn, strict classifier):
  - Raw release: about 4,360 of 5,851 sessions. Claude Code 3,899 of 4,852, OpenCode 383 of 623, Cursor 17 of 19, Gemini CLI 4 of 59, other labels 60.
  - Codex cannot be counted from the parquet. From Docent, Codex is 48 of 213.
  - Docent conversion: Claude Code 3,660 of 4,845.
  - Details and the reasons the numbers differ are in §4.

## 1. What the raw release contains

### Tables (measured row counts match the card)

| Table | Rows | Key | What it holds |
|---|---|---|---|
| `sessions` | 5,851 | `session_id` | agent label, strategy, branch, `created_at`, token totals, tool-call counts, `duration_seconds`, `turn_count`, `prompt_count`, code attribution (`agent_lines`, `human_*`, `agent_percentage`), LLM labels `user_persona` and `session_success` |
| `session_logs` | 5,851 | `session_id` | `transcript_path`, `context_md`, `session_metadata_raw` (Entire's metadata.json) |
| `conversations` | 2,692,480 | `turn_id` | one row per transcript entry: `role`, `turn_type`, `content` (tool results truncated to 10 KB), `model`, `timestamp`, token usage, `tool_name`, `tool_call_id`, `file_path`, `command`, `tool_input_json`, `category`, `bash_category`, `queue_op_subtype`, LLM labels `prompt_intent` and `prompt_pushback` |
| `checkpoints` | 13,406 | `checkpoint_pk` | session ↔ commit join (JSON arrays), checkpoint token totals, additions and deletions |
| `commits` | 14,459 | `commit_sha` | author and commit dates, message, `is_agent_author`, `files_changed`, `numstat`, full `patch`, `agent_changes`, per-file `file_attribution` |
| `repositories` | 205 | `repo_id` | GitHub metadata, license, LLM labels `repo_type_domain` and `repo_type_audience` |
| `transcripts/*.jsonl` | 5,850 files | `session_id` | the agent's native log, verbatim except for PII redaction |

Notes on the transcript files (measured):
- Every file has a `.jsonl` extension, including Gemini CLI. The card says `.json` for Gemini, but Gemini and OpenCode files are single JSON documents saved under a `.jsonl` name.
- One session (`bce82ae2-…`) has an empty `transcript_path`.

### Agent labels (measured from `sessions.agent`)

| Agent label | Sessions | Users | Repos |
|---|---|---|---|
| Claude Code | 4,852 | 172 | 183 |
| OpenCode (+1 `opencode`) | 624 | 14 | 15 |
| Codex | 213 | 4 | 8 |
| Gemini CLI | 59 | 8 | 8 |
| unknown | 52 | 3 | 1 |
| Agent | 24 | 4 | 1 |
| Cursor | 19 | 3 | 3 |
| Roger Roger Agent / Vogon Agent / claude-code | 4 / 1 / 1 | | |
| Copilot CLI | 2 | 2 | 2 |

The labels are noisy. Of the sampled files, "Agent" files are Claude Code JSONL and "unknown" files are Gemini-format JSON (measured). `letta-ai/trajectory` PARITY.md reports the same problem: Gemini labels "must be routed by content". Codex comes from only 4 users, and the Docent sample shows heavy use of the oh-my-codex orchestrator, whose injected leader/worker messages look like user turns.

### Coverage gaps in `conversations.parquet` (measured)

| Agent | Agent/tool rows? | `timestamp` filled | Notes |
|---|---|---|---|
| Claude Code | yes | 100% of agent, tool and system rows; 83% of `user_prompt` | 9,572 user-prompt rows have no timestamp. Many look like agent-written reports (subagent or sidechain text), not human prompts |
| Codex | **no**: 1,263 `user_prompt` rows only | 0% | The agent side of Codex exists only in the raw JSONL |
| OpenCode | yes | 0% | The raw JSON has `time.created` and `time.completed` in milliseconds |
| Cursor | assistant text only | 0% | The raw capture has no timestamps, tool IDs or tool results (also per letta PARITY.md) |
| Gemini CLI | only 11 of 59 sessions have rows | partial | The raw JSON has per-message and per-tool-call timestamps |

### Native fields in the raw transcripts that the parquet drops (measured on samples)

- **Claude Code JSONL:**
  - per-entry `timestamp`, `uuid`/`parentUuid` and `isSidechain`;
  - `permissionMode` on user entries;
  - `message.content[].is_error` on tool results;
  - `toolUseResult.interrupted`, `.userModified` and `.structuredPatch`;
  - AskUserQuestion `answers`, `promptId`, `queue-operation` records, `pr-link` records;
  - subagent messages nested under `progress.data.message`;
  - `system` subtypes (`turn_duration`, `stop_hook_summary`, `compact_boundary`).
- **Codex rollout JSONL:**
  - per-record `timestamp`;
  - `session_meta` and `turn_context`, carrying `approval_policy`, `sandbox_policy`, `model`, `effort` and `git.commit_hash`;
  - `exec_command_end` events with exit codes, `turn_aborted` events, `ghost_snapshot` commits, and `source.subagent`.
- **OpenCode JSON:** session `info.permission[]` rules; per-message model, cost, tokens and times; and tool `parts[].state` (completed, error or running).
- **Copilot CLI events:** `session.mode_changed`, `tool.execution_complete` with `success` and `error`, plus timestamps.

## 2. Field by field: spec §3/§4 inputs

Legend: **P** = present, **Pt** = partial, **A** = absent. "Raw" splits into the parquet tables and the JSONL transcripts.

| Field | Raw parquet | Raw JSONL | Docent conversion | Notes |
|---|---|---|---|---|
| Message timestamps (M8) | Pt (Claude Code yes; Codex, OpenCode and Cursor no) | P for Claude Code, Codex, Gemini, OpenCode and Copilot; A for Cursor | **A**. Messages carry no time. Only run-level `started_at`/`ended_at`, plus `total_turn_duration_ms` in 3,342 Claude Code and 34 Codex sessions | M8 needs the raw data |
| Session start, end, duration | P (`created_at`, `duration_seconds` for Claude Code; 0 for OpenCode, Codex and Cursor) | P | P (`started_at`, `ended_at` on all 5,058; `duration_seconds` on 4,843) | |
| Permission prompts shown and approved | A | **A in every format.** Claude Code logs no "prompt shown" or "approved" event | A | Approvals cannot be observed, so the §4 descriptor "auto-accept rate" is not computable |
| Permission rejections | Pt (rejection text in `tool_result` content: 2,012 rows, 1,037 Claude Code sessions) | P (same text plus `is_error: true`) | P (tool message `error` set, text kept: 1,033 Claude Code sessions) | Includes "user said: …" feedback attached to a rejection, ExitPlanMode rejections, and AskUserQuestion "clarify" |
| Permission mode / approval policy | A | P (Claude Code `permissionMode` per user entry; Codex `approval_policy` and `sandbox_policy`; OpenCode rules) | Pt (Claude Code `permission_modes` list in only 347 of 4,845 sessions: bypassPermissions 225, default 111, acceptEdits 46, plan 6. Codex `approval_policy` on all 213: never 197, on-request 16; `sandbox_mode` on all 213) | Docent's Claude Code coverage is much lower than the raw. In the 4 sampled raw files, all 4 carry `permissionMode`. Why the converter kept so few is unknown |
| Interrupts | P (`[Request interrupted by user…]` in `user_prompt` rows: 2,711 rows, 1,326 Claude Code sessions) | P (also `toolUseResult.interrupted`; Codex `turn_aborted`) | P (Claude Code marker text in 1,327 sessions; Codex `<turn_aborted>` user messages in 47 sessions plus `aborted`/`abort_reason` in 22) | The paper's turn-level interrupt rate (3.3–6.0%) uses these markers |
| Queued or typed-ahead prompts | P (`queue_operation`: enqueued 166k, delivered 170k, discarded 4,972 for Claude Code) | P | Pt (`queued_commands` text list in 2,243 Claude Code sessions; task notifications kept as user messages tagged `source: task_notification`) | Discarded prompts are lost in Docent |
| Tool names | P (`tool_name`; Codex A) | P | P (`function` on every tool call and result) | |
| Tool errors | A (no `is_error` column; must be inferred from text) | P (Claude Code `is_error`, OpenCode state, Gemini status, Copilot `success`) | Pt (Claude Code `error` on 17,399 of 401,862 tool messages, 3,259 sessions. Codex: no `error` field; `exit_code` in metadata on 1,878 of 21,771 tool messages, otherwise "Process exited with code N" in the text) | |
| Tool inputs and outputs | P (input JSON; results truncated to 10 KB) | P (untruncated, plus structured patches) | P (arguments and result text; truncation not checked) | |
| Agent product | P (`sessions.agent`, noisy labels) | P (by format) | P (`agent`: Claude Code 4,845, Codex 213) | |
| Model identity | Pt (per assistant row for Claude Code; A for Codex, OpenCode and Cursor in the parquet) | P for Claude Code, Codex, OpenCode and Gemini; A for Cursor | P (run-level `model`, a string or a list in 814 multi-model runs; per message for Claude Code only. Codex messages have no model; run metadata has it plus `effort`) | Claude Code `<synthetic>` appears in 677 sessions |
| Task type labels | P (`prompt_intent` per user prompt, 8 classes; `prompt_pushback` per prompt, 6 classes; session `user_persona`, `session_success`; repo domain and audience). All LLM-annotated | n/a | Pt (`user_persona`, `session_success`, `repo.repo_type_domain` and `repo_type_audience` kept. **`prompt_intent` and `prompt_pushback` dropped.** Entire's `summary.intent` in 374 runs) | |
| Commit linkage | P (`checkpoints` ↔ `commits` with full `patch`, `numstat`, `file_attribution`) | Pt (Codex `git.commit_hash`, ghost commits; Claude Code `pr-link`) | Pt (`commits[]` holds SHA, dates, message, `agent_changes`, `file_attribution` and additions/deletions, but **no patch or numstat**; `checkpoint.commit_shas` on 5,007 runs; Claude Code `pr_links` on 844; Codex `git_commit` on 199) | Diff-level work needs the raw `commits` table |
| Checkpoint linkage | P | n/a | P (`checkpoint_ids`, `canonical_checkpoint_pk`) | The paper limits commit-level attribution to the 48.6% of sessions that attribute cleanly |
| Code attribution | P | n/a | P (`agent_lines`, `human_*`, `scores.agent_percentage`) | |
| User and repo IDs | P (`user_id` = commit author) | P (paths contain usernames) | P (`user_id` on 3,289 runs, `repo_id` on all) | Spec §9: hash on ingest |
| Thinking traces | P (`assistant_thinking`, 128 Claude Code rows) | P (signatures; Codex encrypted) | P (reasoning blocks) | |
| Subagent and sidechain traffic | Pt (likely in timestamp-less `user_prompt` rows) | P | A apart from the Agent/Task tool result and task notifications | |
| Context compaction | Pt (`summary` and system rows) | P | P (`compact_boundary` system messages; Codex `context_compacted`) | |

**Inferred:** if we want to keep using Transluce's runs, the realistic plan is to join the raw tables offline onto the Docent run IDs through `metadata.session_id`. All 5,058 of those IDs match `sessions.session_id` (measured). M8 would then be computed outside Docent.

## 3. Existing converters

| Converter | Public? | Input | Output | What it keeps or drops |
|---|---|---|---|---|
| Transluce SWE-chat → Docent | **No.** Only its output is public | Raw JSONL, inferred: Codex agent turns are present, and the parquet has none | Docent `AgentRun` with one transcript each | Drops message timestamps, prompt labels, commit patches, discarded queue items and subagent traffic. Keeps tool errors (Claude Code), interrupt and rejection text, run-level metadata. See the selection and fidelity notes below |
| `neulab/agent-data-protocol` `datasets/SALT-NLP_SWE-chat` (added in #256, `3824726`, 2026-06-14) | Yes (`extract_raw.py`, `raw_to_atif.py`, `atif_to_std.py`) | Parquet `conversations` plus `sessions` (needs `HF_TOKEN`) | ATIF trajectories, which Docent imports natively, then ADP std/SFT | Keeps a few session fields: agent, strategy, persona, success, agent %. No timestamp handling in `scripts/raw_to_atif_common.py`. No error, interrupt or permission semantics. Codex sessions come out empty because the parquet has no agent rows |
| `letta-ai/trajectory` (PARITY.md @ `5d5b148`) | Yes | Native SWE-chat raw files for OpenCode, Gemini CLI, Cursor and Copilot CLI | Letta's own trajectory format, not Docent | Native times, IDs, statuses and string errors preserved. Useful as a reference parser for the non-Claude formats |
| SALT-NLP/SWE-chat GitHub (`8608198`) | No code ("data and code coming soon") | | | |

### Transluce selection rule (measured; resolves part of #6 item 4)

- The collection contains every HF session labelled exactly `Claude Code` (4,845 of 4,852) or `Codex` (213 of 213). It contains none of the OpenCode, Gemini CLI, Cursor, Copilot, "Agent" or "unknown" sessions.
- Of the 7 missing Claude Code sessions:
  - 5 have no agent rows (a single prompt only);
  - 1 has no transcript;
  - 1 is unexplained: `2026-01-28-7f78a542-…`, with 1,549 rows and 440 of them agent rows.
- The earlier guess that 5,058 = 5,851 minus Gemini is wrong. The gap is mostly OpenCode (624).

### Fidelity notes on the Docent conversion (measured)

1. **Role mixing.** Docent's `user` role mixes real prompts with injected content: local-command caveats, task notifications, skill bodies, continuation summaries, Conductor `<system_instruction>`, teammate messages, oh-my-codex injections, Codex AGENTS.md and environment context.
   - In Claude Code, my classifier counts 30,223 human prompts and 24,673 injected messages among the user-role messages.
   - Only task notifications are tagged (`metadata.source`). The parquet does better here: it splits out `system_injected` and flags `is_continuation`.
2. **Missing human prompts.** Some human prompts in the raw data are missing from Docent.
   - Across Claude Code sessions, Docent has fewer strict-human prompts than the raw timestamped `user_prompt` rows in 1,579 sessions, and more in 248. Net, it is missing 3,764 of 33,422 raw prompts (11%).
   - Example: session `f5455122-…`. The raw prompt "commit" at turn 306 has no Docent counterpart, even though the run's own `n_human_turns` metadata says 4 and the transcript holds 2 user messages.
   - The cause is unknown. Possibilities include branch selection along `parentUuid` after a rewind, merging of consecutive entries, or a differing classifier on my side. Treat Docent turn counts as approximate.
3. **Tool-error asymmetry.** Codex tool messages never set `error`, so the `error` field means something different for each agent.

## 4. Sessions qualifying under spec §3

### Rule as implemented

- **Anchor.** The first agent action is variant A, the first assistant row or message. Variant B, the first tool call, gives counts lower by 1% or less.
- **Strict human turn.** A user prompt counts only if it is not:
  - an interrupt marker on its own;
  - a continuation summary;
  - a slash-command or local-command wrapper;
  - a task notification, skill body, hook feedback, `<system_instruction>`, teammate or orchestrator injection, AGENTS.md or environment context;
  - "Continue from where you left off.";
  - "Implement the following plan:", the message injected when a plan is approved.
- **Inclusive human turn.** Also counts interrupts, slash commands, plan approvals and tool rejections.
- The classifier is the same for both sources (`classify()` in the scratch script). The prefix list is hand-built from the most frequent openings and will need tuning in the pilot.

| Agent | Sessions | Raw parquet: strict | Raw: inclusive | Raw: strict, timestamped prompts only | Docent: strict | Docent: inclusive |
|---|---|---|---|---|---|---|
| Claude Code | 4,852 (Docent 4,845) | 3,899 | 3,964 | 3,817 | 3,660 | 3,782 |
| Codex | 213 | not computable (no agent rows) | | | 48 | 48 |
| OpenCode | 624 | 383 | 383 | n/a | not in Docent | |
| Cursor | 19 | 17 | 17 | n/a | not in Docent | |
| Gemini CLI | 59 | 4 (only 11 have rows) | 4 | 3 | not in Docent | |
| unknown / Agent / Copilot | 52 / 24 / 2 | 41 / 18 / 1 | 41 / 19 / 1 | | not in Docent | |
| Other labels | 7 | 0 | 0 | | | |

What the numbers say:
- **Claude Code.** Between 75% and 82% of sessions qualify, depending on the source and the rule.
  - The raw count is higher partly because of the timestamp-less `user_prompt` rows, which are probably subagent text. Removing them takes 3,899 down to 3,817.
  - The rest of the gap is Docent's missing prompts (fidelity note 2).
  - Naive rule, counting any user-role message after the first assistant message: raw 4,123, Docent 4,205. This shows how much the injected-message filter matters.
- **Codex.** Only 48 of 213 qualify (Docent).
  - 110 sessions have no strict human prompt at all.
  - 24 have no assistant message.
  - Most are oh-my-codex worker or subagent sessions, 56 of which carry `agent_role` metadata.
  - Inferred: Codex adds little to a human-oversight analysis.
- **Qualifying population for v1.** About 4,360 sessions on the raw rule, about 85% of them Claude Code. If we stay inside Docent, about 3,700.

## Newly surfaced questions

1. **Substrate for the transcript.** Should we convert from the raw JSONL ourselves instead of reusing Transluce's runs? Their runs lack timestamps (M8), prompt labels, patches and some human prompts. The cost of a raw conversion is losing exact comparability with Transluce's overselling labels, unless we keep their run IDs and join the raw data onto them. Recommendation: own converter from raw JSONL, keyed by `session_id`, and a mapping to Transluce run IDs kept for M3.
2. **Scope beyond Claude Code.** Should v1 include OpenCode (624 sessions, 14 users, no parquet timestamps but raw millisecond times) and Gemini CLI? Transluce excluded them, so including them breaks the overselling comparison for that slice.
3. **Is Codex worth including?** 48 qualifying sessions from 4 users, dominated by one orchestrator.
4. **Permission prompt metric.** Approvals are never logged. Should the "permission prompts and auto-accept rate" descriptor in §4 become "permission mode plus rejection count", given that rejections are observable?
5. **Missing Docent prompts.** What drops about 11% of human prompts? Add this to the Transluce questions (#6).
6. **Raw parquet quirks to raise with SALT.**
   - What are the 9,572 timestamp-less Claude Code `user_prompt` rows?
   - The parquet has no Codex agent rows, and 48 of 59 Gemini sessions have no rows.
   - The card says Gemini files are `.json`, but all files are `.jsonl`.
7. **Human-turn classifier.** The injected-message filter moves the §3 count by about 10 points. The pilot should fix it as part of the codebook, and the rule should be written into spec §3.

## Appendix: reproduction

Scratch scripts are not committed. They lived in the session scratchpad. The essential queries are below.

- **Docent transcripts.** `messages` and `metadata_json` are `bytea`, so decode them in DQL with `convert_from(t.messages, 'UTF8')`. For example, counting interrupt markers by agent:

  ```sql
  SELECT ar.metadata_json->>'agent', count(1) FROM transcripts t JOIN agent_runs ar ON ar.id = t.agent_run_id
  WHERE convert_from(t.messages, 'UTF8') LIKE '%[Request interrupted by user%' GROUP BY 1
  ```

  POST it to `https://api.docent.transluce.org/rest/dql/2588573f-daa3-4130-9bce-e60ba5db04c1/execute` as `{"dql": ...}`. The full corpus is about 1.65 GB, so fetch transcripts in batches of 10 to 40 (`WHERE t.agent_run_id IN (...)`).
- **Raw parquet.** Use duckdb over `hf download SALT-NLP/SWE-chat <table>.parquet --repo-type dataset` (needs gated access). The qualification anchor is `min(turn_number) FILTER (WHERE turn_type IN ('assistant_response','tool_use','assistant_thinking'))` per session. Human prompts are `turn_type='user_prompt'` rows passed through the classifier.
- **Docent ↔ raw join.** `agent_runs.metadata_json->>'session_id'` = `sessions.session_id`. All 5,058 match.
