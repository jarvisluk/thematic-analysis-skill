#!/usr/bin/env python3
import argparse
import os
import re
from typing import Dict, List, Optional

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

def load_participants(participants_path: str) -> List[Dict[str, str]]:
    if not os.path.exists(participants_path):
        print(f"Warning: Participants file not found at {participants_path}")
        return []
    text = read_text(participants_path)
    tables = parse_markdown_tables(text)
    table = find_table(tables, ["Participant", "Transcript file"])
    return table["rows"]

def merge_codes(output_root: str):
    participants_path = os.path.join(output_root, "participants.md")
    participant_rows = load_participants(participants_path)
    
    all_codes = []
    headers = ["Code", "Definition", "Example quote", "Participant"]
    
    print(f"Found {len(participant_rows)} participants.")
    
    for row in participant_rows:
        participant_id = row.get("Participant", "").strip()
        output_folder = row.get("Output folder", row.get("Output file", participant_id)).strip()
        
        # Determine the path. output_folder might be just "P1" or "P1.md"
        if not output_folder.endswith(".md"):
            output_file = f"{output_folder}.md"
        else:
            output_file = output_folder
            
        output_path = os.path.join(output_root, output_file)
        
        if not os.path.exists(output_path):
            print(f"Warning: Output file not found for {participant_id} at {output_path}")
            continue
            
        text = read_text(output_path)
        tables = parse_markdown_tables(text)
        # Look for code table. Columns might vary slightly but usually contain Code and Definition
        code_table = find_table(tables, ["Code", "Definition"])
        
        if not code_table["rows"]:
            print(f"Warning: No code table found in {output_path}")
            continue
            
        # Map rows to standard structure
        for r in code_table["rows"]:
            # Try to get values regardless of case or slight variations if we extended find_table logic
            # For now assume headers match what find_table found, which matched "Code" and "Definition"
            
            # We want to keep track of Code, Definition, Example quote, Participant
            # If "Participant" column exists in source, use it, else use participant_id
            
            p_val = r.get("Participant", participant_id)
            if not p_val:
                p_val = participant_id
                
            merged_row = {
                "Code": r.get("Code", ""),
                "Definition": r.get("Definition", ""),
                "Example quote": r.get("Example quote", r.get("Quote", "")),
                "Participant": p_val
            }
            all_codes.append(merged_row)

    if not all_codes:
        print("No codes found to merge.")
        return

    # Write to outputs/final/codes.md
    final_dir = os.path.join(output_root, "final")
    os.makedirs(final_dir, exist_ok=True)
    final_path = os.path.join(final_dir, "codes.md")
    
    with open(final_path, "w", encoding="utf-8") as f:
        f.write("# Final Code Table\n\n")
        header_line = "| " + " | ".join(headers) + " |"
        sep_line = "| " + " | ".join(["---"] * len(headers)) + " |"
        f.write(header_line + "\n")
        f.write(sep_line + "\n")
        
        for row in all_codes:
            line = "| " + " | ".join([row.get(h, "") for h in headers]) + " |"
            f.write(line + "\n")
            
    print(f"Merged {len(all_codes)} codes to {final_path}")

def main() -> int:
    parser = argparse.ArgumentParser(description="Merge code tables from participant outputs.")
    parser.add_argument("--outputs", default="outputs", help="Path to outputs directory.")
    args = parser.parse_args()
    
    merge_codes(args.outputs)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
