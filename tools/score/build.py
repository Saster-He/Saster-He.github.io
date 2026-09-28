"""Engrave the corrected score as one continuous system.

    python3 tools/score/build.py

Writes static/music/bwv846.svg (compact SVG, viewBox only, black on
transparent) and tools/score/notes.csv (one row per sounding note: bar, 16th
position in the bar, score time in quarters, MIDI pitch, sounding length in
quarters, x of the notehead centre as a fraction of the SVG width).
"""
import csv
import re
import sys
import xml.etree.ElementTree as ET

sys.dont_write_bytecode = True
import verovio  # noqa: E402

from common import NOTES, SCORE, SVG  # noqa: E402

OPTIONS = {
    "breaks": "none", "header": "none", "footer": "none", "mnumInterval": 0,
    "adjustPageHeight": True, "adjustPageWidth": True, "svgViewBox": True,
    "font": "Leland",
    "spacingLinear": 0.45,      # a bar is about 2x as wide as the image is tall
    "spacingNonLinear": 0.6,
    "pageMarginLeft": 60, "pageMarginRight": 20, "pageMarginTop": 20, "pageMarginBottom": 20,
}
SVGNS = "http://www.w3.org/2000/svg"
XLINK = "{http://www.w3.org/1999/xlink}href"
ET.register_namespace("", SVGNS)


def q(tag):
    return f"{{{SVGNS}}}{tag}"


def render():
    tk = verovio.toolkit()
    tk.setOptions(OPTIONS)
    if not tk.loadFile(str(SCORE)):
        sys.exit(f"could not load {SCORE}")
    assert tk.getPageCount() == 1
    return tk, tk.renderToSVG(1)


def page_geometry(svg):
    """Outer viewBox size, inner (definition-scale) width and page-margin offset."""
    root = ET.fromstring(svg)
    outer = [float(v) for v in root.get("viewBox").split()]
    inner_svg = root.find(q("svg"))
    inner = [float(v) for v in inner_svg.get("viewBox").split()]
    margin = inner_svg.find(q("g"))
    tx, ty = map(float, re.match(r"translate\((\S+),\s*(\S+)\)", margin.get("transform")).groups())
    return outer, inner, (tx, ty)


def note_positions(tk, clean_svg):
    """Onsets from the Verovio timemap, sounding lengths through ties, notehead x."""
    tk.setOptions({"svgBoundingBoxes": True})
    svg = tk.renderToSVG(1)
    tk.setOptions({"svgBoundingBoxes": False})
    uses = re.compile(r"<use [^>]*>")
    assert uses.findall(svg) == uses.findall(clean_svg), "layout changed between renders"
    outer, inner, (tx, _) = page_geometry(svg)
    boxes = {}
    for g in ET.fromstring(svg).iter(q("g")):
        if (g.get("class") or "").startswith("note bounding-box"):
            rect = g.find(q("rect"))
            boxes[g.get("id")[5:]] = (float(rect.get("x")), float(rect.get("width")))
    mei = tk.getMEI()
    tie_next = dict(re.findall(r'<tie [^>]*startid="#([^"]+)" endid="#([^"]+)"', mei))
    tied_to = set(tie_next.values())
    timemap = tk.renderToTimemap({})
    off = {i: e["qstamp"] for e in timemap for i in e.get("off", [])}
    rows = []
    for e in timemap:
        for nid in e.get("on", []):
            if nid in tied_to:           # continuation of a tied note: not a new sound
                continue
            end = nid
            while end in tie_next:
                end = tie_next[end]
            qs = float(e["qstamp"])
            bar = int(qs // 4) + 1
            x, w = boxes[nid]
            rows.append({
                "bar": bar, "pos": round((qs - 4 * (bar - 1)) * 4), "qstamp": qs,
                "midi": tk.getMIDIValuesForElement(nid)["pitch"],
                "dur_q": off[end] - qs,
                "x": round((tx + x + w / 2) / inner[2], 6),
            })
    rows.sort(key=lambda r: (r["qstamp"], r["midi"]))
    return rows


def compact_svg(svg):
    """Rewrite Verovio's SVG with the same drawing and far fewer bytes."""
    outer, inner, (tx, ty) = page_geometry(svg)
    src = ET.fromstring(svg)
    defs_src = src.find(q("defs"))
    glyphs = {}
    for g in defs_src:
        (path,) = list(g)
        assert path.tag == q("path") and path.get("transform") == "scale(1,-1)"
        glyphs[g.get("id")] = path.get("d")

    out = ET.Element(q("svg"), {"viewBox": f"0 0 {outer[2]:g} {outer[3]:g}"})
    defs = ET.SubElement(out, q("defs"))
    # Verovio strokes shapes with currentColor (black); fill defaults to black.
    ET.SubElement(out, q("style")).text = "path,polygon,rect,ellipse,polyline{stroke:#000}"
    # Same nesting as Verovio (a single matrix() instead moves a few edge pixels).
    scaled = ET.SubElement(out, q("svg"), {"viewBox": f"0 0 {inner[2]:g} {inner[3]:g}"})
    body = ET.SubElement(scaled, q("g"), {"transform": f"translate({tx:g},{ty:g})"})
    used = {}

    def use(el):
        """<use href=#glyph transform="translate(x, y) scale(s, s)"> -> pre-scaled glyph + x/y."""
        ref = (el.get("href") or el.get(XLINK))[1:]
        x, y, sx, sy = re.fullmatch(
            r"translate\((\S+), (\S+)\) scale\((\S+), (\S+)\)", el.get("transform")).groups()
        key = (ref, sx, sy)
        if key not in used:
            used[key] = f"g{len(used)}"
            ET.SubElement(defs, q("path"), {
                "id": used[key], "transform": f"scale({float(sx):g},{-float(sy):g})", "d": glyphs[ref]})
        return ET.Element(q("use"), {"href": "#" + used[key], "x": x, "y": y})

    def copy(el, parent):
        tag = el.tag.split("}")[1]
        if tag == "use":
            parent.append(use(el))
            return
        if tag == "g":              # Verovio's groups only carry id/class: flatten them
            assert set(el.attrib) <= {"id", "class"}, el.attrib
            for child in el:
                copy(child, parent)
            return
        keep = {a: v for a, v in el.attrib.items() if a not in ("id", "class")}
        ET.SubElement(parent, el.tag, keep)
        assert len(el) == 0, f"unexpected children in <{tag}>"

    margin = src.find(q("svg")).find(q("g"))
    for child in margin:
        copy(child, body)
    text = ET.tostring(out, encoding="unicode").replace(" />", "/>")
    assert "<text" not in text
    return text + "\n"


def main():
    tk, svg = render()
    rows = note_positions(tk, svg)
    with open(NOTES, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    out = compact_svg(svg)
    SVG.write_text(out)
    outer, inner, _ = page_geometry(svg)
    bar_x = sorted({r["x"] for r in rows if r["pos"] == 0})
    widths = sorted(b - a for a, b in zip(bar_x, bar_x[1:]))
    onsets = {(r["bar"], r["pos"]) for r in rows}
    print(f"{len(bar_x)} bars, {len(onsets)} onset positions, {len(rows)} notes -> {NOTES.name}")
    print(f"SVG viewBox {outer[2]:g} x {outer[3]:g}; raw {len(svg) / 1024:.0f} KB -> {len(out) / 1024:.0f} KB; "
          f"median bar width {widths[len(widths) // 2] * outer[2] / outer[3]:.2f} x image height")


if __name__ == "__main__":
    main()
