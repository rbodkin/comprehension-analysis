# Docent source investigation: cloning, context overflow, request params, OpenRouter, concurrency, BYOK

Date: 2026-10-02. Read-only.

## Sources

- **SDK**: PyPI `docent` 0.1.87, the latest release. Wheel sha256 `eadf3af6…c25ee`, unpacked at `wheel/sdk/`. Paths below are relative to `wheel/sdk/`.
  - The SDK ships the shared LLM engine (`docent/_llm_util/`). The hosted server injects its own rate limiter into that engine (`rate_limiter.py:1-23`, `llm_svc.py:677-679`), which implies the server runs this engine for its LLM calls.
- **OSS server**: github.com/TransluceAI/docent `main` @ `8ab199c` (2026-09-04, a dependabot merge), cloned at `oss/`.
  - **It is stale.** Its bundled SDK is `0.1.18-alpha` (`oss/docent/pyproject.toml:4`).
  - It has **no readings, reading plans, DQL, BYOK reading routes, clone-collection route or AIMD rate limiter**. `oss/docent_core/docent/server/rest/` holds only chart, chat, refinement, router, rubric and telemetry.
  - **Everything about how the reading worker runs is therefore server-only and closed source.**
- **Docs**: docs.transluce.org, mirrored into `docs/` (47 pages from llms.txt).
- **Live catalog**: `GET https://api.docent.transluce.org/rest/reading/reading-models` (1,220 entries).
  - `anthropic/claude-opus-5` and `openrouter/anthropic/claude-opus-5` are both listed with a 1,000,000-token context window and `uses_byok:false`.

"Server-only" below means the code that decides this is not in any public tree.

---

## 1. Copying agent runs between collections

**There are two supported paths.**

**(a) Server-side clone of a whole public collection** (the most faithful path):

```python
own_id = client.ensure_analyzable_collection(public_cid)
```

- What it does:
  - Calls `POST /{cid}/ensure-own-copy`, then polls `/{cid}/clone_jobs/{job}`.
  - Returns your existing clone if you already have one.
  - Repoints `default_collection_id` to the clone.
- Evidence: `docent/sdk/_collections.py:495-601`. The docstring (502-531) says the server clones a public collection you do not own.
- **The clone logic itself is server-only.** OSS has no `ensure-own-copy` or `clone_jobs` route (grep finds none). What gets copied is therefore undocumented: transcripts, groups, metadata and created_at are not confirmed, and neither are comments, labels or readings.

**(b) Client-side round trip**:

```python
get_agent_run(src_cid, id)        # _agent_runs.py:14-35
clone_agent_runs_with_random_ids  # data_models/util.py:10-157, documented in docs/ingestion__sdk.md:335-344
add_agent_runs(dst_cid, ...)      # _collections.py:155-263
```

- **Kept**:
  - AgentRun `name`, `description`, `metadata`.
  - Transcript `name`, `description`, `created_at`, `messages` (deep-copied), `metadata`.
  - TranscriptGroup `name`, `description`, `created_at`, `metadata`.
  - The parent-group and transcript-to-group references, rewired to the new IDs.
- **Lost**:
  - **All IDs.** New UUIDs are mandatory. `validate_no_user_set_ids` rejects any caller-set ID (`sdk/_client_util.py:57-87`).
  - `TranscriptGroup.agent_run_id`, which is not copied (`util.py:86-91`); the server presumably sets it on ingest.
  - Comments and labels: they are not part of `AgentRun`.

**Why the prompt-relevant fields matter for fidelity:**

- **Prompts carry no UUIDs.** Rendering uses aliases (`T0`, `T0B5`, `R0M`), not UUIDs (`transcript.py:356-420`; `agent_run.py` `to_text`). New IDs do not change prompt text.
- **Order is by `created_at`.** Transcript and group order in the render is sorted by `created_at`, with `datetime.max` used when it is missing (`agent_run.py:276-295`). So `created_at` must survive the copy, and it does.
- **Name filters fall back to IDs.** Context-config name filters (`transcript_names`, `transcript_group_names`) match on name, falling back to the ID (`agent_run.py:540-575`). An unnamed transcript or group targeted by a filter would stop matching after the IDs are regenerated.
- **Comments render into prompts.** `Transcript.to_text` takes `block_content_comments` and metadata comments. Comments are not carried by either path as far as the SDK shows.

