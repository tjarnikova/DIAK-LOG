#!/usr/bin/env python3
"""
diak.py - Příkazový řádek pro deník médií
"""

import csv
import os
from datetime import datetime

CSV_FILE = "diak.csv"
FIELDS = ["datum", "typ", "název", "autor", "hodnocení", "poznámky"]

MEDIA_TYPES = [
    "kniha",
    "článek",
    "podcast",
    "video",
    "hudba",
    "film",
    "seriál",
    "výstava",
    "přednáška",
    "divadlo",
    "jiné"
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
        print("  Toto pole je povinné.")

def select_type():
    print("\nTyp média:")
    for i, t in enumerate(MEDIA_TYPES, 1):
        print(f"  {i}. {t}")
    while True:
        choice = input("Vyber (číslo nebo název): ").strip().lower()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(MEDIA_TYPES):
                return MEDIA_TYPES[idx]
        elif choice in MEDIA_TYPES:
            return choice
        print("  Neplatná volba, zkus znovu.")

def get_rating():
    while True:
        val = input("Hodnocení (1-5, nebo přeskoč): ").strip()
        if not val or val.lower() in ("přeskoč", "preskoc", "skip"):
            return ""
        if val in "12345":
            return val
        print("  Zadej 1-5 nebo nech prázdné.")

def add_entry():
    print("\n--- Nový záznam ---")
    entry = {
        "datum": prompt("Datum", default=datetime.now().strftime("%Y-%m-%d")),
        "typ": select_type(),
        "název": prompt("Název"),
        "autor": prompt("Autor/Tvůrce", required=False),
        "hodnocení": get_rating(),
        "poznámky": prompt("Poznámky", required=False)
    }
    
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writerow(entry)
    
    print(f"\n✓ Uloženo: {entry['název']}")

def load_entries():
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def display_entries(rows):
    if not rows:
        print("Žádné záznamy nenalezeny.")
        return
    for row in rows:
        rating = f" ({row['hodnocení']}★)" if row["hodnocení"] else ""
        author = f" od {row['autor']}" if row["autor"] else ""
        print(f"[{row['datum']}] {row['typ'].upper()}: {row['název']}{author}{rating}")
        if row["poznámky"]:
            print(f"    → {row['poznámky']}")

def browse_entries():
    rows = load_entries()
    if not rows:
        print("Zatím žádné záznamy.")
        return
    
    print("\nProcházet podle:")
    print("  1. chronologicky (všechny záznamy)")
    print("  2. filtrovat podle typu média")
    print("  3. hledat v názvu")
    choice = input("Vyber (1, 2, nebo 3): ").strip()
    
    if choice == "2":
        print("\nTypy médií:")
        for i, t in enumerate(MEDIA_TYPES, 1):
            print(f"  {i}. {t}")
        type_choice = input("Vyber (číslo nebo název): ").strip().lower()
        
        if type_choice.isdigit():
            idx = int(type_choice) - 1
            if 0 <= idx < len(MEDIA_TYPES):
                type_choice = MEDIA_TYPES[idx]
        
        filtered = [r for r in rows if r["typ"].lower() == type_choice]
        print(f"\n--- {type_choice.upper()} ({len(filtered)} záznamů) ---")
        display_entries(filtered)
    elif choice == "3":
        query = input("Hledat: ").strip().lower()
        if query:
            matches = [r for r in rows if query in r["název"].lower() or query in r["autor"].lower()]
            print(f"\n--- Hledání: '{query}' ({len(matches)} výsledků) ---")
            display_entries(matches)
    else:
        print(f"\n--- Všechny záznamy ({len(rows)}) ---")
        display_entries(rows)

def main_menu():
    ensure_csv_exists()
    print("\n╔══════════════════════════╗")
    print("║           DIÁK           ║")
    print("╚══════════════════════════╝")
    
    while True:
        print("\n malý univerzální čtenářskoposluchačskodivácký deník")
        print("\n[z]aznamenat  [p]rocházet  [k]onec")
        choice = input("> ").strip().lower()
        
        if choice in ("z", "zaznamenat"):
            add_entry()
        elif choice in ("p", "procházet", "prochazet"):
            browse_entries()
        elif choice in ("k", "konec", "q", "quit"):
            print("Ahoj!")
            break
        else:
            print("Nechápu. Neznámý příkaz.")

if __name__ == "__main__":
    main_menu()
