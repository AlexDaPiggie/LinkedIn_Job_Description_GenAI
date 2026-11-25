/* Shared engine for the animated explainers (How it works, Evaluation).
 *
 * Everything on screen is a pure function of the playhead time T (seconds).
 * A page's build function only adds keyframes with the helpers below and
 * returns its captions and chapters; render(T) applies the keyframes. That
 * makes play, pause, seeking and chapter jumps all the same operation.
 *
 * Usage: window.Explainer(svgElement, (h) => { ...scenes...; return { CAPTIONS, CHAPTERS, DUR, POSTER }; });
 */
window.Explainer = function (svg, build) {
  const NS = "http://www.w3.org/2000/svg";

  const C = {
    ink: "#0e1d36", soft: "#3b4d6b", muted: "#5c6b8c", line: "#d3dcee",
    blue: "#0a66c2", deep: "#073f7a", tint: "#eaf3ff", paper: "#ffffff", canvas: "#f4f7fc",
    green: "#087852", greenSoft: "#e3f4ec", red: "#b3261e", redSoft: "#fdecea",
    amber: "#9a6400", amberSoft: "#fdf3e1",
  };

  /* ---------- Easing ---------- */
  const lin = (p) => p;
  const smooth = (p) => (p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2);
  const back = (p) => 1 + 2.70158 * Math.pow(p - 1, 3) + 1.70158 * Math.pow(p - 1, 2);
  const clamp = (v) => Math.max(0, Math.min(1, v));

  /* ---------- Keyframe tracks ---------- */
  const tracks = new Map();
  function K(node, prop, ...keys) {
    let props = tracks.get(node);
    if (!props) { props = {}; tracks.set(node, props); }
    (props[prop] = props[prop] || []).push(...keys);
    props[prop].sort((a, b) => a[0] - b[0]);
    return node;
  }

  function mixColor(a, b, p) {
    const pa = parseInt(a.slice(1), 16), pb = parseInt(b.slice(1), 16);
    const ch = (v, s) => (v >> s) & 255;
    const m = (s) => Math.round(ch(pa, s) + (ch(pb, s) - ch(pa, s)) * p);
    return `rgb(${m(16)},${m(8)},${m(0)})`;
  }

  function valueAt(keys, T) {
    if (T <= keys[0][0]) return keys[0][1];
    for (let i = 0; i < keys.length - 1; i++) {
      const a = keys[i], b = keys[i + 1];
      if (T < b[0]) {
        const span = b[0] - a[0];
        const p = span <= 0 ? 1 : (T - a[0]) / span;
        const e = (b[2] || smooth)(clamp(p));
        if (typeof a[1] === "number") return a[1] + (b[1] - a[1]) * e;
        if (typeof a[1] === "string" && a[1][0] === "#") return mixColor(a[1], b[1], e);
        return e < 1 ? a[1] : b[1];
      }
    }
    return keys[keys.length - 1][1];
  }

  function apply(node, st) {
    if ("o" in st) node.setAttribute("opacity", clamp(st.o).toFixed(3));
    if ("x" in st || "y" in st || "s" in st || "sy" in st) {
      const b = node._base || [0, 0];
      const x = "x" in st ? st.x : b[0];
      const y = "y" in st ? st.y : b[1];
      let tr = `translate(${x.toFixed(2)} ${y.toFixed(2)})`;
      if ("s" in st) tr += ` scale(${Math.max(0.001, st.s).toFixed(4)})`;
      if ("sy" in st) tr += ` scale(1 ${Math.max(0.001, st.sy).toFixed(4)})`;
      node.setAttribute("transform", tr);
    }
    if ("draw" in st) {
      const L = node._len;
      node.setAttribute("stroke-dasharray", `${L} ${L}`);
      node.setAttribute("stroke-dashoffset", (L * (1 - clamp(st.draw))).toFixed(2));
    }
    if ("type" in st) {
      const s = node._full.slice(0, Math.round(clamp(st.type) * node._full.length));
      if (node.textContent !== s) node.textContent = s;
    }
    if ("num" in st) {
      const n = node._dec ? st.num.toFixed(node._dec) : String(Math.round(st.num));
      const s = (node._pre || "") + n + (node._suf || "");
      if (node.textContent !== s) node.textContent = s;
    }
    if ("text" in st && node.textContent !== st.text) node.textContent = st.text;
    if ("fill" in st) node.setAttribute("fill", st.fill);
    if ("stroke" in st) node.setAttribute("stroke", st.stroke);
    if ("fo" in st) node.setAttribute("fill-opacity", clamp(st.fo).toFixed(3));
  }

  function render(T) {
    for (const [node, props] of tracks) {
      const st = {};
      for (const prop in props) st[prop] = valueAt(props[prop], T);
      apply(node, st);
    }
  }

  /* ---------- Primitives ---------- */
  // Pushes every keyframe at or after `from` later by `delta` seconds, to make room for a new scene.
  function shiftAfter(from, delta) {
    for (const props of tracks.values()) {
      for (const prop in props) {
        for (const key of props[prop]) if (key[0] >= from) key[0] += delta;
      }
    }
  }

  function el(tag, attrs, parent) {
    const n = document.createElementNS(NS, tag);
    for (const k in attrs) n.setAttribute(k, attrs[k]);
    (parent || svg).appendChild(n);
    return n;
  }

  function group(parent, base) {
    const g = el("g", {}, parent);
    if (base) {
      g._base = base;
      g._pos = base.slice();
      g.setAttribute("transform", `translate(${base[0]} ${base[1]})`);
    }
    return g;
  }

  function txt(parent, x, y, str, o = {}) {
    const n = el("text", {
      x, y,
      "font-size": o.size || 20,
      "font-weight": o.weight || 500,
      fill: o.fill || C.ink,
      "text-anchor": o.anchor || "middle",
      class: "ex-" + (o.font || "body"),
    }, parent);
    n.textContent = str;
    n._full = str;
    return n;
  }

  const appear = (n, t, d = 0.5) => K(n, "o", [t, 0], [t + d, 1]);
  const hide = (n, t, d = 0.5) => K(n, "o", [t, 1], [t + d, 0]);
  const write = (n, t, d = 0.6) => K(n, "type", [t, 0], [t + d, 1, lin]);
  // Also hidden until drawing starts: a round line cap would otherwise show as a dot at length 0.
  const draw = (n, t, d = 0.7) => { K(n, "o", [t, 0], [t + 0.02, 1, lin]); return K(n, "draw", [t, 0], [t + d, 1]); };
  const pop = (n, t) => { K(n, "o", [t, 0], [t + 0.3, 1]); K(n, "s", [t, 0.6], [t + 0.45, 1, back]); return n; };

  function moveTo(node, t, d, x, y, ease) {
    const [cx, cy] = node._pos || node._base || [0, 0];
    K(node, "x", [t, cx], [t + d, x, ease]);
    K(node, "y", [t, cy], [t + d, y, ease]);
    node._pos = [x, y];
  }

  function travel(node, path, t0, t1, n = 28) {
    const L = path.getTotalLength();
    for (let i = 0; i <= n; i++) {
      const p = i / n;
      const pt = path.getPointAtLength(smooth(p) * L);
      const tt = t0 + (t1 - t0) * p;
      K(node, "x", [tt, pt.x, lin]);
      K(node, "y", [tt, pt.y, lin]);
    }
    const end = path.getPointAtLength(L);
    node._pos = [end.x, end.y];
  }

  function box(parent, { x, y, w, h, label, sub, stroke = C.blue, size = 22 }) {
    const g = el("g", {}, parent);
    const r = el("rect", {
      x: x - w / 2, y: y - h / 2, width: w, height: h, rx: 12,
      fill: C.paper, "fill-opacity": 0, stroke, "stroke-width": 2.5,
    }, g);
    r._len = 2 * (w + h);
    const lab = txt(g, x, sub ? y - 3 : y + 8, label, { size, weight: 600 });
    const sb = sub ? txt(g, x, y + 22, sub, { size: 15, font: "mono", fill: C.muted }) : null;
    return { g, r, lab, sb, x, y, w, h };
  }

  function showBox(b, t) {
    draw(b.r, t, 0.7);
    K(b.r, "fo", [t + 0.3, 0], [t + 0.8, 1]);
    write(b.lab, t + 0.45, 0.45);
    if (b.sb) write(b.sb, t + 0.7, 0.5);
  }

  function cylinder(parent, { x, y, w, h, label, sub }) {
    const g = el("g", {}, parent);
    const ry = 15, top = y - h / 2, bot = y + h / 2;
    const body = el("path", {
      d: `M${x - w / 2},${top} L${x - w / 2},${bot} A${w / 2},${ry} 0 0 0 ${x + w / 2},${bot} L${x + w / 2},${top}`,
      fill: C.paper, "fill-opacity": 0, stroke: C.deep, "stroke-width": 2.5,
    }, g);
    body._len = body.getTotalLength();
    const lid = el("ellipse", { cx: x, cy: top, rx: w / 2, ry, fill: C.tint, "fill-opacity": 0, stroke: C.deep, "stroke-width": 2.5 }, g);
    lid._len = 2 * Math.PI * Math.sqrt((w * w / 4 + ry * ry) / 2);
    const lab = txt(g, x, y + 12, label, { size: 22, weight: 600 });
    const sb = sub ? txt(g, x, y + 36, sub, { size: 15, font: "mono", fill: C.muted }) : null;
    return { g, body, lid, lab, sb };
  }

  function showCylinder(c, t) {
    draw(c.body, t, 0.7);
    draw(c.lid, t + 0.1, 0.6);
    K(c.body, "fo", [t + 0.3, 0], [t + 0.8, 1]);
    K(c.lid, "fo", [t + 0.3, 0], [t + 0.8, 1]);
    write(c.lab, t + 0.45, 0.45);
    if (c.sb) write(c.sb, t + 0.7, 0.5);
  }

  function edge(parent, d, { label, lx, ly, color = C.blue } = {}) {
    const g = el("g", {}, parent);
    const p = el("path", { d, fill: "none", stroke: color, "stroke-width": 2.2, "stroke-linecap": "round" }, g);
    p._len = p.getTotalLength();
    const end = p.getPointAtLength(p._len);
    const pre = p.getPointAtLength(Math.max(0, p._len - 8));
    const ang = (Math.atan2(end.y - pre.y, end.x - pre.x) * 180) / Math.PI;
    const head = el("path", {
      d: "M2,0 L-11,-6.5 L-11,6.5 Z", fill: color, opacity: 0,
      transform: `translate(${end.x} ${end.y}) rotate(${ang})`,
    }, g);
    let lab = null;
    if (label) {
      lab = el("g", { opacity: 0 }, g);
      const w = label.length * 8.4 + 22;
      el("rect", { x: lx - w / 2, y: ly - 14, width: w, height: 27, rx: 13.5, fill: C.paper, stroke: C.line }, lab);
      txt(lab, lx, ly + 5, label, { size: 14, font: "mono", fill: C.soft });
    }
    return { g, p, head, lab };
  }

  function showEdge(e, t, d = 0.7) {
    draw(e.p, t, d);
    K(e.head, "o", [t + d - 0.15, 0], [t + d, 1]);
    if (e.lab) appear(e.lab, t + d * 0.5, 0.4);
  }

  function chip(parent, { label, x, y, fill = C.tint, stroke = C.blue, color = C.deep, size = 15, w, font = "mono" }) {
    const g = group(parent, [x, y]);
    const width = w || label.length * size * 0.62 + 26;
    const r = el("rect", { x: -width / 2, y: -17, width, height: 34, rx: 8, fill, stroke, "stroke-width": 1.8 }, g);
    const t = txt(g, 0, 5, label, { size, font, fill: color, weight: 600 });
    g._rect = r;
    g._text = t;
    g._w = width;
    return g;
  }

  function checkIcon(parent, x, y, s = 1, color = C.green) {
    const p = el("path", {
      d: `M${x - 8 * s},${y} L${x - 2 * s},${y + 6 * s} L${x + 9 * s},${y - 7 * s}`,
      fill: "none", stroke: color, "stroke-width": 3.2, "stroke-linecap": "round", "stroke-linejoin": "round",
    }, parent);
    p._len = p.getTotalLength();
    return p;
  }

  function crossIcon(parent, x, y, s = 1, color = C.red) {
    const k = 7 * s;
    const p = el("path", {
      d: `M${x - k},${y - k} L${x + k},${y + k} M${x + k},${y - k} L${x - k},${y + k}`,
      fill: "none", stroke: color, "stroke-width": 3.2, "stroke-linecap": "round",
    }, parent);
    p._len = p.getTotalLength();
    return p;
  }

  function lockIcon(parent, x, y) {
    const g = el("g", {}, parent);
    el("path", { d: `M${x - 7},${y - 4} V${y - 10} A7,7 0 0 1 ${x + 7},${y - 10} V${y - 4}`, fill: "none", stroke: C.deep, "stroke-width": 2.6 }, g);
    el("rect", { x: x - 11, y: y - 5, width: 22, height: 17, rx: 3, fill: C.deep }, g);
    return g;
  }

  /* ---------- Background ---------- */
  const defs = el("defs", {});
  const pat = el("pattern", { id: "exDots", width: 32, height: 32, patternUnits: "userSpaceOnUse" }, defs);
  el("circle", { cx: 1.5, cy: 1.5, r: 1.3, fill: C.line }, pat);
  el("rect", { x: 0, y: 0, width: 1280, height: 720, fill: C.canvas });
  el("rect", { x: 0, y: 0, width: 1280, height: 720, fill: "url(#exDots)" });

  const { CAPTIONS, CHAPTERS, DUR, POSTER } = build({ shiftAfter, C, K, el, group, txt, appear, hide, write, draw, pop, moveTo, travel, box, showBox, cylinder, showCylinder, edge, showEdge, chip, checkIcon, crossIcon, lockIcon, lin, smooth, back, svg });

  /* ---------- Player ---------- */
  const fig = svg.closest(".explainer");
  const playBtn = fig.querySelector(".ex-play");
  const bigPlay = fig.querySelector(".ex-big-play");
  const seek = fig.querySelector(".ex-seek");
  const timeEl = fig.querySelector(".ex-time");
  const capEl = fig.querySelector(".ex-caption");
  const speedBtn = fig.querySelector(".ex-speed");
  const fsBtn = fig.querySelector(".ex-fs");
  const chapList = fig.querySelector(".ex-chapters");
  const ticks = fig.querySelector(".ex-ticks");

  let T = POSTER;
  let playing = false;
  let started = false;
  let last = 0;
  let speed = 1;
  let capIdx = -1;

  const fmt = (s) => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, "0")}`;

  seek.max = String(DUR * 10);
  CHAPTERS.forEach(([t, name], i) => {
    const li = document.createElement("li");
    const b = document.createElement("button");
    b.type = "button";
    const ts = document.createElement("span");
    ts.className = "ex-chap-time";
    ts.textContent = fmt(t);
    b.append(ts, document.createTextNode(name));
    b.addEventListener("click", () => { started = true; bigPlay.hidden = true; setT(t); if (!playing) play(); });
    li.appendChild(b);
    chapList.appendChild(li);
    if (i > 0) {
      const tick = document.createElement("span");
      tick.style.left = `${(t / DUR) * 100}%`;
      ticks.appendChild(tick);
    }
  });
  const chapBtns = [...chapList.querySelectorAll("button")];

  function update() {
    render(T);
    seek.value = String(Math.round(T * 10));
    seek.style.setProperty("--p", `${(T / DUR) * 100}%`);
    timeEl.textContent = `${fmt(T)} / ${fmt(DUR)}`;
    const i = started ? CAPTIONS.findIndex(([a, b]) => T >= a && T < b) : -1;
    if (i !== capIdx) {
      capIdx = i;
      capEl.textContent = i >= 0 ? CAPTIONS[i][2] : "A 3 minute animated tour of the system. Press play.";
    }
    let ch = 0;
    CHAPTERS.forEach(([t], k) => { if (T >= t) ch = k; });
    chapBtns.forEach((b, k) => b.classList.toggle("is-active", started && k === ch));
  }

  function setT(t) {
    T = Math.max(0, Math.min(DUR, t));
    update();
  }

  function frame(now) {
    if (!playing) return;
    // Cap the step so a long pause (tab hidden) does not jump ahead, but slow frame rates still play in real time.
    const dt = Math.min(0.6, (now - last) / 1000);
    last = now;
    T += dt * speed;
    if (T >= DUR) {
      T = DUR;
      update();
      pause();
      playBtn.setAttribute("aria-label", "Replay");
      return;
    }
    update();
    requestAnimationFrame(frame);
  }

  function play() {
    if (!started) { started = true; T = 0; }
    if (T >= DUR) T = 0;
    bigPlay.hidden = true;
    playing = true;
    fig.classList.add("is-playing");
    playBtn.setAttribute("aria-label", "Pause");
    last = performance.now();
    requestAnimationFrame(frame);
  }

  function pause() {
    playing = false;
    fig.classList.remove("is-playing");
    playBtn.setAttribute("aria-label", "Play");
  }

  const toggle = () => (playing ? pause() : play());
  playBtn.addEventListener("click", toggle);
  bigPlay.addEventListener("click", play);
  svg.addEventListener("click", () => { if (started) toggle(); });
  seek.addEventListener("input", () => {
    if (!started) { started = true; bigPlay.hidden = true; }
    setT(Number(seek.value) / 10);
  });
  speedBtn.addEventListener("click", () => {
    speed = speed === 1 ? 1.5 : speed === 1.5 ? 0.75 : 1;
    speedBtn.textContent = `${speed}x`;
  });
  fsBtn.addEventListener("click", () => {
    if (document.fullscreenElement) document.exitFullscreen();
    else if (fig.requestFullscreen) fig.requestFullscreen();
  });
  fig.addEventListener("keydown", (e) => {
    if (e.target === seek) return;
    if (e.key === " " || e.key === "k") { e.preventDefault(); toggle(); }
    else if (e.key === "ArrowRight") { e.preventDefault(); setT(T + 5); }
    else if (e.key === "ArrowLeft") { e.preventDefault(); setT(T - 5); }
  });

  // Pause when scrolled out of view.
  if ("IntersectionObserver" in window) {
    new IntersectionObserver((entries) => {
      entries.forEach((en) => { if (!en.isIntersecting && playing) pause(); });
    }, { threshold: 0.2 }).observe(fig);
  }

  const ready = document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve();
  ready.then(update);
  update();

  // For screenshots and debugging: window.__explainer.seek(42)
  window.__explainer = { seek: (t) => { started = true; bigPlay.hidden = true; setT(t); }, duration: DUR, time: () => T };
};
