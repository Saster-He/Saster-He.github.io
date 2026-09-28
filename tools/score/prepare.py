"""One-time preparation of the owner's uploads.

    python3 tools/score/prepare.py SOURCE.mxl SOURCE.mp3

Score: the MuseScore export has 34 bars; it is missing standard bar 26
(G D G C F figuration), which is identical to the file's bar 29. A copy of
that bar is inserted after bar 25. Tempo words, credits, fingerings and page
layout are removed, and the part name is hidden. Two engraving fixes in the
left hand: the middle voice (MuseScore voice 6) gets its stems up, and its
16th rests are hidden, because they were drawn on top of the bass note.
Result: tools/score/bwv846.mxl

Audio: the MP3 stream is copied as is; only the cover art, lyrics and comment
tags are removed. Result: static/music/bwv846.mp3
"""
import copy
import io
import shutil
import sys
import zipfile
import xml.etree.ElementTree as ET

sys.dont_write_bytecode = True
from mutagen.id3 import ID3  # noqa: E402

from common import CANON, MP3, SCORE, pcs_str  # noqa: E402

STEP = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
LAYOUT_ATTRS = ("default-x", "default-y", "relative-x", "relative-y", "width")


def read_mxl(path):
    with zipfile.ZipFile(path) as z:
        container = ET.fromstring(z.read("META-INF/container.xml"))
        name = container.find(".//rootfile").get("full-path")
        return ET.fromstring(z.read(name))


def write_mxl(root, path):
    ET.indent(root, space="  ")
    body = ET.tostring(root, encoding="unicode")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 3.1 Partwise//EN" '
           '"http://www.musicxml.org/dtds/partwise.dtd">\n' + body + "\n")
    container = ('<?xml version="1.0" encoding="UTF-8"?>\n<container><rootfiles>'
                 '<rootfile full-path="score.xml" media-type="application/vnd.recordare.musicxml+xml"/>'
                 '</rootfiles></container>\n')
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in (("META-INF/container.xml", container), ("score.xml", xml)):
            info = zipfile.ZipInfo(name, date_time=(2025, 1, 14, 0, 0, 0))  # stable bytes
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, data)
    path.write_bytes(buf.getvalue())


def remove_all(root, tag):
    for parent in list(root.iter()):
        for child in list(parent):
            if child.tag == tag:
                parent.remove(child)


def fix_score(root):
    for tag in ("credit", "defaults", "direction", "print", "fingering"):
        remove_all(root, tag)
    for parent in list(root.iter()):          # drop empty <technical> left by fingerings
        for child in list(parent):
            if child.tag == "technical" and len(child) == 0:
                parent.remove(child)
    for el in root.iter():
        for a in LAYOUT_ATTRS:
            el.attrib.pop(a, None)
    for name in root.iter("part-name"):
        name.set("print-object", "no")
    for abbr in root.iter("part-abbreviation"):
        abbr.set("print-object", "no")
    for note in root.iter("note"):             # left-hand middle voice
        if note.findtext("staff") == "2" and note.findtext("voice") == "6":
            if note.find("rest") is not None:
                note.set("print-object", "no")
            elif note.find("stem") is not None:
                note.find("stem").text = "up"

    (part,) = root.findall("part")
    measures = part.findall("measure")
    assert len(measures) == 34, f"expected the 34-bar upload, got {len(measures)} bars"
    bar = copy.deepcopy(measures[28])          # the file's bar 29
    part.insert(list(part).index(measures[24]) + 1, bar)   # after the file's bar 25
    for i, m in enumerate(part.findall("measure"), 1):
        m.set("number", str(i))
    return root


def bar_contents(measure):
    """Pitch classes and onset positions (in divisions) of one measure."""
    pcs, onsets, pos, last_start = set(), set(), 0, 0
    for el in measure:
        if el.tag == "backup":
            pos -= int(el.findtext("duration"))
        elif el.tag == "forward":
            pos += int(el.findtext("duration"))
        elif el.tag == "note":
            start = last_start if el.find("chord") is not None else pos
            if el.find("chord") is None:
                pos += int(el.findtext("duration") or 0)
            last_start = start
            p = el.find("pitch")
            if p is None:
                continue
            pcs.add((STEP[p.findtext("step")] + int(float(p.findtext("alter") or 0))) % 12)
            if not any(t.get("type") == "stop" for t in el.findall("tie")):
                onsets.add(start)
    return pcs, onsets


def check_score(root):
    measures = root.find("part").findall("measure")
    ok = len(measures) == len(CANON)
    for i, m in enumerate(measures, 1):
        pcs, onsets = bar_contents(m)
        good = pcs == CANON.get(i)
        ok &= good
        print(f"bar {i:2d}: {len(onsets):2d} onsets  {pcs_str(pcs):16s} {'ok' if good else 'MISMATCH, expected ' + pcs_str(CANON[i])}")
    print(f"{len(measures)} bars; pitch classes {'all match' if ok else 'DO NOT match'} the reference list")
    return ok


def strip_tags(src, dst):
    shutil.copyfile(src, dst)
    tags = ID3(dst)
    for key in list(tags.keys()):
        if key.startswith(("APIC", "USLT", "SYLT", "COMM")) or key == "TXXX:UNSYNCEDLYRICS":
            print("removing tag", key)
            del tags[key]
    tags.save(dst, v1=1, padding=lambda info: 0)   # ID3v1 is rewritten without the comment


if __name__ == "__main__":
    src_mxl, src_mp3 = sys.argv[1:3]
    root = fix_score(read_mxl(src_mxl))
    if not check_score(root):
        sys.exit("pitch-class check failed; score not written")
    write_mxl(root, SCORE)
    print("wrote", SCORE)
    strip_tags(src_mp3, MP3)
    print("wrote", MP3)
