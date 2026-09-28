# Score ribbon tools

Offline scripts that make the three files behind the music on the home page:

| File | What it is |
|---|---|
| `static/music/bwv846.svg` | the whole Prelude engraved as one long line of music |
| `static/music/bwv846.mp3` | the recording |
| `data/bwv846.json` | when each bar and each note happens, and where it sits in the SVG |

Hugo does not run anything here. You only need these scripts to change the
engraving or the timing.

## Sources and licences

- **Music:** J. S. Bach, Prelude in C major, BWV 846. Public domain.
- **Recording:** Kimiko Ishizaka, *Open Well-Tempered Clavier*, released under
  CC0 (<https://welltemperedclavier.org/>). The MP3 is the original file with
  the cover art, lyrics and comment tags removed. The audio stream is not
  re-encoded or trimmed.
- **Score:** re-engraved with [Verovio](https://www.verovio.org/) from a
  MuseScore 3.6.2 transcription supplied by the site owner. That file was one
  bar short, so the missing bar was restored (see below). The file names no
  transcriber and states no licence; what is kept here is Bach's text (notes,
  rhythms, voices), without its fingerings, titles or layout. The note shapes
  in the SVG come from the Leland music font (SIL Open Font License 1.1).

### Changes to the transcription (`prepare.py`)

- Standard bar 26 (G D G C F) was missing. It is the same as the file's bar 29,
  so a copy of that bar was put after bar 25. The score now has 35 bars, and
  the pitch classes of every bar match the standard text.
- Tempo words, title and credits, fingerings and page layout were removed. The
  part name is hidden.
- Left hand, middle voice: stems point up, and its sixteenth rests are hidden,
  because in the transcription they were drawn on top of the bass note.

## Files here

| File | Made by | Contents |
|---|---|---|
| `bwv846.mxl` | `prepare.py` | the corrected score (compressed MusicXML) |
| `notes.csv` | `build.py` | one row per note: bar, sixteenth position, pitch, notehead x (0-1) |
| `onsets.csv` | `align.py` | the detected time of every note onset and whether it is trusted |
| `bar_times.csv` | `align.py` | the start of each bar in seconds. **Safe to edit by hand.** |

## Rebuild

From the repository root:

```sh
pip install -r tools/score/requirements.txt
python3 tools/score/build.py     # SVG and notes.csv
python3 tools/score/align.py     # onsets.csv and bar_times.csv (overwrites hand edits)
python3 tools/score/export.py    # data/bwv846.json
```

`prepare.py SOURCE.mxl SOURCE.mp3` was run once on the owner's uploads; you
do not need it again unless you start from a new transcription or recording.

To make the bars wider or narrower, change `spacingLinear` in `build.py`, then
run `build.py` and `export.py`. The timing does not need to be redone.

## How the timing is found

`align.py` finds the start of every note in two independent ways and compares
them:

- **A:** dynamic time warping. Chroma and note-onset features are built from
  the score and lined up with the same features computed from the recording.
- **B:** onset detection. Bars 1-34 have exactly 16 note onsets and bar 35 is
  one chord, so exactly 545 onsets are chosen from the peaks of an onset
  detector. The choice favours strong peaks, peaks where the expected notes
  get louder, and an even tempo.

B is used where its peak is clear and A agrees with it (within 50 ms, after
removing A's constant lag of about 28 ms). The other onsets are placed by
linear interpolation between their neighbours. Two further checks: the
average chroma inside each bar should match that bar's notes better than the
neighbouring bars' notes, and the bar lengths should change smoothly.

Result for the current files: at the 35 bar starts A and B differ by 24 ms
(median) and 46 ms at most; A runs about 28 ms early throughout, and after
removing that the median is 9 ms. 499 of 545 onsets are kept as detected.
Bars 21 and 29 start on a soft low bass note, so their start times are
interpolated. The chroma check passes in 33 of 35 bars (34 with
overtone-aware templates); bar 9 shares three of its four pitch classes with
bar 8 and only the bass note differs, and bar 14 differs from bar 13 by one
note. The chroma change across every barline matches the change of notes.

Known limit: the MP3 is variable bit rate, and browsers seek in such files
only approximately. Played from the start, the ribbon follows the recording
exactly. After someone drags the position in the browser's or the phone's
media controls, Chromium can draw the ribbon up to about 0.4 s behind the
sound until playback goes back to the start. The site's own button never seeks
anywhere except back to the beginning.

## Fixing a bar time by hand

1. Play the recording and note the time where the bar's first note sounds.
2. Change that bar's `start_seconds` in `bar_times.csv` (times must increase).
3. Run `python3 tools/score/export.py`.

The first note of each bar always takes the time from `bar_times.csv`. Inside
the bar, detected onsets that still fall between the new bar start and the
next one are kept; the rest are spaced evenly. `export.py` stops with an
error if the result is not in order.