**Recommendation:**

- Use `ensure_analyzable_collection` on Transluce's public collection, then verify the copy. Spot-check with DQL row counts per table, plus a hash of `messages`/`metadata_json` per run against the source.
- Fall back to path (b) only if the clone differs from the source.
- **Ask Transluce** exactly what the server clone copies: comments, labels, readings, created_at, ordering.

## 2. Context overflow

**In the SDK and shared engine there is no truncation, splitting or summarizing for readings.**

- **Rendering has no length handling.**
  - `LLMContext.to_str(token_limit=...)` accepts a token limit but never uses it (`sdk/llm_context.py:827-884`).
  - `render_segments` and `_render_item` (886-973) have no limit at all.
- **The old splitting and truncation helpers are dead code in 0.1.87.** `_tiktoken_util.truncate_to_token_limit` keeps the head and drops the tail (`data_models/_tiktoken_util.py:12-20`). It and `group_messages_into_ranges` are referenced nowhere in 0.1.87.
  - The old OSS `AgentRun.to_text` split long runs into "partial agent run" chunks (`oss/docent/docent/data_models/agent_run.py:173-200`). Current code does not do this.
- **An oversized prompt becomes an error.**
  - An Anthropic 400 containing "prompt is too long" or "context limit" becomes `ContextWindowException` (`providers/anthropic.py:286-295`). It is **not retryable** (`anthropic.py:97-112`).
  - The result therefore becomes an error with `error_type_id="context_window"` (`_llm_util/data_models/exceptions.py:49-51`).
  - OpenRouter maps 400s that say "context limit/length/window" the same way (`providers/openrouter.py:35-39, 217-220`).

**How `input_tokens` can exceed 1M: validation retries are summed (hypothesis).** *Checked against the data on Oct 2 and not supported: the 21 results have a median of about 9.4k output tokens, against about 8.7k for results just under 1M, not the roughly 2× that summed retries would give. Still open with Transluce.*

- `_parallelize_calls` runs up to `MAX_VALIDATION_ATTEMPTS = 3` calls per input (`llm_svc.py:70, 446`).
- It accumulates the usage of *every* call, `accumulated_usage.add(result.usage)` (`llm_svc.py:432-435, 469`), and overwrites the final result's usage with that sum (`llm_svc.py:602-606`).
- `UsageMetrics.add` sums each key (`data_models/llm_output.py:52-61`).
- **What this means for 1.02M–1.81M:**
  - Each call stays under 1M, so neither call is rejected.
  - With `retry_with_feedback`, each retry appends the failed output plus a "Your previous output failed validation…" user turn (`llm_svc.py:540-547`; `judges/util/validation_logging.py:47-51`), so a retry's prompt is slightly larger than the first.
  - The reported number is therefore roughly 2× a 0.5–0.9M prompt, or 3× a smaller one.
- **Other explanations look unlikely:**
  - Anthropic `input` excludes cache tokens, which are stored separately as `cache_read`/`cache_write` (`anthropic.py:474-479, 675-680`).
  - No `cache_control` is sent anywhere in the SDK.
- **The reading worker itself is server-only.** We cannot see whether it calls `get_completions` with a `validation_callback` and `retry_with_feedback=True`, or how it maps `usage` to `ReadingResult.input_tokens` (`data_models/reading.py:161-186`).
  - The local judge does use exactly that pattern (`judges/impl.py:229-238`).
  - `ReadingResult.item_token_estimates` exists (`reading.py:185`), but nothing in the SDK uses it. It suggests a server-side pre-flight estimate whose behavior is unknown.
- **Check in the data:** compare `output_tokens` on those 21 results against the rest; they should be about 2× if this explanation is right. Also check whether those results still have a valid `output`.

**Confidence:** high on the SDK mechanics; medium that this is the cause. **Ask Transluce** to confirm both the summing and that no server-side truncation exists.

