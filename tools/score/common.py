"""Shared paths and reference data for the BWV 846 score tools."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "tools" / "score"
SCORE = HERE / "bwv846.mxl"          # corrected MusicXML (35 bars)
SVG = ROOT / "static" / "music" / "bwv846.svg"
MP3 = ROOT / "static" / "music" / "bwv846.mp3"
NOTES = HERE / "notes.csv"           # written by build.py: one row per onset position
ONSETS = HERE / "onsets.csv"         # written by align.py: detected onset per position
BAR_TIMES = HERE / "bar_times.csv"   # written by align.py, may be edited by hand
JSON_OUT = ROOT / "data" / "bwv846.json"

BARS = 35

# Pitch classes sounding in each bar of the standard 35-bar text.
# Used to check the corrected score and the audio alignment.
_CANON = """
1 C E G | 2 C D F A | 3 B D G F | 4 C E G | 5 C E A | 6 C D F# A | 7 B D G
8 B C E G | 9 A C E G | 10 D F# A C | 11 G B D | 12 G Bb E C# | 13 F A D
14 F Ab D B | 15 E G C | 16 E F A C | 17 D F A C | 18 G D B F | 19 C E G
20 C G Bb E | 21 F A C E | 22 F# C A Eb | 23 Ab F B C D | 24 G F B D
25 G E C | 26 G D C F | 27 G D B F | 28 G Eb A C F# | 29 G E C | 30 G D C F
31 G D B F | 32 C G Bb E | 33 C F A D | 34 C B G D F E | 35 C E G
"""
_PC = {"C": 0, "C#": 1, "D": 2, "Eb": 3, "E": 4, "F": 5, "F#": 6,
       "G": 7, "Ab": 8, "A": 9, "Bb": 10, "B": 11}
CANON = {}
for item in _CANON.replace("\n", " | ").split("|"):
    if item.strip():
        bar, *names = item.split()
        CANON[int(bar)] = frozenset(_PC[n] for n in names)
assert sorted(CANON) == list(range(1, BARS + 1))

PC_NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]


def pcs_str(pcs):
    return " ".join(PC_NAMES[p] for p in sorted(pcs))
