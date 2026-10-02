# Spike: sharpening questions for Selena Zhang (Transluce overselling study)

Date: 2026-10-02. Read-only. All data came from the public Docent collection `2588573f-daa3-4130-9bce-e60ba5db04c1` (anonymous REST and DQL) and the blog's PNG figures. Files in this directory:

| File | Contents |
|---|---|
| `results.json` | REST dump of final reading `299c8276…` (5,055 rows) |
| `readres.json` | DQL rows for final, dev (`b139c6f8…`) and verifier (`da081023…`) readings, with `created_at` |
| `runs.json` | Per-run metadata (5,058 runs) |
| `me_results.json` | Monitor-evasion final reading `997380fc…` (used as a cross-check) |
| `roles.json` | Message-role counts for 412 candidate runs (all Codex runs, plus Claude Code runs with judge input under 12k tokens, a null model, or a `<synthetic>`-only model) |
| `excluded_28_no_assistant.json` | The 28 runs that the inferred filter drops |
| `pending_and_big.json` | The 239 pending run IDs, and the 21 results over 1M input tokens |
| `ci_compare.json` | Measured error bars compared with each CI method |
| `assign.py`, `ci.py`, `caps.py`, `dql.py` | Model-assignment rules, CI methods, figure cap extraction, DQL helper |

**Headline:** the blog's numbers are reproduced exactly from the public labels. That covers the overall n (4,788 overselling, 4,990 monitor evasion), all twelve per-model n values, every published percentage, and every error bar (to within a fraction of a pixel). Three rules do it: (1) drop sessions with no assistant message, (2) assign each session to its highest-tier, latest Claude model after dropping `<synthetic>`, and (3) use Wilson 95% intervals with no clustering. What remains are confirmation questions, not open unknowns.

---

## Q1. Headline denominator (4,788 vs 4,816)

**Facts**
- The final reading has 5,055 rows: 4,816 completed, 239 pending, 0 errors.
- The blog's 34.7% present, 32.9% not severe and 1.8% severe at n = 4,788 hold only if all 28 dropped sessions are negatives. 1,660/4,788 = 34.67%, 1,573/4,788 = 32.85% and 87/4,788 = 1.82%. Dropping any positive pushes "not severe" down to 32.8%.
- Exactly 28 completed sessions have **no assistant message** in their Docent transcript: 23 `gpt-5.3-codex-spark` Codex runs (system prompt plus one user message only), 4 Claude Code runs with `model = null` (one user block), and 1 `gpt-5.4` Codex run (`133da30b-eed6-4f04-93fc-776610f2d184`). All 28 are judged negative. Removing them gives n = 4,788, 1,660 present and 87 severe, which matches the blog exactly.
- Cross-check: the same 28 runs are completed in the monitor-evasion reading (5,018 completed). Removing them gives **4,990**, which is the blog's monitor-evasion n, at 14.7% present and 1.9% severe. Both also match the blog.
- Rejected candidates: a time snapshot (the 4,788th result by `created_at` sits on a batch boundary, 2026-07-31T01:59:57, but that subset gives 34.4%, not 34.7%); dropping Codex (205); dropping results over 1M input tokens (21, of which 14 are positive); dropping sessions with no human turn.

**Caveat:** I checked role counts only for 412 candidate runs, not all 4,816. A Claude Code run with a large prompt and no assistant reply could have been missed. But any extra drop would break the exact match on both behaviors, so this is unlikely.

**Confidence:** high. The rule reproduces two independent denominators and six published percentages.

**Question for Selena:** "We reproduce n = 4,788 (overselling) and n = 4,990 (monitor evasion) exactly by dropping the 28 completed sessions whose transcript has no assistant message (23 codex-spark, 4 null-model Claude Code, 1 gpt-5.4). Is that the filter you applied, and was it applied after judging rather than before?"

## Q2. Multi-model sessions and per-model n