## 3. Prompt wrapping and request params (anthropic, `claude-opus-5`, effort high, max_new_tokens 16000)

**Request built by the shared engine** (`providers/anthropic.py:512-620`, `_apply_thinking_config` 237-283; `model_registry.py`):

| Parameter | Value sent | Source |
|---|---|---|
| `model` | `claude-opus-5` | |
| `max_tokens` | 16000, passed straight through (the reading default is 8192) | `reading.py:31`; `_readings.py:405` |
| `thinking` | `{"type":"adaptive","display":"summarized"}`. `claude-opus-5` is not on the legacy list, so it is treated as adaptive. | `model_registry.py:83-112` |
| `output_config` | `{"effort":"high"}` | |
| `temperature` | **Never sent.** `claude-opus-5` is not on `_FLEXIBLE_SAMPLING_MODELS`, so `requires_default_sampling_params` is true and temperature is popped whatever the caller passed. The API default of 1.0 applies. | `model_registry.py:101-120`; `anthropic.py:264-271` |
| `system` | Only if the message list contains a system message | `anthropic.py:128-185, 581-582` |
| `anthropic-beta` header and `extra_body.output_format` | `structured-outputs-2025-11-13` and `{"type":"json_schema","schema":...}`, but only if the caller passes a `response_format` | `anthropic.py:86, 208-224` |
| Streaming | Non-streaming at 16000, unless the Anthropic SDK's own nonstreaming guard requires a stream, in which case it streams | `anthropic.py:499-563` |

**Retries:** client SDK retries are 0 (`anthropic.py:622-627`). The retry budget is `max_retries + 1` attempts with backoff factor 3 (`anthropic.py:376-383`; `common.py:227-301`).

**Server-only:**

- whether readings send a system prompt;
- whether readings pass a `response_format` or rely on validation retries;
- the timeout;
- the temperature the worker passes (irrelevant for anthropic/opus-5, because it is dropped);
- any wrapper text the server adds.

**What the SDK shows about wrapper text:**

- **Template text** is sent as given, after `dedent` (`_readings.py:532-534`).
- **Separators**: segments are joined with blank-line or space separators (`llm_context.py:72-90, 886-935`).
- **Item rendering** uses `<|agent run metadata R0M|>`-style tags (`agent_run.py:155-176`). Metadata is excluded by default (`EXCLUDE_ALL_GLOB_FILTER`).
- **A candidate system prompt exists:** `LLMContext.get_system_message(interactive, include_citations)` returns "You are tasked with analyzing transcripts of AI agent behavior…" plus a long citation-instruction block (`llm_context.py:975-1002`; `transcript.py:158-175`). Whether readings use it is server-only. Our own analysis uses citations, so it would be plausible.

**Ask Transluce** for one fully rendered request (system plus user) from their reading. It is the only way to replicate the input exactly.

## 4. OpenRouter (`openrouter/anthropic/claude-opus-5`)

**Request mapping** (`providers/openrouter.py:181-195, 235-278`; `providers/openai.py:645-756, 273-330`):

- **Endpoint:** OpenAI-compatible Chat Completions at `https://openrouter.ai/api/v1`.
- **Effort and thinking:** effort is sent as `extra_body.reasoning = {"effort":"high"}`. There is no `thinking` or `output_config`; how OpenRouter translates effort into Anthropic thinking happens on OpenRouter's side.
  - Effort is dropped only if OpenRouter's `/models` catalog says the model has no reasoning params (`openrouter.py:108-144`).
- **Max tokens:** `max_tokens=16000` (or `max_completion_tokens`, if the catalog lists it for the model; `openrouter.py:147-161`).
- **Routing:** `provider = {"data_collection":"deny","require_parameters":true}`. With `served_providers`, `only` is added as well.
- **Temperature: an asymmetry.** It is omitted only if it equals 1.0. A non-1.0 value is sent to OpenRouter, because `requires_default_temperature` lists only OpenAI models (`model_registry.py:193-201`). Anthropic-direct drops it.

**Usage recording:**

