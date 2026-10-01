# Obtaining a recent SWE-chat snapshot

Resolves issue #23 (child of #2). Researched 2026-10-01.

How each claim was established:
- **Documented** means a primary source states it. The source is cited inline.
- **Measured** means I computed it from Git or GitHub metadata today.
- **Inferred** means I reasoned it from the evidence and did not verify it directly.

What I did and did not touch:
- I listed ref names (`git ls-remote`) and read commit metadata (dates, authors, and the `Entire-Session` / `Entire-Agent` trailers in checkpoint-branch commit messages) through the GitHub API.
- I did **not** download any post-April transcript content. An attempt to fetch a 60-checkpoint sample for a format check was blocked by the agent's PII-handling guard. That is the right default until the PI decides on consent/IRB (see §1). The format answer in (c) therefore comes from Entire's own docs plus the HF release.

## Short answer

- **(a) Source.** The live data comes from Entire.io checkpoint data that developers push to public GitHub repos. SALT finds those repos itself, through GitHub Code Search, and harvests them. **There is no SALT-specific consent.** The only "opt-in" is the developer enabling Entire and pushing checkpoints to a public remote. SALT's IRB judged the study exempt. We could collect the same data technically. Doing so needs our own ethics determination; the details and constraints are in §1.
- **(b) Newer snapshots.** SALT has published nothing since April:
  - HF has a single revision, `f66cca95` (2026-04-29).
  - The GitHub repo has had no commits since 2026-04-24 and still says "data and code coming soon".
  - SALT has never replied on any HF discussion, including an open NUL-byte bug report from July.
  - The swe-chat.com "+340 sessions / 7 days" deltas are hardcoded into static HTML, next to the same headline totals the April paper reports. No API or JSON feed exists.
  - The paper promises "frequent" updates. I found no data-request process; the only contact the card gives is for removal requests.
- **(c) Format.** The format has shifted, both in where the data lives and in what it contains:
  - **Location.** Since mid-2026, new Entire repos store each checkpoint as its own ref, `refs/entire/checkpoints/<shard>/<ULID>`, instead of on the `entire/checkpoints/v1` branch. The tree layout inside a checkpoint is unchanged (`metadata.json`, `<n>/full.jsonl`, `prompt.txt`), and it gains `transcript.jsonl` (compact) and `tasks/` subagent records.
  - **Pipeline.** SALT's published pipeline reads only "the metadata branch" (`v1`). Inferred: SALT's pipeline as described would miss every refs-backed repo.
  - **Redaction.** Raw checkpoints carry only Entire's own redaction: always-on secret detection, with PII redaction opt-in. The HF release adds Presidio (PII) and TruffleHog (secrets), which SALT runs. A self-collected snapshot would have to repeat that step.
- **(d) Volume after 2026-04-19.** Measured from metadata, in the repos I could discover:
  - **About 1,550 new Claude Code sessions on `v1` branches**, from about 75 committer identities in 70 repos.
  - **Plus an estimated 700 to 1,500 on per-checkpoint refs.** 5,327 ULID checkpoints exist, all dated Aug–Oct; Claude Code's share of those is not measured.
  - **Total: roughly 2,000 to 3,000 Claude Code sessions.** That is about half of the HF release's 4,852, spread over 5.5 months.
  - **The pace is falling in repos that already use Entire, and rising in repos newly adopting it.** Claude Code is now under half of all new sessions; Codex, Pi and Cursor are growing.
  - Discovery is incomplete: code search caps out at about 200 results per query. The true public total is higher, by an unknown amount.
- **(e) Pinning.** A self-collected snapshot can be pinned exactly:
  - Record, for each repo, the checkpoint ref (or `v1` tip) and its commit SHA, plus the crawl date.
  - Checkpoint commits are content-addressed, so the SHA list fully defines the snapshot.
  - The data cannot be re-fetched later, though. Of the 205 HF repos, 18 are already gone and 47 have deleted their Entire storage; entireio/cli, the largest at 874 sessions, dropped `v1`. So the pinned snapshot must also be **archived** (a private, gated HF dataset or a bucket), not just listed.
  - ODC-By allows us to redistribute the HF release itself. Re-publishing self-collected data is a separate question: it depends on each repo's license and on PII scrubbing.

