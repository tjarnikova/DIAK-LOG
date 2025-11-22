#!/usr/bin/env python3
"""
loglog.py - Command-line media diary
"""

import csv
import os
from datetime import datetime

CSV_FILE = "loglog.csv"
FIELDS = ["date", "type", "title", "author", "rating", "notes"]

MEDIA_TYPES = [
    "book",
    "article",
    "podcast",
    "video",
    "music",
    "film",
    "series",
    "exhibition",
    "lecture",
    "theatre",
    "other"
]

def ensure_csv_exists():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()

def prompt(text, required=True, default=None):
    suffix = f" [{default}]" if default else ""
    while True:
        val = input(f"{text}{suffix}: ").strip()
        if not val and default:
            return default
        if val or not required:
            return val
        print("  This field is required.")

def select_type():
    print("\nMedia type:")
    for i, t in enumerate(MEDIA_TYPES, 1):
        print(f"  {i}. {t}")
    while True:
        choice = input("Choose (number or name): ").strip().lower()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(MEDIA_TYPES):
                return MEDIA_TYPES[idx]
        elif choice in MEDIA_TYPES:
            return choice
        print("  Invalid choice, try again.")

def get_rating():
    while True:
        val = input("Rating (1-5, or skip): ").strip()
        if not val or val.lower() == "skip":
            return ""
        if val in "12345":
            return val
        print("  Enter 1-5 or leave blank.")

def add_entry():
    print("\n--- New Entry ---")
    entry = {
        "date": prompt("Date", default=datetime.now().strftime("%Y-%m-%d")),
        "type": select_type(),
        "title": prompt("Title"),
        "author": prompt("Author/Creator", required=False),
        "rating": get_rating(),
        "notes": prompt("Notes", required=False)
    }
    
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writerow(entry)
    
    print(f"\n✓ Saved: {entry['title']}")

def load_entries():
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def display_entries(rows):
    if not rows:
        print("No entries found.")
        return
    for row in rows:
        rating = f" ({row['rating']}★)" if row["rating"] else ""
        author = f" by {row['author']}" if row["author"] else ""
        print(f"[{row['date']}] {row['type'].upper()}: {row['title']}{author}{rating}")
        if row["notes"]:
            print(f"    → {row['notes']}")

def browse_entries():
    rows = load_entries()
    if not rows:
        print("No entries yet.")
        return
    
    print("\nBrowse by:")
    print("  1. chronological (all entries)")
    print("  2. filter by media type")
    print("  3. search")
    choice = input("Choose (1, 2, or 3): ").strip()
    
    if choice == "2":
        print("\nMedia types:")
        for i, t in enumerate(MEDIA_TYPES, 1):
            print(f"  {i}. {t}")
        type_choice = input("Choose (number or name): ").strip().lower()
        
        if type_choice.isdigit():
            idx = int(type_choice) - 1
            if 0 <= idx < len(MEDIA_TYPES):
                type_choice = MEDIA_TYPES[idx]
        
        filtered = [r for r in rows if r["type"].lower() == type_choice]
        print(f"\n--- {type_choice.upper()} ({len(filtered)} entries) ---")
        display_entries(filtered)
    elif choice == "3":
        query = input("Search: ").strip().lower()
        if query:
            matches = [r for r in rows if query in r["title"].lower() or query in r["author"].lower()]
            print(f"\n--- Search: '{query}' ({len(matches)} results) ---")
            display_entries(matches)
    else:
        print(f"\n--- All Entries ({len(rows)}) ---")
        display_entries(rows)

def main_menu():
    ensure_csv_exists()
    print("\n╔══════════════════════════╗")
    print("║          LOGLOG          ║")
    print("╚══════════════════════════╝")
    
    while True:
        print("\n a small universal reading-listening-watching diary")
        print("\n[r]ecord  [b]rowse  [q]uit")
        choice = input("> ").strip().lower()
        
        if choice in ("r", "record"):
            add_entry()
        elif choice in ("b", "browse"):
            browse_entries()
        elif choice in ("q", "quit", "exit"):
            print("Cheers!")
            break
        else:
            print("Confusing (Unknown command.)")

if __name__ == "__main__":
    main_menu()
