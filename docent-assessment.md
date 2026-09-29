# Docent (Transluce) for comprehension-metrics research: assessment as of Sept 29, 2026

Research pass by an agent over primary sources (docs.transluce.org, github.com/TransluceAI/docent, transluce.org blog, PyPI). Verify flagged items with Transluce before committing to a hosting decision.

## 1. What Docent is

Positioning: "a behavior analysis platform for agents": ingest transcripts, then use LLM "readings" plus a SQL subset to find, measure, and cluster behaviors ([docs intro](https://docs.transluce.org/introduction.md)). Built by Transluce, a 501(c)(3) ([landing page](https://transluce.org/docent)).

Architecture (hosted product, per docs):
- Ingestion: Python SDK (`AgentRun` -> `Transcript` -> `ChatMessage`), a `/docent` Claude Code/Codex plugin that writes ingestion scripts, a tracing library that hooks OpenAI/Anthropic SDK calls, and native converters for Inspect `.eval`, Harbor/ATIF, and NeMo Gym ([ingestion quickstart](https://docs.transluce.org/ingestion/quickstart.md), [llms.txt](https://docs.transluce.org/llms.txt)).
- Analysis: Analysis Plans (June 2026), a lazily evaluated DAG of DQL steps (read-only SQL over Postgres) and Reading steps (one LLM call per DQL row, JSON-schema-constrained output with transcript citations). Clustering is a reduce-style reading over prior reading results ([analysis plans](https://docs.transluce.org/analysis/analysis-plans.md), [reading steps](https://docs.transluce.org/analysis/reading-steps.md), [blog](https://transluce.org/docent/blog/analysis-plans)).
- Legacy (available, "no longer recommended"): rubric objects + judge jobs, guided rubric refinement chat, embedding search and centroid clustering ([legacy rubrics](https://docs.transluce.org/legacy/rubrics.md), [refinement](https://docs.transluce.org/legacy/rubrics/refinement.md), [clustering SDK](https://docs.transluce.org/sdk/rubrics/clustering.md)).
- Stack (self-host): FastAPI-style backend, Next.js/Bun frontend, Postgres 15, Redis, background worker, optional OTel collector ([self-host guide](https://github.com/TransluceAI/docent/blob/main/docs/self_hosting/self_host_docent.md)).

License and hosting: Apache 2.0 since Sept 24, 2025 ([open-source post](https://transluce.org/docent/blog/open-source)); hosted at docent.transluce.org, labelled "public alpha"; "white-glove hosting" for large orgs by email.

Important caveat (inferred): the GitHub SDK `client.py` contains only collections, run upload, Inspect ingestion, legacy rubric/cluster reads, and sharing; no DQL, labels, readings, or analysis plans ([client.py](https://raw.githubusercontent.com/TransluceAI/docent/main/docent/docent/sdk/client.py)). Commit history since ~June 2026 is dependabot only ([commits](https://github.com/TransluceAI/docent/commits/main/)). PyPI `docent` 0.1.87 (Sept 16, 2026) tracks the current docs ([PyPI](https://pypi.org/project/docent/)). Conclusion: the self-hostable OSS snapshot is roughly the late-2025 feature set; Analysis Plans, DQL, general labels, and context configs are documented only for the hosted service.

Recent changes: public changelog stops Oct 30, 2025 ([changelog](https://transluce.org/docent/changelog)); newer features on the blog: Terminal-Bench regression study (Feb 2026), Analysis Plans (June 2026), coding-agent misalignment study (Aug 2026) ([blog](https://transluce.org/docent/blog)).

## 2. Data model

- `Collection` -> `AgentRun` (one task execution) -> `Transcript`s (optionally grouped for multi-agent) -> `ChatMessage`s ([overview](https://docs.transluce.org/concepts/overview.md)).
- Roles: System, User, Assistant (with `tool_calls`), Tool (with `tool_call_id`, `function`, `error`). Content is text or text/reasoning blocks; no image/audio. Free-form `metadata` dict at every level ([chat messages](https://docs.transluce.org/concepts/chat-messages.md)).
- OpenAI-compatible schema; `parse_chat_message` converts OpenAI-style dicts and Inspect messages ([SDK ingestion](https://docs.transluce.org/ingestion/sdk.md)). Claude Code JSONL is not a documented importer; the `/docent` plugin writes `ingest.py` for arbitrary formats ([agentic ingestion](https://docs.transluce.org/ingestion/agentic.md)). Transluce ingested ~5,000 SWE-chat sessions (Claude Code, Codex, Gemini CLI) plus 3,600 internal sessions, so the path is proven ([misalignment post](https://transluce.org/docent/blog/coding-agent-behaviors), [SWE-chat](https://arxiv.org/abs/2604.20779)).
- Human turns are distinct (`UserMessage`); reading steps can target any contiguous window via `transcript_slice(transcript_id, start, end)` with indices computed per row. Diffs exist only as tool-call arguments rendered as text; no diff, file, commit, or PR primitive. Timestamps, permission prompts, interrupts survive only if placed in message metadata.

## 3. Analysis primitives

- Readings/judges: prompt template with typed parameters (`transcript`, `transcript_slice`, `agent_run`, `reading_result`, `text`), any model (OpenAI, Anthropic, Google, OpenRouter), `reasoning_effort`, JSON Schema output, `"citations": true` on string fields; context configs control which metadata the judge sees.
- Search/clustering: legacy embedding search + centroids; new pattern is per-transcript reading then a reduce reading over `array_agg` of results, including recursive re-clustering.
- Labeling: label sets (JSON-schema validated, per run), general labels targeting `agent_run`, `transcript`, `transcript_slice`, or `reading_result`; tags; comments ([labels SDK](https://docs.transluce.org/sdk/feedback/labels.md)). UI labeling of judge results with a live agreement rate; multi-rollout judges with inconsistency highlighting. No kappa or multi-annotator adjudication; export and compute.
- Export: DQL over `agent_runs`, `transcripts`, `transcript_groups`, `judge_results`, `reading_results`; 10,000-row cap per query ([exporting](https://docs.transluce.org/analysis/exporting.md), [DQL schema](https://docs.transluce.org/sdk/dql/schema.md)). Messages stored as bytea JSON; message-level DQL possible but clunky.

## 4. Programmatic access

Python SDK only. `client.query()` and `client.read()` build a plan; `.results` forces execution; steps content-hashed and cached; `client.flush(auto_approve=True)` skips the approval gate. Per-transcript metrics = one reading per DQL row; aggregation = DQL over `reading_results`. Auth by API key or AWS OIDC ([client](https://docs.transluce.org/sdk/client.md)).

## 5. Scale and cost

Collections up to 1M agent runs. Judge calls run server-side; hosted accounts have a free LLM quota; bring-your-own keys for OpenAI/Anthropic/Gemini. Reading results record tokens per call. No public pricing. Transluce's study ran Opus-class judges with high reasoning and 16k output tokens over 8,600 transcripts; budget on the order of one long-context judge call per transcript per metric.

## 6. Known uses

- Anthropic cites Docent in Claude 4 alignment work ([system card](https://www-cdn.anthropic.com/4263b940cabb546aa0e3283f35b686f4f3b2ff47.pdf)).
- SWE-bench leaderboard (bash-only) links trajectories into public Docent collections; cheating judge demo ([SWE-bench post](https://transluce.org/docent/blog/swe-bench)).
- Public collections: SWE-rebench cheating plan, SWE-Bench Pro failure clusters, Terminal-Bench comparison ([Terminal-Bench post](https://transluce.org/docent/blog/terminal-bench)).
- Most relevant: "Measuring coding agent misalignment in the wild" (Aug 4, 2026): 8,600 real sessions; two hand-refined rubrics (overselling, monitor evasion) with `behavior_present / tough_call / is_severe`; a "skeptical verifier" second reading; per-model and per-user breakdowns; raw data public ([post](https://transluce.org/docent/blog/coding-agent-behaviors)). Its limitations section is on point: lying by omission was hard to catch; transcripts alone underdetermine severity without the codebase; user reactions were hard to interpret.

## 7. Fit for comprehension metrics

| Metric | Fit | Notes |
|---|---|---|
| Asked-vs-delivered discrepancy | Strong | Nearly identical to Transluce's overselling rubric; per-run reading with citations |
| Agent explained change, human responded | Strong | Reading over a transcript slice (final assistant message + next user turn); DQL locates indices |
| Unaddressed misbehavior | Good, two stage | Reading 1 flags misbehavior and message index; DQL builds a slice from that index to the end; Reading 2 judges whether the user addressed it |
| Human pushback / correction rate per turn | Good | Reading per user turn, or DQL over message JSON if pre-labeled in metadata |
| Did the human read the diff before approving | Weak | Transcripts carry no reading behavior; proxies (latency between agent output and next human action, approval events, diff size) computed outside and attached as metadata |
| Diff-level and PR/commit linkage | Not supported | No diff parsing, file/hunk objects, or git linkage; SWE-chat `commits` and `checkpoints` tables joined offline and injected as run metadata |
| Inter-rater reliability | Partial | Label sets and general labels on slices give a storage layer; agreement UI for judge-vs-label; no kappa or multi-rater adjudication |

What we would build: (a) a Claude Code/Codex JSONL to `AgentRun` converter that maps tool results to `ToolMessage`, preserves timestamps, permission prompts and interrupts in metadata, and attaches diff stats and commit outcomes as run metadata; (b) offline feature extraction for latency and diff-size proxies; (c) an export-and-analyze layer (DQL to pandas) for agreement statistics and figures.

Ed: There must be an existing converter to read SWE-Chat into Docent given Transluce has analyzed it.

## 8. Alternatives (not primary-verified in this pass)

- Inspect (UK AISI): eval framework with log viewer and model-graded scorers; good for re-run tasks, weaker for post-hoc analysis of wild transcripts; Docent ingests Inspect logs natively.
- LangSmith / Langfuse / Braintrust: production tracing with LLM-as-judge evaluators and annotation queues; Langfuse is open-source and self-hostable. Trace-shaped rather than transcript-shaped: no slice judging, citations, or clustering.
- W&B Weave: tracing plus scorers and dashboards; similar strengths and gaps.
- Custom pipeline (pandas + LLM API + own rubric loop): full control over diff-awareness and git linkage, cheapest to iterate, but rebuilds citation checking, a review UI, and labeling storage, which is where Docent's value concentrates.

## Recommendation

Use Docent as the analysis substrate for the transcript-native metrics (hosted, BYO keys), and build the diff/PR/human-behavior layer ourselves. Its reading-step + slice + citation + general-label stack maps onto three of the four target metrics, and Transluce has run the closest published analog on the same SWE-chat data, which makes the methodology citable and comparable. Two conditions: (1) confirm with Transluce (docent@transluce.org) whether the OSS repo will receive Analysis Plans/DQL, since self-hosting today locks in the 2025 feature set; (2) export all raw labels and reading outputs via DQL so the paper's statistics do not depend on the hosted service. If data cannot leave our environment or Transluce declines to open-source the current stack, use Docent for exploration and rubric development only, and run production measurement in a custom pipeline that reuses the refined rubrics.