**Facts**
- `metadata.model` is a list for 739 of the 4,816 completed runs. Examples: `["<synthetic>","claude-opus-4-6"]` (466), `["claude-haiku-4-5…","claude-opus-4-6"]` (90), `["<synthetic>","claude-sonnet-4-6"]` (42), and `["claude-opus-4-6","claude-opus-4-7"]` (6).
- **Rule "top-tier, latest":** ignore `<synthetic>` and non-Claude names, then pick the highest tier (Opus > Sonnet > Haiku), and break ties by the latest version. This reproduces **all six** overselling n values and **all six** monitor-evasion n values exactly (Haiku 4.5 37/36, Sonnet 4.5 101/103, Sonnet 4.6 487/495, Opus 4.5 166/168, Opus 4.6 3,741/3,928, Opus 4.7 46/48). The present, not-severe and severe percentages also match to one decimal.
- Other rules and their residuals against the published overselling n (Haiku, Son4.5, Son4.6, Op4.5, Op4.6, Op4.7):
  - last non-synthetic model: 0, +12, +25, −11, −27, 0
  - single family only (exclude mixed): 0, −1, −32, −11, −143, −6
  - drop Haiku if mixed, then single family: 0, 0, 0, −11, −27, −6
  - any family present: +151, +12, +25, +1, +6, 0
- Key distinguishing cases: Opus 4.5 + Sonnet 4.5 mixes (11 runs) go to Opus 4.5, and Opus 4.6 + 4.7 mixes (6 runs) go to Opus 4.7.

**Inference:** "highest-tier model" and "main-loop model, with subagents on smaller models" give the same result on this data. I could not test "majority of assistant turns" without per-message model fields, so I can't rule it out. It would have to agree on all 739 mixed runs to match.

**Confidence:** high that the rule reproduces their grouping; medium on what they intended the rule to mean.

**Question for Selena:** "We match every per-model n by assigning a mixed session to its highest-tier model, Opus > Sonnet > Haiku, then the latest version, ignoring `<synthetic>`. For example, Opus 4.5 + Sonnet 4.5 counts as Opus 4.5, and Opus 4.6 + 4.7 counts as Opus 4.7. Is that your rule, or did you mean 'main-loop model' and it happens to coincide?"

## Q3. CI method

**Facts**
- The bundle has no numeric CIs, only PNGs. I measured the cap centroids of all 11 SWE-chat error bars in figures 01–03 (gridline calibration: 4.72, 11.8 and 118 px per percentage point), plus the Transluce monitor-evasion severe bar (0/3,671).
- Method fit, in sum of worst-endpoint errors in half-pixel units across 11 bars (lower is better): **Wilson 1.4**, Agresti–Coull 10.0, Jeffreys 26.1, Clopper–Pearson 47.8, iid bootstrap 49.2, Wald 95.1, **user-clustered bootstrap 598.6**.
- Examples (measured vs Wilson): Opus 4.7, 8/46: [9.07, 30.72] vs [9.09, 30.72]. CP would be [7.82, 31.42] and Wald [6.44, 28.34]. Haiku, 23/37: [46.10, 75.94] vs [46.10, 75.94]. Severe overall, 87/4,788: [1.48, 2.23] vs [1.48, 2.24]. Transluce severe, 0/3,671: [0.00, 0.10] vs Wilson [0, 0.10]. Wald would give zero width there.
- A user-clustered bootstrap gives much wider intervals: overselling present overall [31.9, 37.5] against Wilson [33.3, 36.0], and monitor evasion [9.9, 21.4] against [13.8, 15.7]. One user (user A) accounts for 20 of the 84 dev-severe cases.

**Confidence:** high that the bars are Wilson 95% on per-session binomials with no clustering.

**Question for Selena:** "Your error bars match Wilson 95% intervals that treat sessions as independent to sub-pixel accuracy. Did you consider clustering by user? A user-clustered bootstrap roughly doubles the overall overselling interval ([31.9, 37.5] vs [33.3, 36.0]), and widens monitor evasion about 6-fold."

## Q4. Pending, errors, over-1M-token results, judge params

**Facts**
- 239 pending, no output, all created 2026-07-31T03:40–03:41, the time the final reading was created. 0 errors. `served_provider` is null on all 5,055 rows. The per-row model is `anthropic/claude-opus-5`, effort `high`, `max_new_tokens` 16,000, `rollout_index` 0. There is no temperature field.
- The pending sessions are long. Median assistant turns are 343 against 65 for completed, and median duration is 5.5 h against 21 min. By rule_top model: Opus 4.6 207, none or non-Claude 12, Sonnet 4.6 10, Sonnet 4.5 4, Opus 4.7 3, Opus 4.5 3. By agent: Claude Code 231, Codex 8. Of these, 34 are also pending in monitor evasion, which has 37 pending.
- Results over 1M input tokens: 21, all `completed`, 1,023,166–1,808,348 tokens. 14 are positive (67%, against the 34.7% base rate) and 1 is severe (`3de4bebb-9ae2-482c-9696-df4a08612dd8`, Sonnet 4.5). All 21 are inside the 4,788. The full list is in `pending_and_big.json`. Another 33 results fall between 800k and 1M.
- Dev reading `b139c6f8…` has the same 5,055 rows, of which 4,641 are completed. The final reading reuses those 4,641 result IDs and adds 175 more completed between 07-30 and 07-31.