**Recommended route:**
1. **Email SALT now** (Joachim Baumann) and ask for a post-April export or their crawler.
2. **Prepare a self-collection fallback in parallel**, gated on the PI's ethics decision:
   - discovery from code search plus commit search;
   - `v1` branches and `refs/entire/checkpoints/*`;
   - Claude Code only;
   - only repos whose license permits redistribution (SALT's rule);
   - Presidio + TruffleHog re-redaction, as SALT does;
   - pin by commit SHA, and archive to a private, gated HF dataset.
3. **Keep the HF April release as the pinned baseline either way**, and mirror `f66cca95` now, because its upstream sources are disappearing.

Timeline risk:
- **SALT route: high.** SALT has been silent for five months, and there is no request process.
- **Self-collection: moderate.** It takes about 1–2 weeks of engineering. The ethics/IRB determination is the gating item, not the engineering.

## 1. Where the live data comes from, and the terms

### Collection mechanism (documented)

- **Dataset card.** "Data is collected from public GitHub repositories that use the Entire.io CLI to checkpoint their AI coding sessions. The Entire CLI creates checkpoints on a special branch (`entire/checkpoints/v1`)." (HF card, `f66cca95`, *Data Collection*.)
- **Paper, App. C.1.** "Our pipeline discovers Entire-enabled public repositories by querying the GitHub Code Search API and, for each repository, downloads all checkpoint directories from the metadata branch and parses the raw transcripts into structured tables." (arXiv 2604.20779v1.)
- **Paper, §2.1.** The data comes from "public GitHub repositories whose developers have opted into Entire.io's CLI checkpoint logging", and SALT "plan[s] to update our Website and Data frequently as we continue to collect new data."
- **Entire README, Security & Privacy.** "Your session transcripts are stored in your git repository … If your repository is public, this data is visible to anyone." (entireio/cli README @ main, 2026-10-01; `docs/security-and-privacy.md`.)

### Consent: what the paper actually claims (documented)

- The ethics statement reads: "All data in SWE-chat is collected from public GitHub repositories where developers have explicitly opted in to Entire CLI tracking and pushed session logs to public branches. We only include repositories whose licenses allow redistribution. … The study procedure was reviewed and deemed exempt by the Stanford Institutional Review Board (IRB)."
- **The "opt-in" is to Entire, not to SALT.** Participants never consented to SALT's research specifically. SALT harvests public data, just as we would. The ticket's premise ("participants consented to SALT's collection") is therefore not supported by the paper.
- The only participant-facing control is removal on request. The card says to email joachimbaumann@stanford.edu with `repo_id`, `session_id` or `turn_id`.
- **Implication (inferred).** Self-collection is the same act SALT performed. It is not covered by SALT's IRB exemption, though. We need our own determination: exempt research on public data, plus a removal channel and PII scrubbing equivalent to SALT's.
- **Third parties in the transcripts.** Transcripts capture file contents, MCP calls and tool output (Entire security doc). They can therefore contain personal data about people other than the repo owner.

### Terms that apply to self-collection (documented)

- **GitHub Acceptable Use Policies, §7 ("Information Usage Restrictions").**
  - "Researchers may use public, non-personal information from the Service for research purposes, only if any publications resulting from that research are open access."
  - "Archivists may use public information from the Service for archival purposes."
  - All use "must comply with the GitHub Privacy Statement."
  - API use falls under ToS §H instead.
  - Transcripts contain personal information, so the "non-personal" qualifier matters. This is a further argument for redacting on ingest and keeping raw data private.
- **Repo licenses.** Each repo's own license governs its checkpoint data. SALT keeps only repos "whose licenses allow redistribution". The HF `repositories.license_type` mix is 141 MIT, 22 Apache-2.0, 13 AGPL-3.0, 11 ISC, 7 GPL-3.0, 2 Elastic-2.0, and others (measured). We would need the same filter, and AGPL/GPL/Elastic deserve a closer look if we redistribute.
- **ODC-By** covers SALT's compiled database (the HF release). It permits copying and redistribution with attribution. It does not cover data we collect ourselves.
- **HF gating.** The HF dataset is `gated: auto` (click-through, auto-approved; measured via the HF API). No extra gating terms appear in the card.

## 2. Does SALT publish newer snapshots or take data requests?

All measured on 2026-10-01:

| Channel | State |
|---|---|
| HF `SALT-NLP/SWE-chat` | One revision, `f66cca95b14caaa4177f7ed5eaa424608dadcffa`, last modified 2026-04-29 ("Collapse history after secret redaction"). No other branches or tags |
| HF discussions | Five threads in total; none from SALT. #5 (2026-07-08) reports 4 transcripts with embedded NUL bytes and asks for a re-export. It is open, with no maintainer reply |
| GitHub `SALT-NLP/SWE-chat` | Last push 2026-04-24. README: "Stay tuned — data and code coming soon." Holds only an MIT LICENSE and the README. Issue #1 (dataset 404) was resolved by users, not SALT |
| SALT-NLP org | Active on other projects (pushes through 2026-09-24), but not on SWE-chat |
| swe-chat.com | Static Vercel page, last deployed 2026-09-30. Stats and "+N / last 7 days" deltas are literals in the HTML; no script loads data. Headline totals (6K sessions, 13K checkpoints, 63K prompts, 355K tool calls, 2.7M events) equal the April paper's numbers |
| Paper | v1 only (2026-04-22). Promises "frequent" updates and a "living dataset" |

- No data-request procedure is documented anywhere.
- The only stated contact is the removal address above.
- Inferred: a request is possible but has no defined path or timeline. The five-month silence on HF suggests a slow or no response.

## 3. Is newer data the same format?

### Storage location changed (documented)

- **`docs/architecture/ref-checkpoint-backend.md`** (entireio/cli; doc added 2026-07-09) describes two backends:
  - **`git-branch`**, the legacy backend: checkpoints are subtrees of `entire/checkpoints/v1`, under `<id[:2]>/<id[2:]>/`, with 12-hex IDs.
  - **`git-refs`**: one ref per checkpoint, `refs/entire/checkpoints/<last-2-chars>/<id>`, with 26-character ULID IDs whose timestamp prefix gives the creation time.
- "A first-time `entire enable` writes `git-refs` explicitly, with no prompt." Existing repos without a `checkpoints` block stay on `git-branch`.
- Readers try refs first and fall back to the branch. Old CLIs silently miss refs-backed checkpoints.
- **Measured.** Of 377 reachable non-HF Entire repos, 152 have per-checkpoint refs and 72 have `v1`. Among the 187 reachable HF repos, only entireio/cli switched to refs; it deleted its `v1` branch and has 59 refs.
- **Inferred.** SALT's documented crawler ("downloads all checkpoint directories from the metadata branch") misses refs-backed repos unless SALT has updated it. Every refs-backed repo appeared after the April release (ULID dates run July–October).

### Checkpoint contents (documented: `docs/architecture/sessions-and-checkpoints.md`)

- Each checkpoint holds a root `metadata.json` (`CheckpointSummary`), and per session `<n>/metadata.json`, `<n>/full.jsonl`, `<n>/transcript.jsonl`, `<n>/prompt.txt` and `<n>/content_hash.txt`, plus `tasks/<tool-use-id>/{agent-<id>.jsonl, task.json}`.
- `full.jsonl` is "Agent transcript, sanitized + redacted". For Claude Code this is the native JSONL the HF `transcripts/` files come from. Its schema follows the Claude Code version, not Entire's.
- New since the April release: the compact `transcript.jsonl` and materialized subagent transcripts under `tasks/`. In the HF release, subagent traffic appeared only nested in `progress` entries (see `swe-chat-schema.md`).
- The commit message of each checkpoint carries `Entire-Session`, `Entire-Strategy` and `Entire-Agent` trailers. I used these for the counts in §4.
- Not verified on post-April content (see the note at the top): whether the `full.jsonl` fields we rely on (`timestamp`, `permissionMode`, `is_error`, `toolUseResult.interrupted`, `queue-operation`) are still present. Inferred: likely yes, because Entire stores Claude Code's own log. The fields will shift with Claude Code versions, so a converter must be tolerant of that.

### Redaction (documented)

- **Raw checkpoints (Entire, `docs/security-and-privacy.md`).**
  - Six secret-detection passes run before anything is written to git: entropy, Betterleaks patterns, provider prefixes, credentialed URIs, DB connection strings, and credential values. Five are always on.
  - Custom rules, **opt-in PII redaction** and an opt-in OpenAI Privacy Filter pass are available.
  - Pasted images in Claude Code transcripts are stored **unredacted** as base64.
- **HF release (SALT, card and paper ethics statement).**
  - Presidio NER (spaCy transformer) over every user and assistant turn, for names, emails and phones.
  - TruffleHog for credentials.
  - Images dropped.
- **Consequence.** Raw checkpoints are *not* PII-redacted by default. A self-collected snapshot must re-run an equivalent pipeline on ingest (Presidio + TruffleHog, drop images) before anyone reads it. The card's PII redaction covers "user prompts and assistant text responses", so tool outputs in the HF release may also carry PII (inferred from the card's wording).

