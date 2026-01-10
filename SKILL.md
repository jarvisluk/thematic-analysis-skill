---
name: thematic-analysis
description: Thematic analysis of qualitative text (interview transcripts, open-ended responses) with codebook creation, theme tables, participant labeling, and quote selection. Use when asked to analyze transcripts, extract themes, build a codebook, or produce tables with original sentences/quotes and participant identifiers.
---

# Thematic Analysis

## Workflow

1. Confirm inputs and participant labeling.
   - Treat each transcript file as one participant unless explicit labels are provided.
   - If no participant list is provided, label participants as P1, P2, P3... in the order transcripts are supplied.
   - If a single transcript is provided, label it P1.
   - If the provided participant list is missing entries or unclear, ask the user to provide a corrected list or approve creating one.

2. Process transcripts one at a time.
   - Analyze a single transcript per run.
   - Write results into a new subfolder under `outputs/` named after the transcript (or participant ID if no filename is available).

3. Light preprocessing.
   - Preserve original wording, even if grammar is imperfect.
   - If a quote is too long or contains irrelevant filler, replace only the removed span with "...".

4. Initial coding.
   - Code meaningful units (phrases, sentences, or short turns) that convey a distinct idea.
   - Keep code names short and descriptive.
   - Track participant for each coded quote.

5. Develop themes.
   - Group related codes into themes with clear definitions.
   - Ensure each theme has at least one supporting quote.

6. Produce outputs for the transcript.
   - Provide a participant list, codebook table, and themes table.
   - Include original sentences/quotes and participant identifiers in tables.
   - Output tables in Markdown by default; use CSV if the user requests it.
   - Save outputs into the transcript subfolder under `outputs/`.

7. Final synthesis across transcripts.
   - After all transcripts are processed, examine all per-transcript outputs and produce a final codebook and themes table that synthesize across participants.
   - Save the final synthesis into `outputs/final/`.

## Output formats

- Participant list: bullet list of participant IDs.
- Codebook table columns: Code | Definition | Inclusion | Exclusion | Example quote | Participant
- Themes table columns: Theme | Description | Supporting quotes | Participants
- Output table format: Markdown or CSV based on user request.
- Quote handling: keep original wording; replace removed spans with "..." only.

## Output hierarchy

```
outputs/
  <transcript-or-participant-id>/
    participants.(md|csv)
    codebook.(md|csv)
    themes.(md|csv)
  final/
    codebook.(md|csv)
    themes.(md|csv)
```

## References

- For detailed steps and quality checks, read `references/thematic-workflow.md`.
- For table templates and quote handling examples, read `references/output-templates.md`.
