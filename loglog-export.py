#!/usr/bin/env python3
"""
loglog_export.py - Export loglog.csv to a .txt file

Usage:
  python loglog_export.py chrono     # chronological list
  python loglog_export.py type       # grouped by media type
"""

import csv
import sys
import os
from datetime import datetime

CSV_FILE = "loglog.csv"
OUTPUT_DIR = "./"

def load_entries():
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def format_entry(row):
    rating = f" ({row['rating']}★)" if row["rating"] else ""
    author = f" by {row['author']}" if row["author"] else ""
    line = f"[{row['date']}] {row['type'].upper()}: {row['title']}{author}{rating}"
    if row["notes"]:
        line += f"\n    → {row['notes']}"
    return line

def export_chrono(rows):
    lines = ["LOGLOG - Chronological Overview", "=" * 40, ""]
    for row in rows:
        lines.append(format_entry(row))
    return "\n".join(lines)

def export_by_type(rows):
    lines = ["LOGLOG - Overview by Media Type", "=" * 40, ""]
    
    types = {}
    for row in rows:
        t = row["type"]
        if t not in types:
            types[t] = []
        types[t].append(row)
    
    for media_type, entries in sorted(types.items()):
        lines.append(f"\n### {media_type.upper()} ({len(entries)}) ###\n")
        for row in entries:
            lines.append(format_entry(row))
    
    return "\n".join(lines)

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("chrono", "type"):
        print("Usage:")
        print("  python loglog_export.py chrono   # chronological list")
        print("  python loglog_export.py type     # by media type")
        sys.exit(1)
    
    mode = sys.argv[1]
    rows = load_entries()
    
    if not rows:
        print("No entries to export.")
        sys.exit(1)
    
    if mode == "chrono":
        content = export_chrono(rows)
        filename = "loglog_chrono.txt"
    else:
        content = export_by_type(rows)
        filename = "loglog_type.txt"
    
    output_path = os.path.join(OUTPUT_DIR, filename)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✓ Exported: {output_path} ({len(rows)} entries)")

if __name__ == "__main__":
    main()