## 4. How much Claude Code data exists after 2026-04-19

Method (measured):
1. Discovered Entire repos from two sources:
   - the 205 HF repos;
   - 382 more from GitHub code search (`path:.entire filename:settings.json`, with variants) and commit search (`"Entire-Checkpoint"`, September 2026).
2. Ran `git ls-remote` on `refs/entire/*` and `refs/heads/entire/*` for every repo.
3. For repos with a `v1` branch, paged through `v1` commits since 2026-04-19T06:01Z, the last HF Claude Code session.
4. Counted distinct `Entire-Session` IDs that are not in HF `sessions`, by `Entire-Agent`.
5. For refs-backed repos, dated each checkpoint from its ULID.

### Repo status

| | HF repos (205) | Non-HF discovered (382) |
|---|---|---|
| Gone (404 or private) | 18 | 5 |
| No Entire storage left | 47 | 162 |
| `v1` branch | 139 | 72 (9 also have refs) |
| Per-checkpoint refs | 1 (entireio/cli, `v1` removed) | 152 |
| Active after the cutoff | 41 (12 since 2026-09-01) | — |

### New sessions on `v1` branches since 2026-04-19

| | HF repos | Non-HF repos | Total |
|---|---|---|---|
| All agents | 1,029 | 2,334 | 3,363 |
| Claude Code | 770 (35 repos, 33 committers) | 784 (35 repos, 42 committers) | **1,554** |
| Codex | 218 | 829 | 1,047 |
| Others | Pi 17, Copilot 14, Cursor 10 | Pi 295, Cursor 229, OpenCode 129, Droid 46 | |
| Claude Code, last 7 days | 12 | 29 | 41 |

