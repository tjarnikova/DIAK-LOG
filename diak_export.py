#!/usr/bin/env python3
"""
diak_export.py - Export diak.csv to a .txt file

Usage:
  python diak_export.py chrono       # chronological list
  python diak_export.py typ          # grouped by media type
"""

import csv
import sys
import os
from datetime import datetime

CSV_FILE = "diak.csv"
OUTPUT_DIR = "./"

def load_entries():
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def format_entry(row):
    rating = f" ({row['hodnocení']}★)" if row["hodnocení"] else ""
    author = f" od {row['autor']}" if row["autor"] else ""
    line = f"[{row['datum']}] {row['typ'].upper()}: {row['název']}{author}{rating}"
    if row["poznámky"]:
        line += f"\n    → {row['poznámky']}"
    return line

def export_chrono(rows):
    lines = ["DIÁK - Chronologický přehled", "=" * 40, ""]
    for row in rows:
        lines.append(format_entry(row))
    return "\n".join(lines)

def export_by_type(rows):
    lines = ["DIÁK - Přehled podle typu média", "=" * 40, ""]
    
    types = {}
    for row in rows:
        t = row["typ"]
        if t not in types:
            types[t] = []
        types[t].append(row)
    
    for media_type, entries in sorted(types.items()):
        lines.append(f"\n### {media_type.upper()} ({len(entries)}) ###\n")
        for row in entries:
            lines.append(format_entry(row))
    
    return "\n".join(lines)

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("chrono", "typ"):
        print("Použití:")
        print("  python diak_export.py chrono   # chronologický seznam")
        print("  python diak_export.py typ      # podle typu média")
        sys.exit(1)
    
    mode = sys.argv[1]
    rows = load_entries()
    
    if not rows:
        print("Žádné záznamy k exportu.")
        sys.exit(1)
    
    if mode == "chrono":
        content = export_chrono(rows)
        filename = "diak_chrono.txt"
    else:
        content = export_by_type(rows)
        filename = "diak_typ.txt"
    
    output_path = os.path.join(OUTPUT_DIR, filename)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✓ Exportováno: {output_path} ({len(rows)} záznamů)")

if __name__ == "__main__":
    main()
