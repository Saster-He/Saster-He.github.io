// BWV 846 ribbon: plays the recording and inks the engraved score in time with it.
// Data (data/bwv846.json) is inlined by layouts/partials/score.html; see tools/score/README.md.
(function () {
  "use strict";
  var json = document.getElementById("bwv846-data");
  if (!json) return;
  var d = JSON.parse(json.textContent), sec = json.parentNode, ribbon = sec.querySelector(".ribbon"), track = sec.querySelector(".track");
  var btn = sec.querySelector(".play"), counter = sec.querySelector(".counter"), audio = sec.querySelector("audio");
  var still = window.matchMedia("(prefers-reduced-motion: reduce)");
  var trackW = 0, ribbonW = 0, left = 0, px = 1, offset = 0, raf = 0, hold = 0, bar = 0;

  // Index of the last item whose time is <= t, or -1 if there is none (binary search).
  function find(list, t, time) {
    var lo = -1, hi = list.length;
    while (hi - lo > 1) {
      var mid = (lo + hi) >> 1;
      if (time(list[mid]) <= t) lo = mid; else hi = mid;
    }
    return lo;
  }
  // Position in the score (0..1 of its width) at time t: linear between anchors, clamped at both ends.
  function xAt(anchors, t) {
    var i = find(anchors, t, function (a) { return a[0]; });
    if (i < 0) return anchors[0][1];
    if (i >= anchors.length - 1) return anchors[anchors.length - 1][1];
    var a = anchors[i], b = anchors[i + 1];
    return a[1] + (b[1] - a[1]) * (t - a[0]) / (b[0] - a[0]);
  }

  function measure() {  // also on resize. left: where the ribbon is painted, on whole device pixels
    var r = ribbon.getBoundingClientRect(); px = window.devicePixelRatio || 1;
    trackW = track.getBoundingClientRect().width; ribbonW = r.width; left = Math.round(r.left * px) / px;
  }
  function draw() {
    var t = audio.currentTime, x = xAt(d.anchors, t) * trackW;
    if (!still.matches) offset = x - ribbonW / 3;                        // keep the playhead a third of the way in
    else if (x - offset > ribbonW * 0.85 || x < offset) offset = x - ribbonW * 0.1;  // or turn the page
    offset = Math.max(0, Math.min(offset, trackW - ribbonW + 56));  // +56: the last bar clears the edge fade
    var at = left - offset + x;  // playhead on screen, nudged onto a whole device pixel so the 1px line stays sharp
    track.style.setProperty("--p", x + Math.round(at * px) / px - at + "px");
    track.style.setProperty("--x", x + "px");
    track.style.transform = "translateX(" + -offset + "px)";
    var m = Math.max(1, find(d.barStarts, t, Number) + 1);
    if (m !== bar) counter.textContent = "m. " + (bar = m) + " / " + d.bars;
  }
  function loop() { draw(); raf = requestAnimationFrame(loop); }
  function setButton(playing) {
    btn.setAttribute("aria-pressed", playing);
    btn.removeAttribute("aria-busy");
  }
  function rest() {  // back to the faint, unplayed score; CSS eases the way back unless motion is reduced
    cancelAnimationFrame(raf);
    clearTimeout(hold);
    setButton(false);
    sec.classList.remove("on");
    sec.classList.add("settle");
    counter.hidden = true;
    offset = 0;
    track.style.setProperty("--x", "0px");
    track.style.transform = "";
    if (audio.currentTime) audio.currentTime = 0;
    hold = setTimeout(function () { sec.classList.remove("settle"); }, 1000);
  }

  btn.addEventListener("click", function () {
    if (!audio.paused) { audio.pause(); return; }
    if (audio.readyState < 3) btn.setAttribute("aria-busy", "true");  // first load: show it is buffering
    var p = audio.play();
    if (p) p.catch(function (e) { if (e.name !== "AbortError") rest(); });  // AbortError = paused before it started
  });
  // Any start (the button, or media keys calling play() directly) cancels a pending return to rest.
  audio.addEventListener("play", function () { clearTimeout(hold); sec.classList.remove("settle"); });
  audio.addEventListener("playing", function () {
    measure();
    setButton(true);
    sec.classList.add("on");
    counter.hidden = false;
    cancelAnimationFrame(raf);
    loop();
  });
  audio.addEventListener("pause", function () { cancelAnimationFrame(raf); setButton(false); });
  audio.addEventListener("ended", function () { draw(); hold = setTimeout(rest, 2000); });
  audio.addEventListener("error", rest);
  window.addEventListener("pagehide", function () { audio.pause(); });
  window.addEventListener("resize", function () { measure(); if (sec.classList.contains("on")) draw(); });
})();
