---
name: thematic-analysis
description: Thematic analysis of qualitative text (interview transcripts, open-ended responses) with participant labeling, codes, theme tables, and quote selection. Use when asked to analyze transcripts, extract codes and themes, build theme tables, or produce tables with original sentences/quotes and participant identifiers.
---

# Thematic Analysis

## Workflow

1. Confirm inputs and participant labeling.
   - Treat each transcript file as one participant unless explicit labels are provided.
   - If no participant list is provided, label participants as P1, P2, P3... in the order transcripts are supplied.
   - If a single transcript is provided, label it P1.
   - If the provided participant list is missing entries or unclear, ask the user to provide a corrected list or approve creating one.
   - Output the participants list immediately after labeling (save to `outputs/participants.md`).

2. Process transcripts one at a time.
   - Analyze a single transcript per run.
   - Output results after each transcript is analyzed.
   - Use participant IDs (P01, P02, ...) rather than filenames in outputs.
   - Save per-transcript outputs directly under `outputs/` using the participant ID as the filename (e.g., `outputs/P1.md`).

3. Light preprocessing.
   - Preserve original wording, even if grammar is imperfect.
   - If a quote is too long or contains irrelevant filler, replace only the removed span with "...".
   - Provide all analysis and outputs in English; if transcripts are not in English, do not translate quotes and keep original wording for quoted text.

4. Initial coding.
   - Code meaningful units (phrases, sentences, or short turns) that convey a distinct idea.
   - Keep code names short and descriptive.
   - Track participant for each coded quote.

5. Develop themes after all transcripts are analyzed.
   - Group related codes into themes with clear definitions.
   - Ensure each theme has at least one supporting quote.

6. Produce outputs for each transcript.
   - Provide a participant list entry and a code table (meaning units with codes and quotes).
   - Include original sentences/quotes and participant identifiers in tables.
   - Output tables in Markdown only.
   - Save outputs as `outputs/<participant-id>.md` (e.g., `outputs/P1.md`), no subfolders.
   - Maintain `outputs/participants.md` as the canonical mapping of participant IDs, transcript filenames, and output filenames.

7. Merge and validate after all transcripts are coded.
   - Merge all per-transcript code tables into `outputs/final/codes.md`.
   - Develop the final themes table (`outputs/final/themes.md`) as a summary of codes.
   - Run `scripts/validate_quotes.py --outputs outputs --transcripts-root <root>` to check quotes in the merged codes and themes.
   - Review `outputs/final/quote-check.md` for validation results.

8. Final synthesis across transcripts.
   - After validation, produce a findings report in Markdown that summarizes themes across participants.
   - Write one section per theme with a brief narrative and representative quotes (keep participant IDs as P01, P02, ...).
   - Save final outputs into `outputs/final/` (`findings.md`, `codes.md`, `themes.md`, `quote-check.md`).

## Output formats

- Participant list: mapping table of participant IDs, transcript filenames, and output folders.
- Code table columns (per transcript and merged): Code | Definition | Example quote | Participant
- Themes table columns: Theme | Description | Supporting quotes | Participants
- Output table format: Markdown only.
- Quote handling: keep original wording; replace removed spans with "..." only.
- Participants list mapping: Participant | Transcript file | Output folder

## Output hierarchy

```
outputs/
  participants.md
  <participant-id>.md  # e.g., P01.md
  final/
    codes.md
    themes.md
    quote-check.md
    findings.md
```

## References

- For detailed steps and quality checks, read `references/thematic-workflow.md`.
- For table templates and quote handling examples, read `references/output-templates.md`.