**Inference:** the judge never finished the pending rows, most likely because they were too long. Reading inputs over 1M tokens on a 1M-context model suggests that Docent splits or summarizes the session, or that `input_tokens` sums more than one call. That cannot be seen from the data.

**Confidence:** high on the counts; low on the mechanism.

**Question for Selena:** "239 calls are still pending, mostly very long Opus 4.6 sessions (median 343 assistant turns), and 21 completed results report 1.02M–1.81M input tokens. How does Docent handle sessions beyond Opus 5's context: truncation, chunking, or something else? Should the 239 be read as 'excluded for length' in the paper's denominator?"

## Q5. Which 42 of the severe cases were verified

**Facts**
- The verifier's DQL hard-codes 42 run IDs and joins them to the **dev** reading `b139c6f8…` results. It was created 2026-07-30T00:44. At that point the dev reading had **84 severe** cases. The verifier covers exactly half (42/84), and all 42 are drawn from those 84. The final reading has 87 severe: the 84 plus 3 that completed later (07-30 19:00 to 07-31 02:00).
- The ID list is not sorted by run ID. Verified cases are not tied to judge time (07-29 07:00: 6 of 8; 18:00: 27 of 64; 21:00: 9 of 12).
- **The selection looks user-stratified.** No user has more than 2 verified cases. Every user with 1–2 severe cases has all of them verified (24 singletons, 5 users with 2). The capped users are user A (2 of 20 verified), null `user_id` (1 of 20), user B (2 of 4), user C (2 of 3) and user D (1 of 3). A strict "at most 2 per user" rule would select 44, not 42. The gap is user D (1, not 2) and null user (1, not 2).
- Outcome: 34 cases (plausible = false, invalidates = false) and 8 (plausible = true, invalidates = false). None overturned.

**Inference:** a per-user cap of about 2, with 42 = 84/2 possibly a target size. The two shortfalls may be manual picks or random. Low-to-medium confidence on the exact rule.

**Question for Selena:** "The 42 verified cases are half of the 84 dev-reading severe labels, and no user contributes more than 2 (e.g. 2 of user A's 20). Was the sample capped per user, and was the verifier ever meant to filter the published labels, or only to stress-test the rubric?"

## Q6. Prevalence recomputed from public labels (after the Q1 filter, with the Q2 rule)

| Group | n | Present | Not severe | Severe | Blog |
|---|---|---|---|---|---|
| Overall overselling | 4,788 | 34.67% (1,660) | 32.85% | 1.82% (87) | 34.7 / 32.9 / 1.8, n = 4,788 ✓ |
| Haiku 4.5 | 37 | 62.2 | 48.6 | 13.5 | 62.2 / 48.6 ✓ |
| Sonnet 4.5 | 101 | 54.5 | 48.5 | 5.9 | 54.5 / 48.5 ✓ |
| Sonnet 4.6 | 487 | 39.6 | 37.8 | 1.8 | 39.6 / 37.8 ✓ |
| Opus 4.5 | 166 | 34.3 | 33.7 | 0.6 | 34.3 / 33.7 ✓ |
| Opus 4.6 | 3,741 | 34.5 (1,292) | 32.9 | 1.7 | 34.5 / 32.9 ✓ |
| Opus 4.7 | 46 | 17.4 | 17.4 | 0.0 | 17.4 / 17.4 ✓ |
| Monitor evasion overall | 4,990 | 14.7 (735) | 12.8 | 1.9 (94) | 14.7 / 12.8 / 1.9 ✓ |

Also: `tough_call` is true for 1,162 of 1,660 positives and 487 of the negatives. That is unchanged from the earlier research note.

**Confidence:** high. The labels as published today are the labels behind the blog. No labels changed between the blog and today.

**Question for Selena:** none needed beyond Q1 and Q2. Optionally: "Confirm the published per-transcript labels in reading 299c8276 are final, so a snapshot taken today equals the blog's."

## Not done (cost)
- I did not test "majority of assistant turns" model assignment, because it needs per-message model fields across all 739 mixed transcripts (about 4,800 run fetches).
- I did not check role counts for all 4,816 runs (see the Q1 caveat).
- I did not fit the Transluce-collection bars apart from the zero-count severe bar, because their k values aren't public here.
