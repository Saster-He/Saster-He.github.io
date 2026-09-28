"""Find when each bar starts in the recording, in two independent ways.

    python3 tools/score/align.py [--plots DIR]

A. DTW. Chroma and note-onset features are synthesised from the score
   (notes.csv) and aligned to the same features computed from the recording.
B. Onset detection that knows the score's shape: bars 1-34 have 16 note
   onsets each and bar 35 is one chord, so exactly 545 onsets are chosen
   from the detected peaks by dynamic programming. It prefers strong peaks,
   peaks where the expected pitch classes get louder, and a smooth tempo.

Checks: A against B for every onset; the recording's chroma inside each bar
against the pitch classes of that bar and its neighbours; bar durations.
Final choice: B's onset where its peak is clear and A agrees; elsewhere
interpolated in score time. Writes tools/score/onsets.csv (B's time for every
onset position and whether it is trusted) and tools/score/bar_times.csv
(bar, start_seconds), which can be edited by hand before running export.py.
"""
import csv
import sys

sys.dont_write_bytecode = True
import librosa  # noqa: E402
import numpy as np  # noqa: E402
import soundfile as sf  # noqa: E402
from scipy.ndimage import maximum_filter1d  # noqa: E402
from scipy.spatial.distance import cdist  # noqa: E402

from common import BAR_TIMES, BARS, CANON, MP3, NOTES, ONSETS  # noqa: E402

SR = 22050
HOP = 441             # 50 frames per second for the DTW features
FPS = SR / HOP
OHOP = 110            # about 5 ms for onset detection
OFPS = SR / OHOP


def load_audio():
    y, sr = sf.read(MP3, dtype="float32")
    return librosa.resample(y.mean(axis=1), orig_sr=sr, target_sr=SR), len(y) / sr


def load_events():
    """One event per onset position: bar, pos, score time (quarters), pitches."""
    events = {}
    with open(NOTES) as f:
        for n in csv.DictReader(f):
            key = (int(n["bar"]), int(n["pos"]))
            ev = events.setdefault(key, {"bar": key[0], "pos": key[1], "q": float(n["qstamp"]), "notes": []})
            ev["notes"].append((int(n["midi"]), float(n["dur_q"])))
    return [events[k] for k in sorted(events)]


# ---------------------------------------------------------------- method A
DECAY = np.sqrt(1 - np.arange(10) / 10)   # 200 ms tail after each onset


def with_decay(x):
    out = x.copy()
    for k, w in enumerate(DECAY[1:], 1):
        out[:, k:] = np.maximum(out[:, k:], w * x[:, :-k])
    return out


def unit(x):
    x = x + 1e-3                     # silence becomes a flat vector, not zero
    return x / np.linalg.norm(x, axis=0, keepdims=True)


def unit_rows(x):
    return x / np.linalg.norm(x, axis=1, keepdims=True)


def audio_features(y):
    tuning = librosa.estimate_tuning(y=y, sr=SR)       # the piano is a little sharp of A440
    cqt = np.abs(librosa.cqt(y, sr=SR, hop_length=HOP, fmin=librosa.note_to_hz("C1"), n_bins=84,
                             tuning=tuning))
    chroma = librosa.feature.chroma_cqt(C=cqt, sr=SR, hop_length=HOP, fmin=librosa.note_to_hz("C1"),
                                        bins_per_octave=12, norm=None, tuning=tuning)
    spec = np.log1p(100 * np.abs(librosa.stft(y, n_fft=2048, hop_length=HOP)))
    flux = np.maximum(0, np.diff(spec, axis=1, prepend=spec[:, :1]))
    onset = librosa.filters.chroma(sr=SR, n_fft=2048) @ flux
    onset /= np.maximum(maximum_filter1d(np.linalg.norm(onset, axis=0), int(2 * FPS)), 1e-6)
    return chroma, with_decay(onset)


def score_features(events, n_frames, lead):
    """Piano-roll chroma (pedalled to the half bar, decaying) and onset impulses."""
    fpq = (n_frames - lead) / 140                      # 35 bars of 4 quarters
    chroma = np.zeros((12, n_frames))
    onset = np.zeros((12, n_frames))
    decay = np.exp(-np.arange(n_frames) / (1.5 * FPS))
    for ev in events:
        on = int(round(lead + ev["q"] * fpq))
        ev["frame"] = on
        for midi, dur in ev["notes"]:
            end_q = max(ev["q"] + dur, 2 * np.floor(ev["q"] / 2) + 2)
            end = min(n_frames, int(round(lead + end_q * fpq)))
            chroma[midi % 12, on:end] += decay[:end - on]
            onset[midi % 12, on] = 1
    return chroma, with_decay(onset)


