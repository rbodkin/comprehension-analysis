# Docent capabilities: episode slicing, model support, export, multi-rater labels

Resolves issue #5 (child of #2). Research date: 2026-10-01. This builds on `docent-assessment.md` and does not repeat it.

Sources, in order of trust:
- **SDK**: PyPI `docent` 0.1.87 wheel (uploaded 2026-09-16, still the latest). Paths below are inside the wheel, e.g. `docent/sdk/_labels.py`.
- **Live API**: `GET https://api.docent.transluce.org/rest/reading/reading-models`. No login needed; 1,220 entries on 2026-10-01.
- **Docs**: docs.transluce.org pages listed in [llms.txt](https://docs.transluce.org/llms.txt).
- **OSS server**: github.com/TransluceAI/docent `main`. Last non-dependabot change was before June 2026.
- **OpenAI model docs**: developers.openai.com.

## Verdicts

| # | Question | Verdict |
|---|---|---|
| a | Can `transcript_slice` address an Episode that spans tool-call and tool-result messages? | **Supported**. Getting per-episode bounds into a reading needs a small workaround: scripted readings, or one metadata key per episode. |
| b | BYO keys: Opus 5.5, Sonnet 5.5 with a reasoning setting, GPT-6.1 Luna? | **Supported** for Opus 5.5 and Sonnet 5.5, at effort low/medium/high only (no xhigh/max). **Unsupported** for GPT-6.1 Luna, because OpenAI has no model by that name. The nearest are `gpt-6-luna` and `gpt-6.1-sol`, and both are selectable. |
| c | Export limits (DQL 10k cap, bytea messages) for pulling every reading result and label | **Workaround**. Page DQL with ORDER BY + LIMIT/OFFSET. Decode bytea with `convert_from`. Labels come out through REST endpoints, not DQL. Fine for our volumes. |
| d | Two raters label the same items with separate attribution, for kappa | **Supported** at agent-run level (blind label sets with assignees, plus attributed export). **Workaround** at transcript-slice level: general labels record `created_by` but have no blind or assignment mode and no list endpoint. Either keep one general label set per rater, or make each episode its own agent run. |

## (a) Episode slicing

How a slice works:
- **Indices.** A transcript is a flat list of `ChatMessage`s. Tool calls sit on `AssistantMessage.tool_calls`, and each tool result is its own `ToolMessage` with its own index ([chat messages](https://docs.transluce.org/concepts/chat-messages.md)).
- **Bounds.** `transcript_slice(transcript_id, start_idx, end_idx)` is 0-based, inclusive at both ends, and accepts negative indices. Out-of-range bounds render fewer messages without raising an error. Rendered messages keep their absolute indices, so citations still point into the full transcript ([reading steps](https://docs.transluce.org/analysis/reading-steps.md)).
- **No role filtering.** `Transcript.to_text(message_slice=...)` keeps every message whose index falls between the bounds, whatever its role (`docent/data_models/transcript.py`, lines 356-420). An Episode running from a claimed completion through tool calls and results to the next human turn renders as one contiguous block, with tool calls shown inline as `<tool call>` (`format_chat_message`, same file, lines 180-238). The slice renderer itself does not truncate (same code). Context-window limits still apply to the whole prompt.
- **Context configs.** These work on slices (`TranscriptSliceContextConfig`), so per-message metadata such as timestamps or permission prompts can be shown to the judge for the slice only.

Getting per-episode bounds into a reading:
- **Template readings: one row per Episode.** A template reading makes one LLM call per DQL row, so we need one row per Episode. The documented DQL function list includes `unnest` and `jsonb_array_length`, but not `jsonb_array_elements` or `generate_series` ([execute_dql, allowed syntax](https://docs.transluce.org/sdk/dql/execute.md)). A JSON array of episodes stored in metadata therefore cannot be exploded into rows with documented functions. Two workarounds:
  1. **Scripted readings (recommended).** `client.read(prompts_list=[[..., TranscriptSliceRef(transcript_id, start_idx, end_idx, agent_run_id, collection_id).label("episode")], ...])`. The bounds come from our offline segmenter; no DQL is involved. The labelled ref is stored in `arguments_dict`, so results join back to Episodes (`docent/sdk/_readings.py`: `read`, lines 394-495; `_serialize_scripted_requests`, lines 576-618). This path is in the SDK but not on the docs site, so treat it as less stable.
  2. **Template readings with fixed metadata keys.** Write `episode_k_start` / `episode_k_end` into transcript metadata. Then UNION ALL one SELECT per k, or ingest one transcript per Episode.
- **Materializing episodes as separate transcripts is not required for judging.** It only becomes attractive for multi-rater labelling; see (d).
- **Judge-based segmentation.** If segmentation is done by a judge reading rather than offline, its output (`reading_results.output`) can feed a second reading only through DQL. That brings back the explode-rows problem. Plan to segment offline, or to export the segmentation results and resubmit them as scripted slices.

Caveats:
- **Only one reasoning block renders.** In `format_chat_message`, only the last `ContentReasoning` block of a multi-block assistant message survives (`cur_content =` overwrites inside the loop). Minor, but relevant if agent reasoning matters to a metric.
- **No slices when self-hosted.** The OSS server has no `transcript_slice` or DQL at all (grep of TransluceAI/docent `main` finds no matches). Slicing is a hosted-only feature.

## (b) Models, reasoning settings, BYO keys

**The model list is a live server catalog.**
- The SDK no longer hardcodes models. Pricing and context windows come from "the dynamic model catalog" on the server (`docent/_llm_util/model_registry.py`).
- `client.get_reading_models()` calls `/reading/reading-models` (`docent/sdk/_readings.py`, lines 155-165).
- Fetched without login on 2026-10-01, that endpoint listed:
  - `anthropic/claude-opus-5-5` and `anthropic/claude-sonnet-5-5`: 1M context, `reasoning_effort` in {null, low, medium, high}.
  - `openai/gpt-6-luna`, `gpt-6-sol`, `gpt-6-astra`, `gpt-6.1-sol` (1.05M context), and the `gpt-5.6-*` family.
  - The same models on OpenRouter (`openai/gpt-6-luna`, `openai/gpt-6.1-sol`, `~openai/gpt-luna-latest`, and others).
  - No `gpt-6.1-luna` under any provider.
- Readings take `model="provider/model_name"`. The SDK accepts any string (`_parse_model_option`). Whether the server rejects models outside the catalog is unknown, and it does not matter for the models we want.

**GPT-6.1 Luna does not exist.**
- OpenAI's [models index](https://developers.openai.com/api/docs/models) lists `gpt-6-astra`, `gpt-6-luna` and `gpt-6.1-sol`.
- `.../models/gpt-6.1-luna.md` returns 404, while [gpt-6-luna](https://developers.openai.com/api/docs/models/gpt-6-luna.md) and `gpt-6.1-sol` return 200.
- The spec should name `gpt-6-luna` (cheap) or `gpt-6.1-sol` (closer to GPT-6.1). Docent routes OpenAI through the Responses API (`provider_registry.py`, lines 181-191). OpenAI's docs say Responses supports reasoning plus function calling for `gpt-6-luna`, which avoids the Chat Completions limitation.

**Reasoning setting on Anthropic models** (`docent/_llm_util/providers/anthropic.py`, `_apply_thinking_config`, lines 237-283):
- **When an effort is set**, Docent sends `thinking={"type":"adaptive","display":"summarized"}` and `output_config={"effort": low|medium|high}`. `minimal` maps to `low`. This is the parameter surface Opus 5.5 and Sonnet 5.5 expect: `budget_tokens` and `disabled` both return 400 on these models.
- **Effort is limited to `minimal|low|medium|high`.** The `Literal` is in `ModelOption` (`preference_types.py`) and `read()`. The models also accept `xhigh` and `max`, which Docent cannot select.
- **With no effort set**, Docent omits `thinking`. Both models then run adaptive thinking at their API default: medium for Opus 5.5, high for Sonnet 5.5.
- **The `claude-sonnet-5` "explicitly disable" rule does not misfire on `claude-sonnet-5-5`.** The boundary matcher only extends names by date suffixes. So no `{"type":"disabled"}` is sent, which would be a 400 on Sonnet 5.5.
- **Recommendation: always set the effort explicitly.** For the record, the Opus 5.5 default is `medium`, not `high`.
- **Temperature is dropped** for models not on a known-flexible list, which covers both models (`requires_default_sampling_params`).

**BYO keys**
- **How keys are stored.** The OSS server stores one key per provider in `model_api_keys`. `PUT /model-api-keys` accepts only `openai`, `anthropic` and `google` (TransluceAI/docent `docent_core/docent/server/rest/router.py`, lines 1216-1230). There is no OpenRouter BYO key there. The hosted version may differ.
- **Which models show up.** `merge_models_with_byok` returns the platform default list, adds BYOK-only models for providers the user has a key for, and flags `uses_byok = provider in user_keys` (`docent/_llm_util/providers/preference_types.py`).
- **Inference: these models work without BYO keys.** The unauthenticated list shows Opus 5.5, Sonnet 5.5 and gpt-6-luna with `uses_byok: false`. That makes them platform-default models, usable on Transluce's quota. With an Anthropic or OpenAI key saved, the same entries should flip to `uses_byok: true` and bill our key. This assumes the hosted server matches the SDK copy of this function.
- **Concurrency.** Reading plans fan out with default concurrency 200 (`DEFAULT_READING_PLAN_CONCURRENCY`, `docent/data_models/reading.py`). That load lands on our provider rate limits under BYOK.
- **Not documented.** The docs site does not describe BYOK for readings at all. The only provider-key text covers running legacy judges locally ([legacy rubrics](https://docs.transluce.org/legacy/rubrics.md), [manage rubrics](https://docs.transluce.org/sdk/rubrics/manage.md)).

## (c) Export

**DQL**
- **Row cap.** Every query is capped at 10,000 rows by the server. The response carries `truncated` and `applied_limit` fields. Pagination uses LIMIT/OFFSET ([DQL](https://docs.transluce.org/analysis/dql.md), [exporting](https://docs.transluce.org/analysis/exporting.md), [execute_dql](https://docs.transluce.org/sdk/dql/execute.md)).
- **SDK parameters.** The SDK also exposes `max_rows`. `ensure_latest_results=True` forces the query onto Postgres rather than a possibly lagging parquet replica; use it on the final export (`docent/sdk/_dql.py`, lines 34-85).
- **Pagination.** Order by a unique key (`id`) so pages are stable.
- **Bytea columns.** `transcripts.messages` and `transcripts.metadata_json` are bytea. Inside DQL, wrap them in `convert_from(col,'UTF8')::jsonb`. In exported rows, `json.loads` the value if it arrives as a string ([DQL schema](https://docs.transluce.org/sdk/dql/schema.md)). For message-level statistics, export the whole transcript and parse it locally; that is simpler than message-level DQL.
- **Tables.** Documented: `agent_runs`, `transcripts`, `transcript_groups`, `judge_results`. `reading_results` and `reading_result_links` (columns `result_id`, `reading_id`) appear in the [analysis plans](https://docs.transluce.org/analysis/analysis-plans.md) example. No labels table is documented for DQL.

**REST, without DQL**
- **Reading results.** `get_reading_results(collection_id, reading_id, limit=None, include_output=True)` returns `output`, `error`, `arguments_dict`, `input_tokens`, `output_tokens` and `served_provider`. It has no cursor or offset; whether the server caps it is unknown (`docent/sdk/_readings.py`, lines 198-233; `ReadingResult` in `docent/data_models/reading.py`).
- **Agent-run labels.** `get_labels(..., scope="visible")` returns a plain list. `scope="all"` returns an admin-only attributed review, paginated by cursor at 1-200 agent runs per page (`docent/sdk/_labels.py`, lines 217-259).
- **General labels.** The SDK can create, get by id, update and delete them, and list *sets*. It has **no "list labels in a set"** method (`docent/sdk/_general_labels.py`). Keep the IDs returned by `create_general_label`, or treat our own store as the record.
- **Implication.** Keep our own copy of every label we write, and export reading results per reading ID. At our scale (thousands of sessions, tens of thousands of episodes), the 10k cap only means a few pages per table.

## (d) Multi-rater labels

**Agent-run label sets: supported.** Everything below is SDK-only in 0.1.87 and missing from the docs site (`docent/sdk/_labels.py`, lines 28-135):
- `create_label_set(..., is_blind=True, assignees=[...])` hides each rater's labels from the others ("Whether labels are hidden from other labelers").
- `set_label_assignments` sets up to 10,000 assignees and requires collection admin. Assignment does not share the collection; share it separately.
- `set_label_set_blind(False)` reveals the set and "preserves each answer and its author".
- `Label` carries `created_by` and `creator_email` (`docent/data_models/judge.py`).
- `get_labels(scope="all")` gives the admin an attributed, per-agent-run paginated review. That is the input for kappa.

**Transcript-slice general labels: workaround.**
- `GeneralLabel` has `created_by` (`docent/data_models/general_label.py`). There is no blind flag, no assignees, and no list endpoint.
- Options:
  - One general label set per rater, with the same schema, named per rater, labelling identical slice targets. Kappa is computed offline.
  - Ingest each Episode as its own `AgentRun` (keeping `session_id` and the original indices in metadata) and use a blind label set. This also keeps the UI blind.

**Neither path computes agreement.** As `docent-assessment.md` already noted, kappa is computed offline.

## Newly surfaced questions

1. **Spec correction.** "GPT-6.1 Luna" is not a real model. Choose `gpt-6-luna` or `gpt-6.1-sol`, and update the spec and any decision text that names it.
2. **Is BYOK needed?** If Opus 5.5 and Sonnet 5.5 are platform-default models, BYOK is a choice about cost, quota and billing control, not about access. Ask Transluce: what is the free quota, what does it cost above the quota, and do BYOK calls still pass through Transluce servers? They do: readings run server-side, so transcripts and prompts go to Transluce either way.
3. **No xhigh/max effort.** If the judge design calls for `xhigh` or `max` on Opus 5.5, Docent cannot do it; the caps are `low|medium|high`. Either accept `high`, or run that judge outside Docent.
4. **Stability of SDK-only features.** Scripted readings, blind label sets and attributed label export are in the SDK but not the docs. Confirm with Transluce that they are supported before relying on them for kappa.
5. **Hosted-only lock-in grows.** Slices, DQL and blind labels are all absent from the OSS server, which makes "self-host as fallback" weaker than `docent-assessment.md` implied.
6. **Server caps on REST exports.** It is unknown whether `get_reading_results` and `get_labels(scope="visible")` cap their output. Test with a 10k-plus reading before relying on them.
