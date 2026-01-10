#!/usr/bin/env python3
import argparse
import os
import re
from typing import Dict, List, Tuple


def read_text(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        with open(path, "r", encoding="latin-1") as f:
            return f.read()


def split_markdown_row(line: str, header_len: int) -> List[str]:
    parts = [p.strip() for p in line.strip().strip("|").split("|")]
    if len(parts) > header_len:
        parts = parts[: header_len - 1] + ["|".join(parts[header_len - 1 :]).strip()]
    while len(parts) < header_len:
        parts.append("")
    return parts


def parse_markdown_tables(text: str) -> List[Dict[str, List[Dict[str, str]]]]:
    lines = text.splitlines()
    tables = []
    i = 0
    while i < len(lines) - 1:
        line = lines[i].strip()
        next_line = lines[i + 1].strip()
        if "|" in line and re.match(r"^\s*\|?\s*-", next_line):
            header = [h.strip() for h in line.strip("|").split("|")]
            rows = []
            i += 2
            while i < len(lines):
                row_line = lines[i].strip()
                if not row_line or "|" not in row_line:
                    break
                cells = split_markdown_row(row_line, len(header))
                row = {header[idx]: cells[idx] for idx in range(len(header))}
                rows.append(row)
                i += 1
            tables.append({"header": header, "rows": rows})
        else:
            i += 1
    return tables


def find_table(tables, required_headers: List[str]) -> Dict[str, List[Dict[str, str]]]:
    for table in tables:
        header = [h.strip().lower() for h in table["header"]]
        if all(req.lower() in header for req in required_headers):
            return table
    return {"header": [], "rows": []}


def normalize_quote(text: str) -> str:
    text = text.strip().strip('"').strip()
    text = re.sub(r"\s*\(P[0-9]+.*\)\s*$", "", text).strip()
    return text


def quote_in_transcript(quote: str, transcript: str) -> bool:
    if not quote:
        return False
    if "..." in quote:
        segments = [seg for seg in (s.strip() for s in quote.split("...")) if seg]
        pos = 0
        for seg in segments:
            idx = transcript.find(seg, pos)
            if idx == -1:
                return False
            pos = idx + len(seg)
        return True
    return quote in transcript


def extract_quotes_from_themes(supporting_quotes: str) -> List[str]:
    quotes = re.findall(r'"([^"]+)"', supporting_quotes)
    if quotes:
        return [normalize_quote(q) for q in quotes if normalize_quote(q)]
    fallback = normalize_quote(supporting_quotes)
    return [fallback] if fallback else []


def load_participants(participants_path: str) -> List[Dict[str, str]]:
    text = read_text(participants_path)
    tables = parse_markdown_tables(text)
    table = find_table(tables, ["Participant", "Transcript file", "Output folder"])
    return table["rows"]


def analyze_final(output_root: str, transcripts_text: str) -> Tuple[str, List[Dict[str, str]]]:
    output_path = os.path.join(output_root, "final")
    checks = []

    codes_path = os.path.join(output_path, "codes.md")
    if not os.path.exists(codes_path):
        codes_path = os.path.join(output_path, "codebook.md")

    if os.path.exists(codes_path):
        tables = parse_markdown_tables(read_text(codes_path))
        code_table = find_table(tables, ["Code", "Example quote"])
        for row in code_table["rows"]:
            code = row.get("Code", "").strip()
            quote = normalize_quote(row.get("Example quote", ""))
            found = quote_in_transcript(quote, transcripts_text)
            checks.append(
                {
                    "Source": "Final Codes",
                    "Code/Theme": code or "Final",
                    "Quote": quote,
                    "Found": "Yes" if found else "No",
                }
            )

    themes_path = os.path.join(output_path, "themes.md")
    if os.path.exists(themes_path):
        tables = parse_markdown_tables(read_text(themes_path))
        theme_table = find_table(tables, ["Theme", "Supporting quotes"])
        for row in theme_table["rows"]:
            theme = row.get("Theme", "").strip()
            supporting_quotes = row.get("Supporting quotes", "")
            for quote in extract_quotes_from_themes(supporting_quotes):
                found = quote_in_transcript(quote, transcripts_text)
                checks.append(
                    {
                        "Source": "Final Themes",
                        "Code/Theme": theme or "Final",
                        "Quote": quote,
                        "Found": "Yes" if found else "No",
                    }
                )

    return output_path, checks


def write_check_table(output_path: str, checks: List[Dict[str, str]]) -> str:
    os.makedirs(output_path, exist_ok=True)
    out_path = os.path.join(output_path, "quote-check.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("| Source | Code/Theme | Quote | Found |\n")
        f.write("| --- | --- | --- | --- |\n")
        for row in checks:
            f.write(
                f"| {row['Source']} | {row['Code/Theme']} | {row['Quote']} | {row['Found']} |\n"
            )
    return out_path


def summarize_checks(label: str, checks: List[Dict[str, str]]) -> str:
    total = len(checks)
    missing = [row for row in checks if row["Found"] == "No"]
    missing_count = len(missing)
    summary = f"{label}: {total} quotes checked, {missing_count} missing."
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate quotes against transcripts.")
    parser.add_argument("--outputs", default="outputs", help="Path to outputs directory.")
    parser.add_argument(
        "--transcripts-root",
        default=".",
        help="Root directory for transcript file paths.",
    )
    args = parser.parse_args()

    output_root = args.outputs
    participants_path = os.path.join(output_root, "participants.md")
    if not os.path.exists(participants_path):
        raise FileNotFoundError(f"Missing participants list: {participants_path}")

    participant_rows = load_participants(participants_path)
    if not participant_rows:
        raise ValueError("No participants found in participants.md.")

    transcripts_text = []
    for row in participant_rows:
        transcript_file = row.get("Transcript file", "").strip()
        if not transcript_file:
            continue
        transcript_path = (
            transcript_file
            if os.path.isabs(transcript_file)
            else os.path.join(args.transcripts_root, transcript_file)
        )
        transcripts_text.append(read_text(transcript_path))

    final_output_path, final_checks = analyze_final(
        output_root, "\n".join(transcripts_text)
    )
    if final_checks:
        write_check_table(final_output_path, final_checks)
        print(summarize_checks("final", final_checks))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