def method_a(y, events):
    chroma_a, onset_a = audio_features(y)
    n = chroma_a.shape[1]
    rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=HOP)[0]
    lead = int(np.argmax(rms > rms.max() * 10 ** (-40 / 20)))     # first sound, -40 dB
    chroma_s, onset_s = score_features(events, n, lead)
    cost = cdist(unit(np.log1p(10 * chroma_s)).T, unit(np.log1p(10 * chroma_a)).T, "cosine")
    cost += cdist(onset_s.T, onset_a.T, "euclidean")
    _, path = librosa.sequence.dtw(C=cost)
    path = path[::-1]
    times = np.array([np.median(path[path[:, 0] == ev["frame"], 1]) / FPS for ev in events])
    return times, chroma_a


# ---------------------------------------------------------------- method B
IOI_MIN, IOI_MAX = 0.10, 0.90     # seconds between consecutive 16ths
MAX_BACK = 12                     # candidates considered between two onsets
SMOOTH = 4.0                      # weight of the tempo-change penalty


def candidates(y):
    """Onset peaks: time, strength against the local loudness, and which
    pitch classes got louder at that moment (unit 12-vector)."""
    env = librosa.onset.onset_strength(y=y, sr=SR, hop_length=OHOP, n_fft=1024, lag=1, max_size=3)
    peaks = librosa.util.peak_pick(env, pre_max=6, post_max=6, pre_avg=20, post_avg=20, delta=0, wait=10)
    t, s = peaks / OFPS, env[peaks]
    ref = np.array([np.percentile(s[np.abs(t - ti) < 4], 90) for ti in t])   # local loudness
    strength = np.minimum(s / np.maximum(ref, 0.25 * np.percentile(s, 90)), 1.5)
    spec = np.log1p(100 * np.abs(librosa.stft(y, n_fft=2048, hop_length=OHOP))).astype(np.float32)
    rise = librosa.filters.chroma(sr=SR, n_fft=2048) @ np.maximum(0, spec[:, 4:] - spec[:, :-4])
    pitch = np.stack([rise[:, max(0, p - 6):p + 4].sum(axis=1) for p in peaks], axis=1)
    return t, strength, pitch / np.maximum(np.linalg.norm(pitch, axis=0), 1e-9)


def method_b(y, events):
    """Pick exactly one peak per onset position, in order. Reward: peak strength
    plus how well its pitch classes match the notes expected there. Penalty:
    change of the time between onsets (squared log ratio)."""
    t, strength, pitch = candidates(y)
    expected = np.zeros((len(events), 12))
    for e, ev in enumerate(events):
        expected[e, [midi % 12 for midi, _ in ev["notes"]]] = 1
    reward = strength[None, :] + unit_rows(expected) @ pitch            # (events, peaks)

    m, back = len(t), MAX_BACK
    j = np.arange(m)[:, None]
    prev = j - np.arange(1, back + 1)[None, :]                        # (m, back) predecessor index
    ok = prev >= 0
    pi = np.maximum(prev, 0)
    ioi = t[j] - t[pi]
    ok &= (ioi >= IOI_MIN) & (ioi <= IOI_MAX)
    log_ioi = np.log(np.where(ok, ioi, 1.0))
    penalty = SMOOTH * (log_ioi[:, :, None] - log_ioi[pi]) ** 2      # (m, back, back)
    penalty[~ok] = np.inf
    penalty[~ok[pi]] = np.inf

    # score[j, k]: best total with the current onset at peak j and the previous at j-k-1
    score = np.where(ok, reward[1][j] + reward[0][pi], -np.inf)
    pointers = []
    for e in range(2, len(events) - 1):
        total = score[pi] - penalty
        pointers.append(np.argmax(total, axis=2))
        score = reward[e][j] + np.max(total, axis=2)
        score[~ok] = -np.inf
    # the final chord: any gap up to 4 s after the last 16th, no tempo penalty
    best_prev = np.max(score, axis=1)
    last = np.full(m, -np.inf)
    last_from = np.zeros(m, int)
    for c in range(m):
        cand = np.where((t < t[c] - IOI_MIN) & (t > t[c] - 4))[0]
        if len(cand):
            i = cand[np.argmax(best_prev[cand])]
            last[c], last_from[c] = reward[-1][c] + best_prev[i], i
    c = int(np.argmax(last))
    chosen = [c, last_from[c]]
    k = int(np.argmax(score[chosen[-1]]))
    for ptr in reversed(pointers):
        cur = chosen[-1]
        chosen.append(cur - k - 1)
        k = int(ptr[cur, k])
    chosen.append(chosen[-1] - k - 1)
    chosen = chosen[::-1]
    assert len(chosen) == len(events) and np.all(np.diff(t[chosen]) > 0)
    # a chord may be spread a little: take its first sound
    early = np.where((t < t[c]) & (t > max(t[c] - 0.15, t[chosen[-2]])) & (strength > 0.3 * strength[c]))[0]
    if len(early):
        chosen[-1] = int(early[0])
    match = (unit_rows(expected) @ pitch)[:, chosen]           # (expected at e, peak of e')
    own = np.diag(match)
    wins = sum(own[e] > max(match[e - 1, e] if e else -1, match[e + 1, e] if e + 1 < len(own) else -1)
               for e in range(len(own)))
    return t[chosen], strength[chosen], own, wins


