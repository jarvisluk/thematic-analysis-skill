# Output Templates

## Participant list

- P1
- P2
- P3

Example mapping when each TXT file is one participant:

- P1 = transcript_01.txt
- P2 = transcript_02.txt
- P3 = transcript_03.txt

## Codebook table

Columns: Code | Definition | Inclusion | Exclusion | Example quote | Participant

Markdown example:

| Code | Definition | Inclusion | Exclusion | Example quote | Participant |
| --- | --- | --- | --- | --- | --- |
| Schedule pressure | Mentions of tight timelines or deadline stress | Deadlines, lack of time | General workload with no time reference | "We had to finish in two days, so everything felt rushed..." | P2 |

CSV example:

```csv
Code,Definition,Inclusion,Exclusion,Example quote,Participant
Schedule pressure,Mentions of tight timelines or deadline stress,Deadlines or lack of time,General workload with no time reference,"We had to finish in two days, so everything felt rushed...",P2
```

## Themes table

Columns: Theme | Description | Supporting quotes | Participants

Markdown example:

| Theme | Description | Supporting quotes | Participants |
| --- | --- | --- | --- |
| Time constraints | Participants describe limited time as shaping decisions and stress | "We had to finish in two days..." (P2); "No time to test properly..." (P3) | P2, P3 |

CSV example:

```csv
Theme,Description,Supporting quotes,Participants
Time constraints,"Participants describe limited time as shaping decisions and stress","We had to finish in two days... (P2); No time to test properly... (P3)","P2, P3"
```

## Quote handling

- Keep original wording even if ungrammatical.
- If a quote is too long, replace removed spans with "...".
- Do not change wording beyond the ellipsis replacement.