Claude Code sessions by month (HF repos / non-HF repos):

| Month | HF repos | Non-HF repos |
|---|---|---|
| Apr | 185 | 48 |
| May | 200 | 74 |
| Jun | 163 | 168 |
| Jul | 112 | 268 |
| Aug | 70 | 142 |
| Sep | 38 | 84 |

The committer count uses the GitHub login or email of the checkpoint commit author. It is a proxy for users and may merge or split people.

### Per-checkpoint refs (newer repos)

- 5,327 ULID checkpoints in non-HF repos: July 35, August 2,277, September 2,962, Oct 1 53. **895 of them fall in the last 7 days.**
- Separately, 22 hex-named refs in HF repos and many in a few non-HF repos (e.g. `orin-dx/callisto` has 8,253 refs) are migrated legacy checkpoints.
- I could not get the agent mix without reading checkpoint contents. Estimate (inferred):
  - HF has 0.44 distinct sessions per checkpoint (5,851 / 13,406).
  - Claude Code is 46% of post-cutoff `v1` sessions.
  - 5,327 × 0.44 × 0.46 gives **about 1,100 Claude Code sessions**, with a plausible range of 700–1,500.

### Scale of the public universe (measured, rough)

- GitHub commit search for `"Entire-Checkpoint"` (the trailer Entire adds to user commits) counts:
  - **38,308 commits before the cutoff**, against the HF release's 14,459;
  - **51,000 after the cutoff**: 16,244 from Apr 20 to May 31, 8,710 in Jun, 8,162 in Jul, 10,671 in Aug, 7,211 in Sep, and 1,893 in the last 7 days.