- `input` is `usage.prompt_tokens` (`openai.py:1040-1044`; streaming 617-621).
- `served_provider` is recorded (`reading.py:170-171, 184`).

**Would `input_tokens` match the anthropic provider? Approximately, not exactly.**

- **Different count.** Anthropic-direct records `usage.input_tokens`, which excludes cache read/write. OpenRouter's `prompt_tokens` is OpenRouter's count, which for Anthropic upstreams is the native count *including* any cached tokens.
- **Different wire format.** The request goes through a different serialization: OpenAI-format messages, `response_format` and reasoning, translated by OpenRouter. That changes the overhead tokens slightly.
- **Same summing.** Validation-retry summing applies identically on both paths.
- **Rough size of the gap:** expect agreement within a small overhead (hundreds of tokens) for the same rendered prompt, not byte-identical counts. Behavior on OpenRouter's side is not in Docent's code; this is inference.

## 5. Concurrency and rate limits

**SDK control:**

- Set it per plan approval:

  ```python
  client.flush(auto_approve=True, max_concurrency=N)
  ```

- `N` runs from 1 to `MAX_READING_PLAN_CONCURRENCY = 1000`. It requires `auto_approve=True` (`_readings.py:782-819`) and is sent as `max_concurrency` in `POST /reading/{cid}/reading-plan/{plan}/approve` (`_readings.py:980-1003`).
- The default is `DEFAULT_READING_PLAN_CONCURRENCY = 200` (`reading.py:34-41`).
- There is no per-reading setting. Concurrency applies to the steps approved in that call.

**Engine retries:**

- **429 handling:** a 429 becomes `RateLimitException` carrying `retry-after`/`retry-after-ms` (`anthropic.py:296-297`; `common.py:151-185`).
- **Retry budget:** `max_retries=2`, so 3 attempts (`llm_svc.py:711`).
- **Backoff:** full-jitter exponential (factor 3: 3s, 6s, …), floored at Retry-After but capped at 20s per sleep (`common.py:82, 259-289`). Retry-After values are clamped to 300s (`common.py:71`).
- **Fallback:** when attempts are exhausted, the engine rotates to the next model option if one exists (`llm_svc.py:755-874`).

**Server rate limiting (server-only):**

- The server injects a Postgres-backed AIMD limiter, bucketed per (provider, model, key). A BYOK key gets its own bucket, keyed by a hash (`rate_limiter.py:1-23, 113-141`; `llm_svc.py:785-792`).
- It reserves estimated prompt tokens plus max_new_tokens, at about 4 characters per token (`llm_svc.py:216-229`; `rate_limiter.py:40-48`), and waits at most 15s for admission (`llm_svc.py:94-104`). Its limits are not visible to us.
- The service semaphore defaults to 100 (`llm_svc.py:84-85`). Plans raise it to 200.

**Ask Transluce** for the platform-key limits and any per-user cap.

## 6. BYOK

**Which providers accept user keys:**

- The engine supports `anthropic`, `google`, `openai`, `azure_openai` and `openrouter` (`provider_registry.py:130-136`). Each takes a per-provider key override (`llm_svc.py:787`).
- **OpenRouter key handling is mixed:**
  - The client accepts a key (`openrouter.py:164-178`), and there is an `is_openrouter_api_key_valid` helper (`openrouter.py:327-342`), which suggests the hosted server accepts OpenRouter keys.
  - The stale OSS `PUT /model-api-keys` accepted only openai, anthropic and google (prior research, `router.py:1216-1230`).
  - **The hosted list is server-only.**
- **The live catalog** marks `uses_byok` per model for the current user (`preference_types.py:105-116`).

**Quota:**

- `DocentUsageLimitException` says: "Free weekly usage limit reached. Add your own API key in settings or email docent@transluce.org…" (`_llm_util/data_models/exceptions.py:64-69`). That implies BYOK calls do not count against the free weekly limit.
- The accounting itself is server-only. The engine only calls a server-supplied `completion_callback` that "may throw if we just exceeded limit" (`llm_svc.py:629-638`).

**Ask Transluce** for the quota size, and to confirm that BYOK is exempt.
