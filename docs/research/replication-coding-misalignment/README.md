# Replication spike: Transluce's coding-agent misalignment study

Throwaway research from Oct 2, 2026. It reproduces the published overselling numbers in Transluce's "Measuring coding agent misalignment in the wild" from the public Docent collection, and reads the `docent` 0.1.87 SDK source for how readings run. It feeds [Export Transluce's published overselling results](https://github.com/rbodkin/comprehension-analysis/issues/30), which turns it into a reproducible script and note. The findings are summarized in the [status update](https://github.com/rbodkin/comprehension-analysis/issues/6#issuecomment-5960651026) on "Email Transluce: OSS roadmap and public-collection terms".

- `spike-note.md`: the public-data findings: denominator, per-model assignment, CIs, pending and over-1M results, verifier sample, prevalence. Its "Question for Selena" drafts are superseded; the Oct 2 follow-up asked only about the missing human prompts. SWE-chat user IDs are replaced with "user A" to "user D".
- `docent-sdk-note.md`: SDK findings on cloning collections, context overflow, request params, OpenRouter, concurrency and BYO keys, with `path:line` references into the 0.1.87 wheel.
- `scripts/`: the spike's helpers, kept as they were run (not cleaned up).
  - `dql.py`: anonymous DQL helper.
  - `assign.py`: model-assignment rules.
  - `ci.py`: CI methods, including the user-clustered bootstrap.
  - `bars.py`, `caps.py`: pixel measurements of the blog's error bars.

**Data is not committed.** It contains SWE-chat text, and Transluce's terms for redistributing their labels are unanswered. The scripts expect JSON dumps (`results.json`, `runs.json`, `table.json` and others listed in `spike-note.md`) in the working directory. Re-fetch them anonymously with the REST and DQL calls in Appendix C of the [Transluce overselling findings](https://github.com/rbodkin/comprehension-analysis/blob/research/transluce-overselling/docs/research/transluce-overselling.md).