- A trailer means only that Entire was active. Its checkpoints may have gone to a private `checkpoint_remote` or not been pushed at all.
- Inferred: our discovered set (about 2,000–3,000 Claude Code sessions) is a lower bound. A complete crawl might reach about 1.5–2× that. Discovery must use commit search sliced by date as well as code search, because both APIs cap at about 1,000 results per query (code search at about 200 in practice).

**The "+340 sessions in the last 7 days" on swe-chat.com cannot be checked from the page.** It is a literal in the HTML. Our measured Claude Code rate on `v1` is about 41 sessions a week, plus perhaps 75 a week on refs; the all-agent rate on refs is roughly 2–3 times that.

## 5. Pinning a snapshot reproducibly

1. **Mirror the HF baseline now.** Copy revision `f66cca95` to a private (or gated) HF dataset under our org, or to a bucket. ODC-By allows this with attribution. Record the revision SHA in the spec.
2. **Manifest for self-collected data.** For each repo record:
   - `repo_id`;
   - the discovery query and date;
   - the backend;
   - for `v1`, the branch tip SHA; for refs, each `refs/entire/checkpoints/...` name and its commit SHA;
   - the license.

   Git commits are content-addressed, so the manifest defines the snapshot exactly. Store it in the repo.
3. **Archive the raw objects too.** Upstream data disappears: in five months 65 of 205 HF repos became unusable (18 gone, 47 storage removed). Developers can also rewrite or delete refs at will, and Entire's docs encourage cleaning up. Store the fetched checkpoints, redacted on ingest, in a private, gated HF dataset or a bucket, keyed by the manifest.
4. **Dated export.** Freeze the snapshot at a cutoff, for example sessions created on or before 2026-09-30 from a crawl on 2026-10-0x. Tag the revision of our HF mirror.
5. **Redistribution.** Publish only derived measures, or redacted data from redistributable-license repos with a removal channel (mirroring SALT's practice). Keep raw data private.

## 6. Open questions for the PI

1. **Contact SALT?** Recommended: yes, now. Ask for:
   - a post-April export, or read access to their crawl;
   - whether their crawler handles `refs/entire/checkpoints/*`;
   - their license allowlist and redaction code;
   - whether they object to us collecting in parallel.
2. **Ethics determination for self-collection.** Will our institution's IRB, or an exempt determination, cover harvesting public Entire checkpoints? The data includes third-party PII in tool outputs, and GitHub's AUP limits research use to "non-personal" information with open-access publication.
3. **Is about 2,000–3,000 new Claude Code sessions, from about 75+ committers, enough for "recent"?** Or should the study population be April HF plus the recent crawl, analyzed as two cohorts? The April data is now 5–8 months old, and agent mix and Claude Code versions have shifted.
4. **Did we inspect post-April content?** No, by design. The first step of any self-collection should be a small, redacted-on-ingest format check of `full.jsonl` fields against spec §3, run once (2) is settled.

## Sources

- HF dataset card and API: `SALT-NLP/SWE-chat`, revision `f66cca95b14caaa4177f7ed5eaa424608dadcffa`; discussions #1–#5.
- Baumann et al., *SWE-chat*, arXiv 2604.20779v1 (2026-04-22): §2.1, Ethics statement, App. A, App. C.1.
- swe-chat.com, HTML as served 2026-10-01 (`last-modified: 2026-09-30`).
- GitHub `SALT-NLP/SWE-chat` @ `8608198`; issue #1.
- `entireio/cli` @ main (2026-10-01): `README.md`, `docs/architecture/ref-checkpoint-backend.md`, `docs/architecture/sessions-and-checkpoints.md`, `docs/security-and-privacy.md`.
- GitHub Acceptable Use Policies §7, from `github/docs` `content/site-policy/acceptable-use-policies/github-acceptable-use-policies.md`.
- Measurements: `git ls-remote` on 587 repos; GitHub REST commit listings on 211 `v1` branches; GitHub code and commit search counts. Run 2026-10-01; scripts were kept in the session scratchpad and not committed.
- Prior findings: `docs/research/swe-chat-schema.md` (branch `research/swe-chat-schema`).