# ---------------------------------------------------------------- choice
def combine(events, t_b, strength, t_a):
    """Keep B's onset where its peak is clear and A agrees (after removing A's
    constant lag); elsewhere interpolate in score time between kept onsets."""
    offset = np.median(t_b - t_a)
    confident = (strength >= 0.25) & (np.abs(t_b - t_a - offset) <= 0.05)
    confident[[0, -1]] = True                  # the interpolation needs both ends
    q = np.array([ev["q"] for ev in events])
    final = np.where(confident, t_b, np.interp(q, q[confident], t_b[confident]))
    return final, confident, offset


# ---------------------------------------------------------------- checks
def template(pcs, overtones):
    """12-bin pitch-class template; with overtones, harmonics 2-6 of each note
    are added with weight 0.4^(h-1) (piano tone puts energy a fifth and a
    major third above each note)."""
    v = np.zeros(12)
    for p in pcs:
        for h in range(1, 7 if overtones else 2):
            v[(p + round(12 * np.log2(h))) % 12] += 0.4 ** (h - 1)
    return v


def chroma_check(chroma, bounds, overtones):
    """Mean chroma of each bar against its own reference pitch classes and
    those of the previous and next bar. Returns rows and the number of wins."""
    rows = []
    for b in range(1, BARS + 1):
        mean = chroma[:, int(bounds[b - 1] * FPS):int(bounds[b] * FPS)].mean(axis=1)
        corr = {nb: float(np.corrcoef(mean, template(CANON[nb], overtones))[0, 1])
                for nb in (b - 1, b, b + 1) if nb in CANON}
        rows.append((b, corr.get(b - 1), corr[b], corr.get(b + 1), max(corr, key=corr.get)))
    return rows, sum(r[4] == r[0] for r in rows)


def change_check(chroma, bounds):
    """For each barline: does the chroma change from one bar to the next
    correlate with the change of reference pitch classes?"""
    means = [chroma[:, int(bounds[b] * FPS):int(bounds[b + 1] * FPS)].mean(axis=1) for b in range(BARS)]
    return [float(np.corrcoef(means[b] - means[b - 1],
                              template(CANON[b + 1], False) - template(CANON[b], False))[0, 1])
            for b in range(1, BARS)]


def fmt(v):
    return "   -  " if v is None else f"{v:6.3f}"


def ms(x):
    return f"{x * 1000:.0f} ms"


