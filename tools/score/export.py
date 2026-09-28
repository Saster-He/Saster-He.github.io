"""Write data/bwv846.json, the timing data for the score ribbon on the home page.

    python3 tools/score/export.py

Reads tools/score/bar_times.csv (bar starts, may be edited by hand),
tools/score/onsets.csv (the detected time of every note onset and whether it
is trusted), tools/score/notes.csv (notehead positions), and the SVG and MP3.

Anchor times: each bar's first note takes the time in bar_times.csv; other
onsets take their detected time if it is trusted and lies inside its bar;
the rest are interpolated in score time between those fixed points.
"""
import csv
import json
import re
import sys

sys.dont_write_bytecode = True
import numpy as np  # noqa: E402
from mutagen.mp3 import MP3 as Mp3File  # noqa: E402

from common import BAR_TIMES, BARS, JSON_OUT, MP3, NOTES, ONSETS, SVG  # noqa: E402


def read_csv(path):
    with open(path) as f:
        return list(csv.DictReader(f))


def main():
    starts = {int(r["bar"]): float(r["start_seconds"]) for r in read_csv(BAR_TIMES)}
    assert sorted(starts) == list(range(1, BARS + 1)), "bar_times.csv needs bars 1-35"
    starts = [starts[b] for b in range(1, BARS + 1)]
    assert all(a < b for a, b in zip(starts, starts[1:])), "bar starts must increase"

    x_at = {}
    for n in read_csv(NOTES):
        key = (int(n["bar"]), int(n["pos"]))
        x_at[key] = min(x_at.get(key, 1.0), float(n["x"]))
    onsets = read_csv(ONSETS)
    keys = [(int(o["bar"]), int(o["pos"])) for o in onsets]
    assert keys == sorted(x_at), "onsets.csv and notes.csv disagree; rerun align.py"

    q = np.array([(b - 1) * 4 + p / 4 for b, p in keys])     # score time in quarters
    fixed = np.full(len(keys), np.nan)
    for i, ((bar, pos), o) in enumerate(zip(keys, onsets)):
        if pos == 0:
            fixed[i] = starts[bar - 1]
        elif o["confident"] == "1":
            t = float(o["t_detected"])
            end = starts[bar] if bar < BARS else np.inf
            if starts[bar - 1] < t < end:
                fixed[i] = t
    known = ~np.isnan(fixed)
    times = np.where(known, fixed, np.interp(q, q[known], fixed[known]))

    duration = round(Mp3File(MP3).info.length, 3)
    w, h = (json.loads(v) for v in re.search(r'viewBox="0 0 (\S+) (\S+)"', SVG.read_text()).groups())
    anchors = [[round(float(t), 3), round(x_at[k], 6)] for t, k in zip(times, keys)] + [[duration, 1.0]]
    data = {
        "title": "Prelude in C major, BWV 846",
        "bars": BARS,
        "duration": duration,
        "svg": {"width": w, "height": h},
        "barStarts": [round(s, 3) for s in starts],
        "anchors": anchors,
    }
    validate(data)
    head = ",\n".join(f"  {json.dumps(k)}: {json.dumps(v)}" for k, v in data.items() if k != "anchors")
    rows = ",\n".join(f"    {json.dumps(a)}" for a in anchors)
    text = f'{{\n{head},\n  "anchors": [\n{rows}\n  ]\n}}\n'
    assert json.loads(text) == data
    JSON_OUT.write_text(text)
    print(f"wrote {JSON_OUT.relative_to(JSON_OUT.parents[1])}: {len(anchors)} anchors, "
          f"{int(known.sum())} fixed, {int((~known).sum())} interpolated; bar 1 at {starts[0]:.3f} s, "
          f"final chord at {starts[-1]:.3f} s")


def validate(d):
    bars, anchors = d["barStarts"], d["anchors"]
    t = [a[0] for a in anchors]
    x = [a[1] for a in anchors]
    assert len(bars) == d["bars"] == BARS
    assert all(a < b for a, b in zip(bars, bars[1:])) and 0 <= bars[0] and bars[-1] < d["duration"]
    assert all(a < b for a, b in zip(t, t[1:])), "anchor times must strictly increase"
    assert all(a <= b for a, b in zip(x, x[1:])), "anchor x must not decrease"
    assert all(0 <= v <= 1 for v in x)
    assert anchors[-1] == [d["duration"], 1.0]
    assert set(bars) <= set(t), "every bar start is an anchor"
    assert len(anchors) == 34 * 16 + 1 + 1


if __name__ == "__main__":
    main()
