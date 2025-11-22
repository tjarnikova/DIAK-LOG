# DIAK-LOG

A small universal reader-listener-viewer diary in python.

*Malý univerzální čtenářskoposluchačskodivácký deník v pythonu.*

Track media from the command line (if you're the kind of person who wants to keep a diary in the command line). 

*Mediální deník v příkazovém řádku, pro lidi co mají rádi příkazový řádek.*

Available in **Czech** (diak) and **English** (loglog).

*K dispozici v češtině (diak) i angličtině (loglog).*

## Usage / Použití

### Recording & Browsing / Zaznamenávání a procházení

```bash
python diak.py      # Česky
python loglog.py    # English
```

This opens an interactive menu where you can:
- **Record** a new entry (date, media type, title, author, rating, notes)
- **Browse** entries chronologically, by media type, or search by title/author

*Otevře se interaktivní menu, kde lze:*
- *Zaznamenat nový záznam (datum, typ, název, autor, hodnocení, poznámky)*
- *Procházet záznamy chronologicky, podle typu, nebo hledat podle názvu/autora*

### Exporting to Text / Export do textu

```bash
# Czech / Česky
python diak_export.py chrono   # → diak_chrono.txt
python diak_export.py typ      # → diak_typ.txt

# English / Anglicky
python loglog-export.py chrono # → loglog_chrono.txt
python loglog-export.py type   # → loglog_type.txt
```

## Media Types / Typy médií

| Česky | English |
|-------|---------|
| kniha | book |
| článek | article |
| podcast | podcast |
| video | video |
| hudba | music |
| film | film |
| seriál | series |
| výstava | exhibition |
| přednáška | lecture |
| divadlo | theatre |
| jiné | other |

## Files / Soubory

| File / Soubor | Description / Popis |
|---------------|---------------------|
| `diak.py` | Hlavní program (česky) |
| `diak_export.py` | Export (česky) |
| `diak.csv` | Data (česky) |
| `loglog.py` | Main program (English) |
| `loglog-export.py` | Export tool (English) |
| `loglog.csv` | Data file (English) |

## Requirements / Požadavky

Python 3.6+ (no external dependencies / bez externích závislostí)

🦭🎧