def main():
    plots = sys.argv[sys.argv.index("--plots") + 1] if "--plots" in sys.argv else None
    y, duration = load_audio()
    events = load_events()
    assert len(events) == 34 * 16 + 1
    first = [i for i, ev in enumerate(events) if ev["pos"] == 0]
    t_a, chroma = method_a(y, events)
    t_b, strength, match, pitch_wins = method_b(y, events)
    final, confident, offset = combine(events, t_b, strength, t_a)
    starts = final[first]

    print("== A (DTW) vs B (onsets + DP)")
    for name, idx in (("all 545 onsets", slice(None)), ("35 bar starts", first)):
        d = (t_b - t_a)[idx]
        dc = np.abs(d - offset)
        print(f"{name}: |B-A| median {ms(np.median(np.abs(d)))}, max {ms(np.abs(d).max())}; "
              f"after removing the constant lag {ms(offset)}: median {ms(np.median(dc))}, "
              f"90th pct {ms(np.percentile(dc, 90))}, max {ms(dc.max())}")
    over = [events[i]["bar"] for i in first if abs(t_b[i] - t_a[i]) > 0.08]
    print(f"bars whose starts differ by more than 80 ms: {over or 'none'}")
    print(f"B's chosen peaks: the pitch classes that got louder match the expected notes better "
          f"than the previous/next onset's notes at {pitch_wins} of {len(events)} onsets "
          f"(median match {np.median(match):.2f}; 1 = only the expected pitch classes)")
    print(f"kept as detected: {confident.sum()} of {len(events)} onsets, "
          f"{confident[first].sum()} of {BARS} bar starts; interpolated bar starts: "
          f"{[events[i]['bar'] for i in first if not confident[i]]}")

    bounds = list(starts) + [min(duration, starts[-1] + 3)]
    tables = []
    print("== chroma of each bar vs reference pitch classes (own vs previous/next bar)")
    for overtones in (False, True):
        rows, wins = chroma_check(chroma, bounds, overtones)
        label = "templates with overtones" if overtones else "plain templates"
        lost = [b for b, *_, best in rows if best != b]
        print(f"{label}: own bar wins in {wins} of {BARS} bars; not won: {lost or 'none'}")
        tables += [label, "bar   prev    own    next  best",
                   *(f"{b:3d} {fmt(p)} {fmt(o)} {fmt(n)}  {best:3d}{'' if best == b else '  <--'}"
                     for b, p, o, n, best in rows), ""]

    change = np.array(change_check(chroma, bounds))
    print(f"chroma change across each barline vs change of reference pitch classes: correlation "
          f"min {change.min():.2f} (barline {int(np.argmin(change)) + 1}|{int(np.argmin(change)) + 2}), "
          f"median {np.median(change):.2f}, negative at {int((change <= 0).sum())} of {BARS - 1} barlines")
    tables += ["barline change correlation", " ".join(f"{b}|{b + 1}:{c:.2f}" for b, c in enumerate(change, 1)), ""]

    durs = np.diff(starts)
    step = np.abs(durs[1:] / durs[:-1] - 1)
    print("== tempo")
    print("bar durations (s):", " ".join(f"{x:.2f}" for x in durs))
    print(f"bars 1-33: {durs[:-1].min():.2f}-{durs[:-1].max():.2f} s; largest change between "
          f"neighbouring bars {step.max() * 100:.0f}% (bars {int(np.argmax(step)) + 1}-{int(np.argmax(step)) + 2}); "
          f"last three bars {durs[-3:].round(2).tolist()} s")
    print(f"bar 1 starts at {starts[0]:.3f} s, final chord at {starts[-1]:.3f} s, audio {duration:.2f} s")

    with open(ONSETS, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["bar", "pos", "t_detected", "strength", "confident"])
        for ev, tb, s, c in zip(events, t_b, strength, confident):
            w.writerow([ev["bar"], ev["pos"], f"{tb:.3f}", f"{s:.2f}", int(c)])
    with open(BAR_TIMES, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["bar", "start_seconds"])
        for b, s in enumerate(starts, 1):
            w.writerow([b, f"{s:.3f}"])
    print("wrote", ONSETS.name, "and", BAR_TIMES.name)

    if plots:
        save_plots(plots, events, t_a, t_b, final, first, tables)


def save_plots(folder, events, t_a, t_b, final, first, tables):
    from pathlib import Path
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    out = Path(folder)
    out.mkdir(parents=True, exist_ok=True)
    (out / "chroma_check.txt").write_text("\n".join(tables))
    with open(out / "onsets_a_b.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["bar", "pos", "t_a", "t_b", "t_final"])
        for ev, a, b, c in zip(events, t_a, t_b, final):
            w.writerow([ev["bar"], ev["pos"], f"{a:.3f}", f"{b:.3f}", f"{c:.3f}"])
    ink, muted, grid = "#0b0b0b", "#52514e", "#e4e3df"
    fig, (top, bottom) = plt.subplots(2, 1, figsize=(9, 5.2), dpi=130, sharex=True,
                                      gridspec_kw={"height_ratios": [3, 2]})
    bars = np.arange(1, BARS)
    top.plot(bars, np.diff(t_a[first]), "-o", color="#2a78d6", lw=2, ms=5, label="A: DTW")
    top.plot(bars, np.diff(t_b[first]), "-s", color="#eb6834", lw=2, ms=4, label="B: onsets + DP")
    top.set_ylabel("bar duration (s)", color=muted)
    top.set_title("BWV 846, Ishizaka: duration of each bar", loc="left", color=ink, fontsize=11)
    top.legend(frameon=False, loc="upper left")
    diff = (t_b - t_a)[first] * 1000
    bottom.axhline(0, color=muted, lw=1)
    bottom.bar(np.arange(1, BARS + 1), diff, width=0.6, color="#2a78d6")
    bottom.set_ylabel("bar start, B - A (ms)", color=muted)
    bottom.set_xlabel("bar", color=muted)
    bottom.set_xticks(range(1, BARS + 1, 2))
    for ax in (top, bottom):
        ax.grid(axis="y", color=grid, lw=0.8)
        ax.set_axisbelow(True)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        ax.tick_params(colors=muted)
    fig.tight_layout()
    fig.savefig(out / "bar_durations.png")


if __name__ == "__main__":
    main()
