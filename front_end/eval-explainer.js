/* Scenes for the Evaluation explainer. Engine: explainer-engine.js.
 *
 * Numbers come from eval_results/model_comparison.json (run 20261118T062621Z),
 * summarised the same way as scripts/render_eval_charts.py.
 */
(() => {
  const svg = document.getElementById("exSvg");
  if (!svg || !window.Explainer) return;

  // [name, role, $ per 1k calls, median s, p90 s, tokens in, tokens out, judge, ok, calls]
  // Sorted by cost, cheapest first. Role: p = main, f1-f3 = backups.
  const MODELS = [
    ["llama-3.1-8b", "", 0.043, 21.40, 27.91, 915, 606, 3.09, 19, 23],
    ["mistral-small-24b-2501", "f2", 0.099, 9.52, 17.86, 1087, 562, 3.69, 24, 24],
    ["phi-4", "", 0.149, 6.78, 9.83, 924, 600, 3.42, 24, 24],
    ["gemini-2.5-flash-lite", "p", 0.313, 1.97, 2.75, 987, 535, 3.77, 24, 24],
    ["gpt-4o-mini", "f1", 0.398, 7.04, 9.68, 864, 448, 3.75, 24, 24],
    ["qwen-2.5-72b", "", 0.505, 9.88, 15.21, 878, 472, 3.79, 24, 24],
    ["nemotron-3-nano-30b-a3b", "", 0.513, 7.33, 10.60, 884, 1918, 4.18, 24, 24],
    ["command-r-08-2024", "", 0.526, 17.00, 37.21, 1049, 615, 3.27, 24, 24],
    ["deepseek-chat-v3.1", "", 0.650, 12.29, 23.83, 898, 448, 3.77, 24, 24],
    ["llama-3.1-70b", "f3", 0.995, 4.77, 9.21, 870, 512, 3.75, 24, 24],
    ["nemotron-3-super-120b-a12b", "", 1.036, 9.00, 20.93, 891, 2423, 4.40, 24, 24],
    ["qwen-2.5-coder-32b", "", 1.075, 12.16, 22.66, 912, 474, 3.77, 24, 24],
    ["llama-3.3-70b", "", 1.185, 7.99, 19.14, 951, 718, 3.31, 24, 24],
    ["qwen3.5-flash-02-23", "", 1.500, 33.07, 38.33, 872, 5549, 3.38, 2, 14],
    ["mixtral-8x22b", "", 5.273, 3.75, 6.38, 951, 562, 4.12, 24, 24],
    ["gpt-4o", "", 5.789, 2.42, 4.71, 838, 369, 3.88, 24, 24],
    ["command-r-plus-08-2024", "", 7.731, 39.92, 106.96, 995, 524, 3.39, 24, 24],
    ["gemini-2.5-pro", "", 25.100, 18.34, 29.68, 988, 2386, 4.34, 24, 24],
  ];

  window.Explainer(svg, ({ shiftAfter, C, K, el, group, txt, appear, hide, write, draw, pop, moveTo, travel, box, showBox, edge, showEdge, chip, checkIcon, crossIcon, lin, smooth, back }) => {
    const BAR = { p: C.blue, f: "#7fa9d6", o: "#c9ced6" };
    const barColor = (role) => (role === "p" ? BAR.p : role ? BAR.f : BAR.o);
    const IN = "#b7791f";
    const OUT = "#2e8b57";
    const JUDGE = "#c53030";

    // Plot frame shared by both charts
    const X0 = 150, X1 = 1130, YT = 150, YB = 520;
    const STEP = (X1 - X0) / MODELS.length;
    const cx = (i) => X0 + STEP * (i + 0.5);

    function axes(parent, t) {
      const ax = el("path", { d: `M${X0},${YT - 10} V${YB} H${X1} V${YT - 10}`, fill: "none", stroke: C.ink, "stroke-width": 1.6 }, parent);
      ax._len = ax.getTotalLength();
      draw(ax, t, 1.0);
    }

    function gridLine(parent, y, label, t, side = "left") {
      const g = el("g", {}, parent);
      el("line", { x1: X0, y1: y, x2: X1, y2: y, stroke: C.line, "stroke-width": 1 }, g);
      if (label) {
        txt(g, side === "left" ? X0 - 12 : X1 + 12, y + 5, label, { size: 14, font: "mono", fill: C.muted, anchor: side === "left" ? "end" : "start" });
      }
      appear(g, t, 0.4);
      return g;
    }

    function rightLabel(parent, y, label, t, color) {
      const n = txt(parent, X1 + 12, y + 5, label, { size: 14, font: "mono", fill: color || C.muted, anchor: "start" });
      appear(n, t, 0.4);
      return n;
    }

    function bars(parent, order, valueToY, t0, gap = 0.16) {
      return order.map((m, i) => {
        const x = cx(i);
        const h = Math.max(2, YB - valueToY(m));
        const g = group(parent, [x, YB]);
        el("rect", { x: -16, y: -h, width: 32, height: h, fill: barColor(m[1]) }, g);
        const t = t0 + i * gap;
        K(g, "sy", [t, 0], [t + 0.6, 1]);
        const lab = txt(parent, x + 4, YB + 18, m[0], { size: 12, font: "mono", fill: m[1] === "p" ? C.blue : C.soft, anchor: "end", weight: m[1] === "p" ? 600 : 500 });
        lab.setAttribute("transform", `rotate(-40 ${x + 4} ${YB + 18})`);
        appear(lab, t, 0.4);
        return g;
      });
    }

    function legend(parent, items, t) {
      let x = 80;
      items.forEach(([label, color, kind], i) => {
        const g = el("g", {}, parent);
        if (kind === "line") {
          el("line", { x1: x, y1: 112, x2: x + 26, y2: 112, stroke: color, "stroke-width": 3 }, g);
          el("circle", { cx: x + 13, cy: 112, r: 4.5, fill: color }, g);
        } else {
          el("rect", { x, y: 104, width: 18, height: 16, rx: 2, fill: color }, g);
        }
        const w = kind === "line" ? 34 : 26;
        txt(g, x + w, 118, label, { size: 15, anchor: "start", fill: C.soft });
        appear(g, t + i * 0.15, 0.4);
        x += w + label.length * 8 + 30;
      });
    }

    function valueTag(parent, x, y, label, t, t2, color = C.ink) {
      const g = group(parent, [x, y]);
      const w = label.length * 9 + 18;
      el("rect", { x: -w / 2, y: -15, width: w, height: 28, rx: 6, fill: C.paper, stroke: color, "stroke-width": 1.5 }, g);
      txt(g, 0, 5, label, { size: 15, font: "mono", fill: color, weight: 600 });
      pop(g, t);
      if (t2) hide(g, t2, 0.4);
      return g;
    }

    function dimOthers(groups, keepIdx, t, t2) {
      groups.forEach((g, i) => {
        if (keepIdx.includes(i)) return;
        K(g, "o", [t, 1], [t + 0.4, 0.3], [t2, 0.3], [t2 + 0.4, 1]);
      });
    }

    function polyline(parent, pts, color, t, d) {
      const p = el("path", { d: "M" + pts.map(([x, y]) => `${x.toFixed(1)},${y.toFixed(1)}`).join(" L"), fill: "none", stroke: color, "stroke-width": 2.6, "stroke-linejoin": "round" }, parent);
      p._len = p.getTotalLength();
      draw(p, t, d);
      pts.forEach(([x, y], i) => {
        const c = el("circle", { cx: x, cy: y, r: 4.5, fill: color, opacity: 0 }, parent);
        appear(c, t + (d * i) / pts.length, 0.2);
      });
      return p;
    }

    /* =========================================================
       Scene 0 - Title (0-6)
       ========================================================= */
    const gTitle = el("g", {});
    const t0a = txt(gTitle, 640, 318, "How we picked the AI model", { size: 58, font: "head", weight: 600 });
    const t0b = txt(gTitle, 640, 376, "18 models, the same tests, one choice", { size: 24, fill: C.soft });
    const t0line = el("path", { d: "M440,404 H840", stroke: C.blue, "stroke-width": 3, "stroke-linecap": "round" }, gTitle);
    t0line._len = 400;
    write(t0a, 0.3, 1.4);
    write(t0b, 1.4, 1.0);
    draw(t0line, 2.0, 0.8);
    hide(gTitle, 5.2, 0.7);

    /* =========================================================
       Scene 1 - The test (6-38.8)
       ========================================================= */
    const gSet = el("g", {});
    K(gSet, "o", [5.8, 0], [6.2, 1], [38.0, 1], [38.8, 0]);
    write(txt(gSet, 80, 92, "The test", { size: 36, font: "head", anchor: "start", weight: 600 }), 6.2, 0.6);

    // 18 models as dots, coloured by role
    MODELS.forEach((m, i) => {
      const c = group(gSet, [130 + (i % 6) * 28, 250 + Math.floor(i / 6) * 28]);
      el("circle", { cx: 0, cy: 0, r: 10, fill: barColor(m[1]) }, c);
      pop(c, 6.8 + i * 0.09);
    });
    write(txt(gSet, 200, 380, "18 models", { size: 20, weight: 600 }), 7.6, 0.5);

    const times = (x, t) => { const n = txt(gSet, x, 290, "×", { size: 48, font: "head", fill: C.muted }); appear(n, t, 0.4); };
    times(345, 9.4);
    ["only required fields", "every field filled", "a mix of fields", "tricky edge case"].forEach((s, i) => {
      const c = chip(gSet, { label: s, x: 500, y: 222 + i * 40, size: 14, w: 210, font: "body", fill: C.paper, stroke: C.line, color: C.ink });
      pop(c, 9.8 + i * 0.25);
    });
    write(txt(gSet, 500, 380, "4 job scenarios", { size: 20, weight: 600 }), 10.6, 0.5);
    times(650, 11.8);
    ["generate", "refine"].forEach((s, i) => {
      const c = chip(gSet, { label: s, x: 760, y: 262 + i * 42, size: 15, w: 120 });
      pop(c, 12.2 + i * 0.25);
    });
    write(txt(gSet, 760, 380, "2 tasks", { size: 20, weight: 600 }), 12.6, 0.4);
    times(870, 13.4);
    [0, 1, 2].forEach((i) => {
      const c = group(gSet, [940 + i * 34, 284]);
      el("circle", { cx: 0, cy: 0, r: 13, fill: C.paper, stroke: C.blue, "stroke-width": 2 }, c);
      txt(c, 0, 5, String(i + 1), { size: 14, font: "mono", fill: C.blue, weight: 600 });
      pop(c, 13.8 + i * 0.2);
    });
    write(txt(gSet, 974, 380, "3 runs", { size: 20, weight: 600 }), 14.2, 0.4);
    const eq = txt(gSet, 1060, 296, "=", { size: 48, font: "head", fill: C.muted });
    appear(eq, 15.0, 0.4);
    const calls = txt(gSet, 1160, 306, "0", { size: 64, font: "head", weight: 600, fill: C.blue });
    K(calls, "o", [15.2, 0], [15.4, 1]);
    K(calls, "num", [15.4, 0], [17.2, 421]);
    write(txt(gSet, 1160, 340, "calls", { size: 20, weight: 600 }), 16.4, 0.4);
    write(txt(gSet, 1160, 380, "run on 2026-11-18", { size: 14, font: "mono", fill: C.muted }), 16.8, 0.6);

    // What is measured on every call
    const meters = [
      ["Speed", "seconds per call"],
      ["Tokens", "in and out"],
      ["Cost", "OpenRouter list price"],
      ["Rule checks", "JSON, sections, facts"],
      ["Quality", "judged 1 to 5"],
    ];
    meters.forEach(([a, b], i) => {
      const x = 80 + i * 228;
      const g = el("g", {}, gSet);
      el("rect", { x, y: 480, width: 210, height: 96, rx: 10, fill: C.paper, stroke: i === 4 ? C.blue : C.line, "stroke-width": 1.6 }, g);
      txt(g, x + 18, 518, a, { size: 20, weight: 600, anchor: "start" });
      txt(g, x + 18, 548, b, { size: 14, font: "mono", fill: C.muted, anchor: "start" });
      appear(g, 22.4 + i * 0.5, 0.5);
    });
    const judgeNote = txt(gSet, 1100, 610, "judge: claude-haiku-4.5, not a candidate", { size: 14, font: "mono", fill: C.blue, anchor: "end" });
    appear(judgeNote, 32.2, 0.5);
    const fbNote = txt(gSet, 80, 640, "Fallbacks off: each model answered on its own.", { size: 16, fill: C.soft, anchor: "start", weight: 600 });
    appear(fbNote, 35.0, 0.5);

    /* =========================================================
       Scene 2 - Cost and tokens (39-92)
       ========================================================= */
    const gCost = el("g", {});
    K(gCost, "o", [38.6, 0], [39.0, 1], [91.4, 1], [92.2, 0]);
    write(txt(gCost, 80, 76, "Cost per 1,000 calls, and tokens used", { size: 30, font: "head", anchor: "start", weight: 600 }), 39.0, 1.0);
    legend(gCost, [["Main model", BAR.p], ["Backups", BAR.f], ["Others", BAR.o]], 39.8);

    const LO = Math.log10(0.02), HI = Math.log10(50);
    const yCost = (v) => YB - ((Math.log10(v) - LO) / (HI - LO)) * (YB - YT);
    axes(gCost, 39.6);
    [[0.1, "$0.10"], [1, "$1"], [10, "$10"]].forEach(([v, l], i) => gridLine(gCost, yCost(v), l, 40.6 + i * 0.2));

    // "Each line is 10x"
    const gLog = el("g", {}, gCost);
    const ya = yCost(1), yb = yCost(0.1);
    const brace = el("path", { d: `M${X0 + 40},${yb - 4} V${ya + 4} M${X0 + 32},${ya + 12} L${X0 + 40},${ya + 3} L${X0 + 48},${ya + 12}`, fill: "none", stroke: C.blue, "stroke-width": 2.4, "stroke-linecap": "round" }, gLog);
    brace._len = brace.getTotalLength();
    draw(brace, 42.0, 0.7);
    const x10 = txt(gLog, X0 + 58, (ya + yb) / 2 + 8, "× 10", { size: 26, font: "head", fill: C.blue, anchor: "start", weight: 600 });
    appear(x10, 42.5, 0.4);
    hide(gLog, 46.0, 0.4);

    const costBars = bars(gCost, MODELS, (m) => yCost(m[2]), 46.4);
    const iMain = 3, iCheap = 0, iPro = 17;
    dimOthers(costBars, [iMain, iCheap, iPro], 50.4, 66.6);
    valueTag(gCost, cx(iMain), yCost(MODELS[iMain][2]) - 26, "$0.31", 50.8, 66.6, C.blue);
    valueTag(gCost, cx(iCheap), yCost(MODELS[iCheap][2]) - 26, "$0.04", 56.2, 66.6, C.ink);
    const failNote = txt(gCost, X0 + 8, yCost(MODELS[iCheap][2]) - 92, "4/23 calls failed", { size: 14, font: "mono", fill: C.red, anchor: "start" });
    K(failNote, "o", [56.6, 0], [57.0, 1], [66.6, 1], [67.0, 0]);
    valueTag(gCost, cx(iPro) - 10, yCost(MODELS[iPro][2]) - 24, "$25.10", 61.2, 66.6, C.ink);
    const x80 = txt(gCost, cx(iPro) - 60, yCost(MODELS[iPro][2]) + 30, "80× the main model", { size: 15, font: "mono", fill: C.red, anchor: "end", weight: 600 });
    K(x80, "o", [62.4, 0], [62.8, 1], [66.6, 1], [67.0, 0]);

    // Tokens on a second axis
    const yTok = (v) => YB - (v / 6000) * (YB - YT);
    [0, 2000, 4000, 6000].forEach((v, i) => rightLabel(gCost, yTok(v), v === 0 ? "0" : `${v / 1000}k`, 67.4 + i * 0.1));
    const tokTitle = txt(gCost, X1 + 12, YT - 22, "tokens", { size: 14, font: "mono", fill: C.muted, anchor: "start" });
    appear(tokTitle, 67.4, 0.4);
    const gLeg2 = el("g", {}, gCost);
    appear(gLeg2, 67.6, 0.4);
    [["Input tokens", IN, 640], ["Output tokens", OUT, 820]].forEach(([l, c, x]) => {
      el("line", { x1: x, y1: 112, x2: x + 26, y2: 112, stroke: c, "stroke-width": 3 }, gLeg2);
      el("circle", { cx: x + 13, cy: 112, r: 4.5, fill: c }, gLeg2);
      txt(gLeg2, x + 34, 118, l, { size: 15, anchor: "start", fill: C.soft });
    });
    polyline(gCost, MODELS.map((m, i) => [cx(i), yTok(m[5])]), IN, 68.4, 2.0);
    const inNote = txt(gCost, X0 + 12, YT + 16, "input: ~900 tokens, same prompt for every model", { size: 14, font: "mono", fill: IN, anchor: "start" });
    K(inNote, "o", [70.4, 0], [70.8, 1], [91, 1]);
    polyline(gCost, MODELS.map((m, i) => [cx(i), yTok(m[6])]), OUT, 73.6, 2.0);
    const spikes = [[13, "5,549"], [10, "2,423"], [17, "2,386"]];
    spikes.forEach(([i, l], k) => {
      const t = 76.0 + k * 0.6;
      valueTag(gCost, cx(i) + (k === 0 ? -48 : 0), yTok(MODELS[i][6]) - (k === 0 ? -4 : 24), l, t, 0, OUT);
    });
    const qwenFail = txt(gCost, cx(13) - 92, yTok(MODELS[13][6]) + 34, "12 of 14 calls failed", { size: 14, font: "mono", fill: C.red, anchor: "start" });
    K(qwenFail, "o", [86.4, 0], [86.8, 1]);

    /* =========================================================
       Scene 3 - Speed and quality (92-137)
       ========================================================= */
    const gLat = el("g", {});
    K(gLat, "o", [91.8, 0], [92.2, 1], [136.2, 1], [137.0, 0]);
    write(txt(gLat, 80, 76, "Seconds per call, and quality", { size: 30, font: "head", anchor: "start", weight: 600 }), 92.2, 1.0);
    legend(gLat, [["Main model", BAR.p], ["Backups", BAR.f], ["Others", BAR.o]], 92.8);

    const ySec = (v) => YB - (v / 110) * (YB - YT);
    axes(gLat, 92.6);
    [0, 20, 40, 60, 80, 100].forEach((v, i) => gridLine(gLat, ySec(v), `${v}s`, 93.4 + i * 0.08));
    const byLat = MODELS.slice().sort((a, b) => a[3] - b[3]);
    const latBars = bars(gLat, byLat, (m) => ySec(m[3]), 94.0, 0.14);
    const li = (name) => byLat.findIndex((m) => m[0] === name);
    const lMain = li("gemini-2.5-flash-lite"), lPlus = li("command-r-plus-08-2024");
    const lNemo = li("nemotron-3-super-120b-a12b"), lPro = li("gemini-2.5-pro");

    valueTag(gLat, cx(lMain) + 14, ySec(byLat[lMain][3]) - 30, "2.0 s", 97.4, 0, C.blue);

    // p90 whiskers
    byLat.forEach((m, i) => {
      const x = cx(i);
      const w = el("path", { d: `M${x},${ySec(m[3])} V${ySec(m[4])} M${x - 6},${ySec(m[4])} H${x + 6}`, fill: "none", stroke: C.soft, "stroke-width": 1.6 }, gLat);
      w._len = w.getTotalLength();
      draw(w, 102.2 + i * 0.08, 0.5);
    });
    valueTag(gLat, cx(lMain) + 70, ySec(byLat[lMain][4]) - 64, "p90 2.7 s", 103.6, 106.8, C.blue);
    dimOthers(latBars, [lMain, lPlus], 107.0, 111.8);
    valueTag(gLat, cx(lPlus) - 90, ySec(byLat[lPlus][3]) - 8, "40 s median", 107.4, 111.8, C.ink);
    valueTag(gLat, cx(lPlus) - 90, ySec(byLat[lPlus][4]) + 10, "p90 107 s", 108.2, 111.8, C.red);

    // Judge score on a right axis
    const yJ = (v) => YB - ((v - 1) / 4) * (YB - YT);
    [1, 2, 3, 4, 5].forEach((v, i) => rightLabel(gLat, yJ(v), String(v), 112.2 + i * 0.08, JUDGE));
    const jTitle = txt(gLat, X1 + 12, YT - 22, "judge", { size: 14, font: "mono", fill: JUDGE, anchor: "start" });
    appear(jTitle, 112.2, 0.4);
    const gLeg3 = el("g", {}, gLat);
    appear(gLeg3, 112.4, 0.4);
    el("line", { x1: 640, y1: 112, x2: 666, y2: 112, stroke: JUDGE, "stroke-width": 3 }, gLeg3);
    el("circle", { cx: 653, cy: 112, r: 4.5, fill: JUDGE }, gLeg3);
    txt(gLeg3, 674, 118, "Judge score (1-5)", { size: 15, anchor: "start", fill: C.soft });
    polyline(gLat, byLat.map((m, i) => [cx(i), yJ(m[7])]), JUDGE, 112.6, 2.4);
    valueTag(gLat, cx(lNemo), yJ(byLat[lNemo][7]) - 28, "4.40", 118.4, 0, JUDGE);
    valueTag(gLat, cx(lPro), yJ(byLat[lPro][7]) - 28, "4.34", 118.8, 0, JUDGE);
    valueTag(gLat, cx(lMain) + 24, yJ(byLat[lMain][7]) - 28, "3.77", 119.6, 0, C.blue);
    dimOthers(latBars, [lMain, lNemo, lPro], 124.0, 136.2);
    const slow1 = txt(gLat, cx(lNemo), ySec(byLat[lNemo][4]) - 14, "4.6× slower", { size: 14, font: "mono", fill: C.ink, weight: 600 });
    const slow2 = txt(gLat, cx(lPro), ySec(byLat[lPro][4]) - 14, "9.3× slower", { size: 14, font: "mono", fill: C.ink, weight: 600 });
    appear(slow1, 125.0, 0.4);
    appear(slow2, 125.6, 0.4);

    /* =========================================================
       Scene 4 - The shortlist (137-165)
       ========================================================= */
    const gTab = el("g", {});
    K(gTab, "o", [136.8, 0], [137.2, 1], [164.4, 1], [165.2, 0]);
    write(txt(gTab, 80, 76, "The shortlist", { size: 30, font: "head", anchor: "start", weight: 600 }), 137.2, 0.7);
    const COLS = [
      ["Model", 80, "start"], ["Role", 440, "start"], ["Median / p90", 640, "middle"], ["$ per 1k", 790, "middle"],
      ["Term checks", 920, "middle"], ["All sections", 1050, "middle"], ["Judge", 1170, "middle"],
    ];
    const ROWS = [
      ["gemini-2.5-flash-lite", "main", "2.0 / 2.7 s", "0.31", "22/24", "19/24", "3.77"],
      ["gpt-4o-mini", "backup 1", "7.0 / 9.7 s", "0.40", "20/24", "16/24", "3.75"],
      ["mistral-small-24b", "backup 2", "9.5 / 17.9 s", "0.10", "21/24", "9/24", "3.69"],
      ["llama-3.1-70b", "backup 3", "4.8 / 9.2 s", "1.00", "18/24", "9/24", "3.75"],
      ["gpt-4o", "-", "2.4 / 4.7 s", "5.79", "22/24", "6/24", "3.88"],
      ["nemotron-3-super-120b", "-", "9.0 / 20.9 s", "1.04", "22/24", "7/24", "4.40"],
      ["gemini-2.5-pro", "-", "18.3 / 29.7 s", "25.10", "18/24", "7/24", "4.34"],
    ];
    const RY = (r) => 182 + r * 58;
    const head = el("g", {}, gTab);
    COLS.forEach(([h, x, a]) => txt(head, x, 140, h, { size: 15, font: "mono", fill: C.muted, anchor: a, weight: 600 }));
    el("line", { x1: 70, y1: 154, x2: 1220, y2: 154, stroke: C.ink, "stroke-width": 1.5 }, head);
    appear(head, 137.6, 0.5);
    const cellHl = (r, c, color, t, t2) => {
      const [, x, a] = COLS[c];
      const w = c === 0 ? 300 : 120;
      const rx = a === "start" ? x - 10 : x - w / 2;
      const hl = el("rect", { x: rx, y: RY(r) - 24, width: w, height: 40, rx: 6, fill: color, opacity: 0 }, gTab);
      K(hl, "o", [t, 0], [t + 0.4, 1], [t2, 1], [t2 + 0.4, 0]);
    };
    // highlights first so they sit behind the text
    cellHl(0, 2, C.greenSoft, 142.2, 163.8);
    cellHl(2, 3, C.greenSoft, 147.2, 163.8);
    cellHl(0, 3, C.tint, 148.0, 163.8);
    cellHl(0, 5, C.greenSoft, 152.2, 163.8);
    cellHl(5, 6, C.amberSoft, 158.2, 163.8);
    cellHl(6, 6, C.amberSoft, 158.4, 163.8);
    cellHl(0, 6, C.tint, 159.0, 163.8);
    ROWS.forEach((row, r) => {
      const g = el("g", {}, gTab);
      if (r % 2 === 0) el("rect", { x: 70, y: RY(r) - 29, width: 1150, height: 58, fill: C.paper, opacity: 0.7 }, g);
      row.forEach((v, c) => {
        const [, x, a] = COLS[c];
        txt(g, x, RY(r) + 5, v, { size: c === 0 ? 17 : 17, font: c === 0 || c > 1 ? "mono" : "body", anchor: a, fill: r === 0 && c === 0 ? C.blue : C.ink, weight: r === 0 && c === 0 ? 600 : 500 });
      });
      el("line", { x1: 70, y1: RY(r) + 29, x2: 1220, y2: RY(r) + 29, stroke: C.line }, g);
      appear(g, 138.2 + r * 0.35, 0.4);
    });
    const tabNote = txt(gTab, 80, 620, '"All sections" = drafts with every core section filled.', { size: 15, fill: C.muted, anchor: "start" });
    appear(tabNote, 152.6, 0.5);

    /* =========================================================
       Scene 5 - The decision (165-202)
       ========================================================= */
    const gDec = el("g", {});
    K(gDec, "o", [164.8, 0], [165.2, 1]);
    write(txt(gDec, 80, 76, "The trade-off", { size: 30, font: "head", anchor: "start", weight: 600 }), 165.2, 0.7);
    const TRIO = [
      ["flash-lite", BAR.p, 3.77, 1.97, 0.313],
      ["nemotron", BAR.o, 4.40, 9.00, 1.036],
      ["2.5-pro", BAR.o, 4.34, 18.34, 25.10],
    ];
    const PANELS = [
      ["Quality", "judge score, 1 to 5", (v) => (v - 1) / 4, 2, (v) => v.toFixed(2), 171.0],
      ["Speed", "median seconds, lower is better", (v) => v / 20, 3, (v) => `${v.toFixed(1)} s`, 177.0],
      ["Cost", "$ per 1,000 calls, lower is better", (v) => v / 26, 4, (v) => `$${v.toFixed(2)}`, 183.0],
    ];
    const PB = 470, PT = 190;
    const gPanels = el("g", {}, gDec);
    K(gPanels, "o", [189.4, 1], [190.0, 0.3]);
    PANELS.forEach(([title, sub, scale, idx, fmtv, t], p) => {
      const px = 90 + p * 380;
      const g = el("g", {}, gPanels);
      txt(g, px, 150, title, { size: 22, weight: 600, anchor: "start" });
      txt(g, px, 174, sub, { size: 13, font: "mono", fill: C.muted, anchor: "start" });
      el("line", { x1: px, y1: PB, x2: px + 320, y2: PB, stroke: C.ink, "stroke-width": 1.5 }, g);
      appear(g, 165.6 + p * 0.3, 0.5);
      TRIO.forEach((m, k) => {
        const v = m[idx];
        const h = Math.max(3, scale(v) * (PB - PT));
        const bx = px + 30 + k * 100;
        const bg = group(g, [bx + 30, PB]);
        el("rect", { x: -30, y: -h, width: 60, height: h, fill: m[1] }, bg);
        K(bg, "sy", [t, 0], [t + 0.8, 1]);
        const val = txt(g, bx + 30, PB - h - 10, fmtv(v), { size: 16, font: "mono", weight: 600, fill: k === 0 ? C.blue : C.ink });
        appear(val, t + 0.7, 0.3);
        const nm = txt(g, bx + 30, PB + 24, m[0], { size: 13, font: "mono", fill: k === 0 ? C.blue : C.soft });
        appear(nm, 166.4, 0.4);
      });
    });

    // The chosen chain
    const CHAIN = [["gemini-2.5-flash-lite", "main"], ["gpt-4o-mini", "backup 1"], ["mistral-small-24b", "backup 2"], ["llama-3.1-70b", "backup 3"]];
    CHAIN.forEach(([name, role], i) => {
      const x = 170 + i * 310;
      const c = chip(gDec, { label: name, x, y: 590, size: 15, w: 250, fill: i === 0 ? C.blue : C.paper, stroke: C.blue, color: i === 0 ? C.paper : C.deep });
      pop(c, 190.2 + i * 0.6);
      const r = txt(gDec, x, 632, role, { size: 14, font: "mono", fill: C.muted });
      appear(r, 190.5 + i * 0.6, 0.4);
      if (i > 0) {
        const a = edge(gDec, `M${x - 180},590 H${x - 130}`, { color: C.muted });
        showEdge(a, 190.0 + i * 0.6, 0.4);
      }
    });
    const chosenCk = checkIcon(gDec, 170, 548, 1.1, C.green);
    draw(chosenCk, 191.0, 0.5);


    /* =========================================================
       Scene 1b - How each call is scored (38.8-94.8)
       Inserted after the test setup; everything later is pushed back by D.
       Checks mirror src/evaluation/metrics.py and scenarios.py.
       ========================================================= */
    const S = 38.8, D = 56;
    shiftAfter(38.5, D);
    K(gSet, "o", [38.8, 0]); // keep the setup scene's fade-out where it was

    const gScore = el("g", {});
    K(gScore, "o", [S - 0.2, 0], [S + 0.2, 1], [S + D - 0.8, 1], [S + D, 0]);
    write(txt(gScore, 80, 76, "How each call is scored", { size: 30, font: "head", anchor: "start", weight: 600 }), S + 0.2, 0.8);

    // The scenario (input)
    const gScen = el("g", {}, gScore);
    appear(gScen, S + 0.8, 0.6);
    el("rect", { x: 80, y: 120, width: 330, height: 220, rx: 12, fill: C.paper, stroke: C.line, "stroke-width": 1.6 }, gScen);
    txt(gScen, 100, 152, "Scenario 4: tricky edge case", { size: 17, weight: 600, anchor: "start" });
    txt(gScen, 100, 182, "role: DevOps Engineer", { size: 14, font: "mono", fill: C.soft, anchor: "start" });
    txt(gScen, 100, 218, "must include", { size: 14, font: "mono", fill: C.green, anchor: "start", weight: 600 });
    txt(gScen, 100, 240, "HIPAA, Kubernetes, Terraform", { size: 14, font: "mono", fill: C.soft, anchor: "start" });
    txt(gScen, 100, 276, "must leave out", { size: 14, font: "mono", fill: C.red, anchor: "start", weight: 600 });
    txt(gScen, 100, 298, "health insurance, PTO, vacation", { size: 14, font: "mono", fill: C.soft, anchor: "start" });
    txt(gScen, 100, 322, "no pay given", { size: 14, font: "mono", fill: C.soft, anchor: "start" });

    // The model under test, with a stopwatch
    const aIn = edge(gScore, "M412,230 H491", { color: C.muted });
    showEdge(aIn, S + 5.6, 0.5);
    const mBox = box(gScore, { x: 610, y: 230, w: 236, h: 100, label: "Model under test", sub: "same prompt as the site", size: 19 });
    showBox(mBox, S + 6.0);
    const watch = txt(gScore, 610, 316, "0.0 s", { size: 22, font: "mono", fill: C.blue, weight: 600 });
    watch._dec = 1;
    watch._suf = " s";
    K(watch, "o", [S + 6.8, 0], [S + 7.0, 1]);
    K(watch, "num", [S + 7.0, 0, lin], [S + 9.0, 2.0, lin]);

    // The draft it returns
    const aOut = edge(gScore, "M729,230 H808", { color: C.muted });
    showEdge(aOut, S + 10.6, 0.5);
    const gDraft = el("g", {}, gScore);
    appear(gDraft, S + 11.0, 0.5);
    el("rect", { x: 812, y: 150, width: 200, height: 160, rx: 10, fill: C.paper, stroke: C.blue, "stroke-width": 1.8 }, gDraft);
    txt(gDraft, 830, 178, "{ draft JSON }", { size: 14, font: "mono", fill: C.deep, anchor: "start", weight: 600 });
    [150, 120, 160, 100, 140].forEach((w, i) => el("rect", { x: 830, y: 196 + i * 20, width: w, height: 7, rx: 3.5, fill: C.soft, opacity: 0.35 }, gDraft));
    const tokIn = txt(gScore, 1040, 205, "tokens in: 870", { size: 14, font: "mono", fill: C.muted, anchor: "start" });
    const tokOut = txt(gScore, 1040, 230, "tokens out: 512", { size: 14, font: "mono", fill: C.muted, anchor: "start" });
    appear(tokIn, S + 11.6, 0.4);
    appear(tokOut, S + 11.9, 0.4);

    // Five checks
    const CARD_Y = 380, CARD_H = 190, CARD_W = 214;
    const cardX = (i) => 80 + i * 232;
    function card(i, title, t) {
      const g = el("g", {}, gScore);
      const r = el("rect", { x: cardX(i), y: CARD_Y, width: CARD_W, height: CARD_H, rx: 12, fill: C.paper, stroke: C.line, "stroke-width": 1.6 }, g);
      txt(g, cardX(i) + 16, CARD_Y + 30, `${i + 1}`, { size: 14, font: "mono", fill: C.blue, anchor: "start", weight: 600 });
      txt(g, cardX(i) + 38, CARD_Y + 30, title, { size: 17, weight: 600, anchor: "start" });
      appear(g, t, 0.5);
      K(r, "stroke", [t + 3.0, C.line], [t + 3.4, C.green]);
      const ck = checkIcon(g, cardX(i) + CARD_W - 26, CARD_Y + 26, 0.9);
      draw(ck, t + 3.0, 0.4);
      return g;
    }
    const line = (g, x, y, str, o = {}) => txt(g, x, y, str, Object.assign({ size: 14, font: "mono", fill: C.soft, anchor: "start" }, o));

    // 1. Valid JSON
    const c1 = card(0, "Valid JSON", S + 14.0);
    line(c1, cardX(0) + 16, CARD_Y + 70, "parses as JSON");
    line(c1, cardX(0) + 16, CARD_Y + 94, "matches the schema");
    line(c1, cardX(0) + 16, CARD_Y + 140, "fail = call failed:", { fill: C.red });
    line(c1, cardX(0) + 16, CARD_Y + 162, "no time, cost, score", { fill: C.red });

    // 2. Core sections
    const c2 = card(1, "Core sections", S + 20.0);
    ["title", "about company", "about role", "responsibilities", "requirements"].forEach((f, k) => {
      const n = line(c2, cardX(1) + 16, CARD_Y + 64 + k * 24, f);
      appear(n, S + 20.6 + k * 0.3, 0.3);
    });

    // 3. Terms
    const c3 = card(2, "Term check", S + 26.0);
    ["HIPAA", "Kubernetes", "Terraform"].forEach((w, k) => {
      const ch = chip(c3, { label: w, x: cardX(2) + 76, y: CARD_Y + 66 + k * 34, size: 13, w: 120, fill: C.greenSoft, stroke: C.green, color: C.green });
      pop(ch, S + 26.6 + k * 0.4);
    });
    const absent = line(c3, cardX(2) + 16, CARD_Y + 176, "PTO, vacation: absent", { fill: C.green });
    appear(absent, S + 28.2, 0.4);

    // 4. No invented pay
    const c4 = card(3, "No invented pay", S + 32.0);
    line(c4, cardX(3) + 16, CARD_Y + 70, "input had no pay, so");
    line(c4, cardX(3) + 16, CARD_Y + 94, "no $, £, € or 90k");
    line(c4, cardX(3) + 16, CARD_Y + 118, "may appear");
    const allPass = line(c4, cardX(3) + 16, CARD_Y + 162, "all 18 models passed", { fill: C.green });
    appear(allPass, S + 35.4, 0.4);

    // 5. Judge
    const c5 = card(4, "Judge score", S + 37.0);
    const crit = [["specific", 4], ["tone", 5], ["faithful", 5], ["LinkedIn-ready", 4]];
    crit.forEach(([n, v], k) => {
      const y = CARD_Y + 64 + k * 24;
      const a = line(c5, cardX(4) + 16, y, n);
      const b = line(c5, cardX(4) + CARD_W - 20, y, String(v), { anchor: "end", fill: C.ink, weight: 600 });
      appear(a, S + 38.0 + k * 0.4, 0.3);
      appear(b, S + 38.2 + k * 0.4, 0.3);
    });
    const avgLine = el("line", { x1: cardX(4) + 16, y1: CARD_Y + 152, x2: cardX(4) + CARD_W - 16, y2: CARD_Y + 152, stroke: C.line }, c5);
    appear(avgLine, S + 44.2, 0.3);
    const avgLbl = line(c5, cardX(4) + 16, CARD_Y + 176, "average", { fill: C.blue, weight: 600 });
    const avg = line(c5, cardX(4) + CARD_W - 20, CARD_Y + 176, "4.50", { anchor: "end", fill: C.blue, weight: 600, size: 16 });
    appear(avgLbl, S + 44.4, 0.3);
    appear(avg, S + 44.8, 0.3);
    const judgeChip = chip(gScore, { label: "judge: claude-haiku-4.5, temperature 0", x: 1060, y: 330, size: 13, w: 330, fill: C.paper, stroke: C.blue, color: C.deep });
    pop(judgeChip, S + 37.4);

    // Cost
    const cost = txt(gScore, 80, 630, "cost = tokens in × input price + tokens out × output price", { size: 18, font: "mono", fill: C.ink, anchor: "start", weight: 600 });
    write(cost, S + 48.2, 1.6);
    const costSub = txt(gScore, 80, 660, "OpenRouter list prices, saved on 2026-11-17. Unknown prices are never guessed.", { size: 15, fill: C.muted, anchor: "start" });
    appear(costSub, S + 49.6, 0.5);
    const example = txt(gScore, 80, 690, "The numbers in this example are for illustration.", { size: 13, font: "mono", fill: C.muted, anchor: "start" });
    appear(example, S + 50.4, 0.5);

    const CAPTIONS = [
      [0, 6, "Before choosing an AI model, we tested 18 of them on the exact prompts this site uses."],
      [6, 9.4, "Eighteen models, colored here by the job they have now: blue is the main model, light blue the backups."],
      [9.4, 13.4, "Each one wrote job descriptions for 4 fixed hiring scenarios, and did both tasks: generate a draft, then refine it."],
      [13.4, 17.6, "Every combination ran 3 times."],
      [17.6, 22.2, "18 x 4 x 2 x 3 would be 432 calls. When a draft failed, its refine step was skipped, so 421 calls ran."],
      [22.2, 27.4, "Every call was measured: seconds taken, tokens in and out, and cost at OpenRouter's list price on 2026-11-17."],
      [27.4, 32.2, "Plain rule checks asked: is it valid JSON, is every core section there, does it include the facts it was given?"],
      [32.2, 35, "Quality was scored 1 to 5 by claude-haiku-4.5, a model that was not in the race, at temperature 0."],
      [35, 38.8, "Fallbacks were switched off, so every model had to answer on its own."],
      [39, 42, "First chart: what one model costs for 1,000 calls."],
      [42, 46.4, "The cost axis is a log scale. Each grid line is 10 times the one below it."],
      [46.4, 50.6, "Models are sorted from cheapest to most expensive."],
      [50.6, 56.2, "The main model, gemini-2.5-flash-lite, costs about $0.31 per 1,000 calls."],
      [56.2, 61, "The cheapest, llama-3.1-8b, costs $0.04, but 4 of its 23 calls failed."],
      [61, 67.2, "gemini-2.5-pro costs about $25 per 1,000 calls: 80 times the main model."],
      [67.2, 73.4, "Now tokens, on the right axis. Input, in amber, is flat at about 900: every model got the same prompt."],
      [73.4, 79.6, "Output, in green, is not. Some models write thousands of extra tokens, much of it thinking before they answer."],
      [79.6, 86.2, "qwen3.5-flash averaged about 5,500 output tokens. nemotron-3-super and gemini-2.5-pro used about 2,400. You pay for every one."],
      [86.2, 92, "qwen3.5-flash also failed 12 of its 14 calls."],
      [92, 97.2, "Second chart: the same 18 models, sorted by speed. Each bar is the median time for one call."],
      [97.2, 102, "gemini-2.5-flash-lite is the fastest of all 18: 2.0 seconds at the median."],
      [102, 107, "The thin lines show p90: 9 out of 10 calls finished below that point. For the main model, that is 2.7 seconds."],
      [107, 112.2, "At the slow end, command-r-plus takes 40 seconds at the median, and its slowest calls took over 100."],
      [112.2, 118.2, "The red line is quality: the judge's score from 1 to 5. Most models land between 3.1 and 4.4."],
      [118.2, 124, "The top scores: nemotron-3-super at 4.40 and gemini-2.5-pro at 4.34. The main model scores 3.77."],
      [124, 130.4, "But those two are 4.6 and 9.3 times slower at the median."],
      [130.4, 137, "This is a small test, so gaps under about 0.3 should be read as ties."],
      [137, 142.2, "The shortlist: the four models we use, next to the three strongest alternatives."],
      [142.2, 147.2, "Speed: the main model is the fastest here, at 2.0 seconds, with a p90 of 2.7."],
      [147.2, 152.2, "Cost: only mistral-small is cheaper. The main model is next, at $0.31."],
      [152.2, 158.2, "Completeness: the main model filled every core section in 19 of 24 drafts, the most on this list."],
      [158.2, 165, "Quality is where it gives ground: 3.77, against 4.40 and 4.34."],
      [165, 171, "Here is the trade-off in one picture: the main model next to the two best-scoring models."],
      [171, 177, "Quality on the full 1 to 5 scale: a gap of about 0.6."],
      [177, 183, "Speed: 2.0 seconds against 9.0 and 18.3."],
      [183, 189.6, "Cost: $0.31 against $1.04 and $25.10 per 1,000 calls."],
      [189.6, 196, "People wait for the draft while they work, so we chose speed and reliability. If the main model fails, three backups take over in order."],
      [196, 999, "Every model and every number is in the table below."],
    ];
    const CHAPTERS = [
      [0, "Intro"],
      [6, "The test"],
      [39, "Cost and tokens"],
      [92, "Speed and quality"],
      [137, "The shortlist"],
      [165, "The decision"],
    ];
    // Push captions and chapters after the inserted scene back by D, then add the scene's own.
    const later = (t) => (t >= 38.8 ? t + D : t);
    const caps = CAPTIONS.map(([a, b, text]) => [later(a), a >= 38.8 ? later(b) : b, text]);
    const SCORE_CAPS = [
      [S, S + 5.6, "So how is one call scored? Follow this one from start to finish. Each scenario lists facts the draft must include, and facts it must leave out."],
      [S + 5.6, S + 10.6, "The model gets the same prompt this site uses, and a stopwatch times the whole call."],
      [S + 10.6, S + 14, "It sends back a draft as JSON. The token counts for the call are saved too."],
      [S + 14, S + 20, "Check 1: is it valid JSON in the right structure? If not, the call counts as failed and gets no time, cost or score."],
      [S + 20, S + 26, "Check 2: are all the core sections filled? This is the \"all core sections\" number in the table."],
      [S + 26, S + 32, "Check 3: every must-include term is there, and no must-leave-out term is. This is the \"term checks\" number."],
      [S + 32, S + 37, "Check 4: the input had no pay, so the draft must not show a pay figure. Every model passed this one."],
      [S + 37, S + 44.2, "Check 5: a judge model, claude-haiku-4.5, reads the facts and the draft, and scores 4 things from 1 to 5. Refine calls also get a score for how well the change was made."],
      [S + 44.2, S + 48.2, "The quality score is the average of those, worked out in code, not by the judge."],
      [S + 48.2, S + 52.4, "Cost is the real token count times OpenRouter's list price, saved on 2026-11-17."],
      [S + 52.4, S + D, "Every model goes through this for each scenario, task and run. Those results are the charts that follow."],
    ];
    const idx = caps.findIndex(([a]) => a >= S + D);
    caps.splice(idx, 0, ...SCORE_CAPS);
    const chaps = CHAPTERS.map(([t, n]) => [later(t), n]);
    chaps.splice(2, 0, [S, "How scoring works"]);
    return { CAPTIONS: caps, CHAPTERS: chaps, DUR: 202 + D, POSTER: 3.2 };
  });
})();
