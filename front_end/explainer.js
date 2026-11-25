/* Scenes for the How it works explainer. Engine: explainer-engine.js.
 *
 * Facts shown here mirror the code: src/api/services.py (upload limits, models),
 * src/llm/models.py (fallbacks), src/agent/prompts.py (sanitizing, 12,000 chars),
 * docs/migrations/001_credit_ledger.sql (spend/refund/grant, stripe_events).
 */
(() => {
  const svg = document.getElementById("exSvg");
  if (!svg || !window.Explainer) return;
  window.Explainer(svg, ({ C, K, el, group, txt, appear, hide, write, draw, pop, moveTo, travel, box, showBox, cylinder, showCylinder, edge, showEdge, chip, checkIcon, crossIcon, lockIcon, lin, smooth, back, svg }) => {
  /* =========================================================
     Scene 0 - Title (0-6)
     ========================================================= */
  const gTitle = el("g", {});
  const t0a = txt(gTitle, 640, 318, "How the generator works", { size: 58, font: "head", weight: 600 });
  const t0b = txt(gTitle, 640, 376, "The AI pipeline, file upload, and the credit ledger", { size: 24, fill: C.soft });
  const t0line = el("path", { d: "M440,404 H840", stroke: C.blue, "stroke-width": 3, "stroke-linecap": "round" }, gTitle);
  t0line._len = 400;
  write(t0a, 0.3, 1.4);
  write(t0b, 1.4, 1.2);
  draw(t0line, 2.0, 0.8);
  hide(gTitle, 5.2, 0.7);

  /* =========================================================
     Scene 1 + 2 - The map, then one draft through it (6-81)
     ========================================================= */
  const gMap = el("g", {});
  K(gMap, "o", [6, 0], [6.3, 1], [80, 1], [80.8, 0], [188, 0], [188.6, 1]);

  const gDim = el("g", {}, gMap);
  K(gDim, "o", [34.3, 1], [35, 0.25], [188, 0.25], [188.6, 1]);

  const browser = box(gMap, { x: 180, y: 400, w: 200, h: 84, label: "Browser", sub: "your answers" });
  const api = box(gMap, { x: 620, y: 400, w: 250, h: 96, label: "FastAPI", sub: "on Google Cloud Run" });
  const router = box(gMap, { x: 1060, y: 400, w: 230, h: 96, label: "OpenRouter", sub: "main + backup models" });
  const checks = box(gMap, { x: 840, y: 165, w: 270, h: 90, label: "Checks", sub: "schema + quality rules" });
  const supa = cylinder(gDim, { x: 1060, y: 610, w: 190, h: 70, label: "Supabase", sub: "sign-in, credits" });
  const stripe = box(gDim, { x: 180, y: 615, w: 200, h: 80, label: "Stripe", sub: "payments", stroke: C.amber });

  const e1 = edge(gMap, "M280,400 H493", { label: "answers + bot token", lx: 388, ly: 374 });
  const e2 = edge(gMap, "M745,400 H941", { label: "prompt", lx: 843, ly: 374 });
  const e3 = edge(gMap, "M1060,352 C1060,260 1040,165 977,165", { label: "JSON draft", lx: 1078, ly: 262 });
  const e4 = edge(gMap, "M705,165 C420,165 180,200 180,356", { label: "checked draft", lx: 400, ly: 178 });
  const e5 = edge(gDim, "M745,430 C860,430 880,600 963,605", { label: "sign-in, credit ledger", lx: 842, ly: 548, color: C.deep });
  const e6 = edge(gDim, "M180,442 V573", { label: "checkout", lx: 180, ly: 508, color: C.amber });
  const e7 = edge(gDim, "M280,615 C420,615 560,560 600,451", { label: "signed webhook", lx: 410, ly: 604, color: C.amber });

  showBox(browser, 6.4);
  showEdge(e1, 8.6);
  showBox(api, 9.3);
  showEdge(e2, 13.6);
  showBox(router, 14.3);
  showEdge(e3, 18.6);
  showBox(checks, 19.3);
  showEdge(e4, 23.6, 0.9);
  showEdge(e5, 26.8);
  showCylinder(supa, 27.4);
  showEdge(e6, 30.4, 0.5);
  showBox(stripe, 30.8);
  showEdge(e7, 31.6);

  // --- One draft: answers leave the browser
  const pAnswers = chip(gMap, { label: "answers", x: 180, y: 400 });
  const shield = group(pAnswers, [52, -18]);
  el("circle", { cx: 0, cy: 0, r: 12, fill: C.green }, shield);
  el("path", { d: "M-5,0 L-1.5,4 L5.5,-4", fill: "none", stroke: C.paper, "stroke-width": 2.6, "stroke-linecap": "round", "stroke-linejoin": "round" }, shield);
  pop(pAnswers, 35.6);
  pop(shield, 37.0);
  travel(pAnswers, e1.p, 38.2, 39.8);
  moveTo(pAnswers, 39.8, 0.5, 620, 318);

  // Gates at the server
  const gates = [];
  ["bot check", "per-IP limit", "daily cap"].forEach((label, i) => {
    const gx = 480 + i * 140;
    const g = group(gMap, [gx, 262]);
    el("rect", { x: -64, y: -16, width: 128, height: 32, rx: 16, fill: C.paper, stroke: C.line, "stroke-width": 1.5 }, g);
    txt(g, -12, 5, label, { size: 13, font: "mono", fill: C.soft });
    const ck = checkIcon(g, 46, 0, 0.75);
    appear(g, 40.4 + i * 0.25, 0.3);
    draw(ck, 41.2 + i * 0.8, 0.35);
    hide(g, 44.6, 0.4);
    gates.push(g);
  });

  // Pay range is held back by code
  const pPay = chip(gMap, { label: "$80k - $100k", x: 620, y: 318, fill: C.amberSoft, stroke: C.amber, color: C.amber });
  K(pPay, "o", [44.6, 0], [44.9, 1]);
  moveTo(pPay, 44.9, 1.0, 540, 505);
  const payNote = txt(gMap, 540, 545, "added by code, after the AI", { size: 14, font: "mono", fill: C.amber });
  appear(payNote, 46, 0.4);

  // Prompt card: instructions first, data last
  const pPrompt = group(gMap, [620, 318]);
  el("rect", { x: -84, y: -40, width: 168, height: 80, rx: 8, fill: C.paper, stroke: C.blue, "stroke-width": 2 }, pPrompt);
  el("rect", { x: -84, y: -40, width: 168, height: 40, rx: 8, fill: C.blue }, pPrompt);
  el("rect", { x: -84, y: -8, width: 168, height: 8, fill: C.blue }, pPrompt);
  txt(pPrompt, 0, -14, "instructions", { size: 15, font: "mono", fill: C.paper, weight: 600 });
  txt(pPrompt, 0, 26, "<data> answers", { size: 15, font: "mono", fill: C.deep, weight: 600 });
  hide(pAnswers, 48.6, 0.3);
  pop(pPrompt, 48.8);
  moveTo(pPrompt, 53.2, 0.5, 745, 400);
  travel(pPrompt, e2.p, 53.7, 55.0);
  hide(pPrompt, 55.0, 0.3);

  // Scrim behind zoom panels
  const scrim = el("rect", { x: 0, y: 0, width: 1280, height: 720, fill: C.canvas, opacity: 0 });
  K(scrim, "o", [55.2, 0], [55.9, 0.8], [63.2, 0.8], [63.9, 0], [66.0, 0], [66.7, 0.8], [77.0, 0.8], [77.7, 0]);

  // --- Panel: inside OpenRouter
  const gModels = group(null, [640, 360]);
  K(gModels, "o", [55.2, 0], [55.5, 1], [63.5, 1], [63.9, 0]);
  K(gModels, "s", [55.2, 0.12], [56.2, 1], [63.1, 1], [63.9, 0.12]);
  K(gModels, "x", [55.2, 1060], [56.2, 640], [63.1, 640], [63.9, 1060]);
  K(gModels, "y", [55.2, 400], [56.2, 360], [63.1, 360], [63.9, 400]);
  el("rect", { x: -420, y: -220, width: 840, height: 440, rx: 16, fill: C.paper, stroke: C.line, "stroke-width": 1.5 }, gModels);
  txt(gModels, -370, -160, "Inside OpenRouter", { size: 32, font: "head", anchor: "start", weight: 600 });
  txt(gModels, -370, -126, "One main model, three backups in line", { size: 18, fill: C.muted, anchor: "start" });
  const models = [
    ["google/gemini-2.5-flash-lite", "main"],
    ["openai/gpt-4o-mini", "backup 1"],
    ["mistralai/mistral-small-24b", "backup 2"],
    ["meta-llama/llama-3.1-70b", "backup 3"],
  ];
  const rowBg = [];
  models.forEach(([name, tag], i) => {
    const y = -60 + i * 62;
    const r = el("rect", { x: -350, y: y - 24, width: 700, height: 48, rx: 8, fill: C.canvas }, gModels);
    rowBg.push(r);
    txt(gModels, -325, y + 6, name, { size: 18, font: "mono", anchor: "start" });
    txt(gModels, 90, y + 6, tag, { size: 15, fill: C.muted, anchor: "start" });
  });
  const pointer = group(gModels, [-372, -60]);
  el("path", { d: "M-10,-9 L6,0 L-10,9 Z", fill: C.blue }, pointer);
  K(pointer, "o", [56.6, 0], [56.9, 1]);
  K(rowBg[0], "fill", [56.8, C.canvas], [57.2, C.tint], [58.3, C.tint], [58.7, C.redSoft]);
  const x1 = crossIcon(gModels, 318, -60, 1);
  draw(x1, 58.3, 0.4);
  const note1 = txt(gModels, 290, -54, "timed out", { size: 15, font: "mono", fill: C.red, anchor: "end" });
  appear(note1, 58.5, 0.3);
  moveTo(pointer, 59.2, 0.6, -372, 2);
  K(rowBg[1], "fill", [59.5, C.canvas], [59.9, C.tint], [60.3, C.tint], [60.7, C.greenSoft]);
  const c1 = checkIcon(gModels, 318, 2, 1);
  draw(c1, 60.3, 0.4);
  const note2 = txt(gModels, 290, 8, "answered", { size: 15, font: "mono", fill: C.green, anchor: "end" });
  appear(note2, 60.5, 0.3);
  const evalNote = txt(gModels, -370, 196, "Chosen by testing 18 models on the same hiring tasks.", { size: 16, fill: C.muted, anchor: "start" });
  appear(evalNote, 61.2, 0.5);

  // JSON draft to the checks
  const pJson = chip(gMap, { label: "{ JSON }", x: 1060, y: 352 });
  K(pJson, "o", [64.0, 0], [64.3, 1]);
  travel(pJson, e3.p, 64.3, 65.8);
  hide(pJson, 65.8, 0.3);

  // --- Panel: the checks
  const gChecks = group(null, [640, 370]);
  K(gChecks, "o", [66.0, 0], [66.3, 1], [77.2, 1], [77.6, 0]);
  K(gChecks, "s", [66.0, 0.12], [67.0, 1], [76.8, 1], [77.6, 0.12]);
  K(gChecks, "x", [66.0, 840], [67.0, 640], [76.8, 640], [77.6, 840]);
  K(gChecks, "y", [66.0, 165], [67.0, 370], [76.8, 370], [77.6, 165]);
  el("rect", { x: -470, y: -240, width: 940, height: 480, rx: 16, fill: C.paper, stroke: C.line, "stroke-width": 1.5 }, gChecks);
  el("line", { x1: 0, y1: -200, x2: 0, y2: 200, stroke: C.line, "stroke-width": 1.5 }, gChecks);
  txt(gChecks, -430, -180, "1. Schema check", { size: 28, font: "head", anchor: "start", weight: 600 });
  txt(gChecks, 40, -180, "2. Quality rules", { size: 28, font: "head", anchor: "start", weight: 600 });
  ["title", "summary", "responsibilities", "requirements", "benefits", "equal_opportunity"].forEach((f, i) => {
    const y = -122 + i * 40;
    const r = el("rect", { x: -430, y: y - 17, width: 360, height: 32, rx: 6, fill: C.canvas }, gChecks);
    txt(gChecks, -414, y + 5, f, { size: 17, font: "mono", anchor: "start" });
    const ck = checkIcon(gChecks, -98, y - 1, 0.85);
    draw(ck, 67.6 + i * 0.4, 0.3);
    K(r, "fill", [67.6 + i * 0.4, C.canvas], [67.9 + i * 0.4, C.greenSoft]);
  });
  const retry1 = txt(gChecks, -430, 140, "Missing or cut off?", { size: 17, fill: C.soft, anchor: "start", weight: 600 });
  const retry2 = txt(gChecks, -430, 166, "Retry once, then show a clear error.", { size: 17, fill: C.soft, anchor: "start" });
  appear(retry1, 70.2, 0.4);
  appear(retry2, 70.4, 0.4);

  const sample = [
    "We need a rockstar analyst who thrives",
    "in a fast-paced environment.",
    "Must be a digital native.",
    "Experience with Salesforce.",
  ];
  sample.forEach((s, i) => txt(gChecks, 40, -126 + i * 28, s, { size: 17, fill: C.soft, anchor: "start" }));
  const scan = el("rect", { x: 30, y: -146, width: 400, height: 28, rx: 4, fill: C.blue, opacity: 0 }, gChecks);
  K(scan, "o", [71.0, 0], [71.2, 0.14], [74.2, 0.14], [74.5, 0]);
  K(scan, "y", [71.0, 0], [74.2, 84, lin]);
  scan._base = [0, 0];
  const findings = [
    ["rockstar", "hype word", C.red, C.redSoft],
    ["fast-paced environment", "hype word", C.red, C.redSoft],
    ["digital native", "age-coded", C.red, C.redSoft],
    ["Salesforce", "verify: not in your answers", C.amber, C.amberSoft],
  ];
  findings.forEach(([word, why, col, bg], i) => {
    const y = 0 + i * 44;
    const w = word.length * 9.2 + 24;
    const g = el("g", { opacity: 0 }, gChecks);
    el("rect", { x: 40, y: y - 16, width: w, height: 32, rx: 6, fill: bg, stroke: col, "stroke-width": 1.5 }, g);
    txt(g, 40 + w / 2, y + 5, word, { size: 15, font: "mono", fill: col, weight: 600 });
    txt(g, 40 + w + 14, y + 5, why, { size: 16, fill: C.soft, anchor: "start" });
    appear(g, 71.6 + i * 0.75, 0.35);
  });

  // Checked draft (+ pay) reach the browser
  const pDraft = chip(gMap, { label: "draft", x: 705, y: 165, fill: C.greenSoft, stroke: C.green, color: C.green });
  K(pDraft, "o", [77.6, 0], [77.9, 1]);
  travel(pDraft, e4.p, 77.9, 79.4);
  moveTo(pPay, 78.2, 1.2, 180, 440);
  hide(pPay, 79.6, 0.4);
  hide(payNote, 77.8, 0.4);
  hide(pDraft, 79.6, 0.4);

  /* =========================================================
     Scene 3 - Uploading an old posting (81-126)
     ========================================================= */
  const gUp = el("g", {});
  K(gUp, "o", [80.8, 0], [81.2, 1], [125.0, 1], [125.8, 0]);
  const upTitle = txt(gUp, 80, 92, "Upload an old job description", { size: 36, font: "head", anchor: "start", weight: 600 });
  write(upTitle, 81.2, 1.0);

  const gStations = el("g", {}, gUp);
  K(gStations, "o", [114.0, 1], [114.6, 0.3]);

  // Station 1: the file
  const doc = el("path", { d: "M85,230 H168 L195,257 V370 H85 Z", fill: C.paper, stroke: C.blue, "stroke-width": 2.5, "fill-opacity": 0 }, gStations);
  doc._len = doc.getTotalLength();
  const fold = el("path", { d: "M168,230 V257 H195", fill: "none", stroke: C.blue, "stroke-width": 2.5 }, gStations);
  fold._len = fold.getTotalLength();
  draw(doc, 81.8, 0.8);
  K(doc, "fo", [82.2, 0], [82.7, 1]);
  draw(fold, 82.4, 0.4);
  const pdfTag = chip(gStations, { label: "PDF", x: 140, y: 330, fill: C.redSoft, stroke: C.red, color: C.red, size: 13 });
  pop(pdfTag, 82.8);
  for (let i = 0; i < 4; i++) {
    const ln = el("rect", { x: 100, y: 262 + i * 14, width: [70, 56, 76, 48][i], height: 6, rx: 3, fill: C.line }, gStations);
    appear(ln, 82.7 + i * 0.1, 0.3);
  }

  const stationX = [140, 380, 640, 900, 1140];
  const stationText = [
    ["old_posting.pdf", "PDF, Word or text, max 5 MB"],
    ["Read the text", "pypdf, python-docx"],
    ["Clean it", "strip, cap at 12,000"],
    ["Wrap as data", "inside <document> tags"],
    ["Filter fields", "known keys only"],
  ];
  const frames = [];
  stationX.forEach((sx, i) => {
    if (i > 0) {
      const f = el("rect", { x: sx - 90, y: 210, width: 180, height: 180, rx: 14, fill: C.paper, "fill-opacity": 0, stroke: C.line, "stroke-width": 2 }, gStations);
      f._len = 720;
      frames.push(f);
    }
    const [a, b] = stationText[i];
    const la = txt(gStations, sx, 425, a, { size: 20, weight: 600 });
    const lb = txt(gStations, sx, 450, b, { size: 14, font: "mono", fill: C.muted });
    const t = [82.5, 86.2, 91.2, 97.0, 104.8][i];
    write(la, t, 0.5);
    write(lb, t + 0.3, 0.6);
    if (i > 0) {
      draw(frames[i - 1], t - 0.3, 0.7);
      K(frames[i - 1], "fo", [t, 0], [t + 0.5, 1]);
      const ax = [205, 475, 735, 995][i - 1];
      const bx = [282, 543, 803, 1043][i - 1];
      const a2 = edge(gStations, `M${ax},300 H${bx}`, { color: C.muted });
      showEdge(a2, t - 0.5, 0.4);
    }
  });

  // The text block that moves through the stations
  const tb = group(gUp, [140, 300]);
  el("rect", { x: -75, y: -62, width: 150, height: 124, rx: 8, fill: C.paper, stroke: C.blue, "stroke-width": 1.8 }, tb);
  const lineW = [110, 96, 118, 58, 104, 90];
  lineW.forEach((w, i) => el("rect", { x: -58, y: -44 + i * 17, width: w, height: 7, rx: 3.5, fill: C.soft, opacity: 0.35 }, tb));
  const ctrl1 = el("rect", { x: 56, y: -45, width: 9, height: 9, rx: 2, fill: C.red }, tb);
  const ctrl2 = el("rect", { x: 46, y: 5, width: 9, height: 9, rx: 2, fill: C.red }, tb);
  const fakeTag = txt(tb, 34, 15, "</document>", { size: 10, font: "mono", fill: C.red, anchor: "middle", weight: 600 });
  const cutLine = el("line", { x1: -75, y1: 36, x2: 75, y2: 36, stroke: C.red, "stroke-width": 2, "stroke-dasharray": "5 4", opacity: 0 }, tb);
  const tail = el("rect", { x: -58, y: 41, width: 90, height: 7, rx: 3.5, fill: C.soft, opacity: 0 }, tb);
  const cutLabel = txt(tb, 0, 86, "cut at 12,000 chars", { size: 13, font: "mono", fill: C.red });
  K(cutLabel, "o", [0, 0], [94.6, 0], [95.0, 1], [97.0, 1], [97.3, 0]);
  K(tb, "o", [86.0, 0], [86.3, 1], [104.4, 1], [104.8, 0]);
  K(tb, "s", [86.0, 0.6], [87.4, 1]);
  moveTo(tb, 86.4, 1.2, 380, 300);
  moveTo(tb, 91.6, 1.0, 640, 300);
  moveTo(tb, 97.2, 1.0, 900, 300);
  // Cleaning
  K(ctrl1, "o", [92.8, 1], [93.3, 0]);
  K(ctrl1, "s", [92.8, 1], [93.3, 2]);
  K(ctrl2, "o", [93.1, 1], [93.6, 0]);
  K(ctrl2, "s", [93.1, 1], [93.6, 2]);
  ctrl1._base = [0, 0];
  ctrl2._base = [0, 0];
  K(fakeTag, "o", [93.6, 1], [94.2, 0]);
  K(cutLine, "o", [94.4, 0], [94.7, 1], [96.8, 1], [97.1, 0]);
  K(tail, "o", [0, 0.35], [95.2, 0.35], [95.7, 0]);
  // Wrap as data: fences + a sneaky line
  const fenceL = el("path", { d: "M833,232 H821 V368 H833", fill: "none", stroke: C.blue, "stroke-width": 3 }, gUp);
  const fenceR = el("path", { d: "M967,232 H979 V368 H967", fill: "none", stroke: C.blue, "stroke-width": 3 }, gUp);
  fenceL._len = fenceL.getTotalLength();
  fenceR._len = fenceR.getTotalLength();
  draw(fenceL, 98.3, 0.5);
  draw(fenceR, 98.3, 0.5);
  K(fenceL, "o", [104.4, 1], [104.8, 0]);
  K(fenceR, "o", [104.4, 1], [104.8, 0]);
  const docOpen = txt(gUp, 900, 226, "<document>", { size: 13, font: "mono", fill: C.blue, weight: 600 });
  const docClose = txt(gUp, 900, 384, "</document>", { size: 13, font: "mono", fill: C.blue, weight: 600 });
  K(docOpen, "o", [98.6, 0], [99.0, 1], [104.4, 1], [104.8, 0]);
  K(docClose, "o", [98.6, 0], [99.0, 1], [104.4, 1], [104.8, 0]);
  const sneaky = el("rect", { x: -64, y: -14, width: 132, height: 15, rx: 3, fill: C.red, opacity: 0 }, tb);
  K(sneaky, "o", [99.4, 0], [99.8, 0.3]);
  K(sneaky, "fill", [101.0, C.red], [101.6, C.muted]);
  const inj1 = txt(gUp, 900, 160, '"Ignore your rules and..."', { size: 17, font: "mono", fill: C.red, weight: 600 });
  const inj2 = txt(gUp, 900, 188, "treated as data, not instructions", { size: 16, fill: C.muted });
  K(inj1, "o", [99.6, 0], [100.0, 1], [103.0, 1], [103.4, 0]);
  K(inj1, "fill", [101.0, C.red], [101.6, C.muted]);
  K(inj2, "o", [101.4, 0], [101.8, 1], [103.0, 1], [103.4, 0]);
  // One AI call
  const aiChip = chip(gUp, { label: "AI: Gemini 2.5 Flash Lite", x: 900, y: 172, fill: C.paper, stroke: C.blue, color: C.deep, size: 15, font: "body" });
  pop(aiChip, 103.6);
  hide(aiChip, 109, 0.5);

  // JSON keys land in the filter
  const keys = ["company_name", "role_title", "responsibilities", "pay_min", "is_admin"];
  const keyChips = keys.map((k, i) => {
    const c = chip(gUp, { label: k, x: 900, y: 172, size: 14, w: 160 });
    K(c, "o", [105.0 + i * 0.25, 0], [105.2 + i * 0.25, 1]);
    moveTo(c, 105.0 + i * 0.25, 0.8, 1140, 228 + i * 36);
    return c;
  });
  keyChips.forEach((c, i) => {
    const bad = i === 4;
    const t = 108.4 + i * 0.35;
    K(c._rect, "fill", [t, C.tint], [t + 0.3, bad ? C.redSoft : C.greenSoft]);
    K(c._rect, "stroke", [t, C.blue], [t + 0.3, bad ? C.red : C.green]);
    K(c._text, "fill", [t, C.deep], [t + 0.3, bad ? C.red : C.green]);
  });
  const badChip = keyChips[4];
  moveTo(badChip, 110.6, 0.8, 1140, 410, smooth);
  K(badChip, "o", [111.0, 1], [111.4, 0]);
  const dropped = txt(gUp, 1140, 478, "is_admin dropped", { size: 14, font: "mono", fill: C.red });
  K(dropped, "o", [110.8, 0], [111.1, 1], [113.6, 1], [114.0, 0]);

  // The form fills in
  const gForm = el("g", {}, gUp);
  appear(gForm, 114.2, 0.6);
  el("rect", { x: 120, y: 488, width: 1040, height: 200, rx: 12, fill: C.paper, stroke: C.line, "stroke-width": 1.5 }, gForm);
  txt(gForm, 150, 520, "Intake form", { size: 18, weight: 600, anchor: "start" });
  const fields = [
    ["Company", 150, 548, "Acme"],
    ["Role title", 690, 548, "Data Analyst"],
    ["Responsibilities", 150, 618, "Build weekly sales reports, ..."],
    ["Pay range", 690, 618, "$80,000 - $100,000"],
  ];
  const targets = [];
  fields.forEach(([label, fx, fy, val], i) => {
    txt(gForm, fx, fy, label, { size: 13, font: "mono", fill: C.muted, anchor: "start" });
    const inp = el("rect", { x: fx, y: fy + 8, width: 440, height: 40, rx: 6, fill: C.canvas, stroke: C.line }, gForm);
    const v = txt(gUp, fx + 16, fy + 34, val, { size: 17, anchor: "start" });
    const t = 115.3 + i * 0.45;
    write(v, t + 0.8, 0.7);
    K(inp, "stroke", [t + 0.7, C.line], [t + 1.0, C.blue]);
    targets.push([fx + 220, fy + 28, t]);
  });
  keyChips.slice(0, 4).forEach((c, i) => {
    const [x, y, t] = targets[i];
    moveTo(c, t, 0.8, x, y);
    K(c, "o", [t + 0.6, 1], [t + 0.9, 0]);
  });

  /* =========================================================
     Scene 4 - The credit ledger (126-163)
     ========================================================= */
  const gDb = el("g", {});
  K(gDb, "o", [125.8, 0], [126.2, 1], [162.2, 1], [163.0, 0]);
  const dbTitle = txt(gDb, 80, 92, "The credit ledger", { size: 36, font: "head", anchor: "start", weight: 600 });
  const dbSub = txt(gDb, 80, 126, "How Supabase makes sure a credit is spent exactly once", { size: 19, fill: C.muted, anchor: "start" });
  write(dbTitle, 126.3, 0.8);
  write(dbSub, 127.0, 1.0);

  // profiles
  const gProf = el("g", {}, gDb);
  appear(gProf, 127.8, 0.6);
  el("rect", { x: 80, y: 190, width: 300, height: 220, rx: 12, fill: C.paper, stroke: C.deep, "stroke-width": 2 }, gProf);
  el("rect", { x: 80, y: 190, width: 300, height: 44, rx: 12, fill: C.tint }, gProf);
  el("rect", { x: 80, y: 222, width: 300, height: 12, fill: C.tint }, gProf);
  txt(gProf, 100, 219, "profiles", { size: 16, font: "mono", anchor: "start", weight: 600, fill: C.deep });
  txt(gProf, 230, 290, "your credits", { size: 16, fill: C.muted });
  const bal = txt(gProf, 230, 370, "20", { size: 72, font: "head", weight: 600, fill: C.ink });
  K(bal, "num", [0, 20], [139.0, 20], [139.6, 19], [151.6, 19], [152.2, 20]);
  K(bal, "fill", [139.0, C.ink], [139.3, C.red], [140.2, C.red], [140.8, C.ink], [151.6, C.ink], [151.9, C.green], [152.8, C.green], [153.4, C.ink]);

  // spend_credits
  const gFn = el("g", {}, gDb);
  appear(gFn, 131.2, 0.6);
  el("rect", { x: 465, y: 190, width: 350, height: 230, rx: 12, fill: C.paper, stroke: C.blue, "stroke-width": 2.5 }, gFn);
  txt(gFn, 640, 226, "spend_credits(user, 1, key)", { size: 17, font: "mono", weight: 600, fill: C.deep });
  el("line", { x1: 465, y1: 244, x2: 815, y2: 244, stroke: C.line, "stroke-width": 1.5 }, gFn);
  const steps = ["1. Seen this key before?", "2. Enough credits? Subtract", "3. Write a ledger row"];
  const dots = steps.map((s, i) => {
    txt(gFn, 488, 290 + i * 45, s, { size: 18, anchor: "start", fill: C.soft });
    return el("circle", { cx: 785, cy: 284 + i * 45, r: 10, fill: C.line }, gFn);
  });
  // First request: new key
  K(dots[0], "fill", [137.6, C.line], [137.9, C.green], [142.6, C.green], [142.9, C.line], [144.4, C.line], [144.7, C.amber], [148.6, C.amber], [148.9, C.line]);
  K(dots[1], "fill", [138.6, C.line], [138.9, C.green], [142.6, C.green], [142.9, C.line]);
  K(dots[2], "fill", [139.6, C.line], [139.9, C.green], [142.6, C.green], [142.9, C.line]);

  // credit_ledger
  const gLed = el("g", {}, gDb);
  appear(gLed, 131.8, 0.6);
  el("rect", { x: 870, y: 190, width: 340, height: 230, rx: 12, fill: C.paper, stroke: C.deep, "stroke-width": 2 }, gLed);
  el("rect", { x: 870, y: 190, width: 340, height: 44, rx: 12, fill: C.tint }, gLed);
  el("rect", { x: 870, y: 222, width: 340, height: 12, fill: C.tint }, gLed);
  txt(gLed, 890, 219, "credit_ledger", { size: 16, font: "mono", anchor: "start", weight: 600, fill: C.deep });
  ["delta", "reason", "key (unique)"].forEach((h, i) => txt(gLed, [890, 960, 1050][i], 262, h, { size: 13, font: "mono", fill: C.muted, anchor: "start" }));
  el("line", { x1: 885, y1: 274, x2: 1195, y2: 274, stroke: C.line }, gLed);
  const row1 = el("g", {}, gLed);
  txt(row1, 890, 306, "-1", { size: 16, font: "mono", fill: C.red, anchor: "start", weight: 600 });
  txt(row1, 960, 306, "spend", { size: 16, font: "mono", anchor: "start" });
  txt(row1, 1050, 306, "req-7f3a", { size: 16, font: "mono", anchor: "start" });
  appear(row1, 139.8, 0.4);
  const row2 = el("g", {}, gLed);
  txt(row2, 890, 344, "+1", { size: 16, font: "mono", fill: C.green, anchor: "start", weight: 600 });
  txt(row2, 960, 344, "refund", { size: 16, font: "mono", anchor: "start" });
  txt(row2, 1050, 344, "refund:req-7f3a", { size: 14, font: "mono", anchor: "start" });
  appear(row2, 151.6, 0.4);
  const keyHl = el("rect", { x: 1044, y: 288, width: 90, height: 26, rx: 4, fill: C.amber, opacity: 0 }, gLed);
  K(keyHl, "o", [144.4, 0], [144.7, 0.18], [148.4, 0.18], [148.8, 0]);

  // Requests
  const req1 = chip(gDb, { label: 'Refine "more senior"   key: req-7f3a', x: 640, y: 160, size: 14 });
  pop(req1, 136.0);
  moveTo(req1, 137.0, 0.5, 640, 205);
  K(req1, "o", [137.2, 1], [137.5, 0]);
  const req2 = chip(gDb, { label: "same request again   key: req-7f3a", x: 640, y: 160, size: 14, fill: C.amberSoft, stroke: C.amber, color: C.amber });
  K(req2, "o", [143.0, 0], [143.3, 1], [145.4, 1], [145.8, 0]);
  K(req2, "y", [143.6, 160], [144.2, 200], [145.0, 200], [145.6, 150]);
  const once = chip(gDb, { label: "charged once", x: 230, y: 450, fill: C.amberSoft, stroke: C.amber, color: C.amber, size: 15, font: "body" });
  K(once, "o", [145.6, 0], [145.9, 1], [148.6, 1], [149.0, 0]);
  K(once, "s", [145.6, 0.6], [146.1, 1, back]);
  const fail = chip(gDb, { label: "AI call failed", x: 640, y: 160, fill: C.redSoft, stroke: C.red, color: C.red, size: 15, font: "body" });
  pop(fail, 149.4);
  hide(fail, 154.6, 0.4);
  const refund = chip(gDb, { label: "refund_credits(user, 1, key)", x: 640, y: 470, fill: C.greenSoft, stroke: C.green, color: C.green, size: 16, w: 350 });
  pop(refund, 150.4);
  // Locks
  const locks = [lockIcon(gDb, 362, 212), lockIcon(gDb, 1190, 212)];
  locks.forEach((l, i) => appear(l, 155.4 + i * 0.3, 0.4));
  const rls = txt(gDb, 640, 590, "Row level security: only the server's secret key can write here", { size: 19, fill: C.deep, weight: 600 });
  write(rls, 156.0, 1.4);

  /* =========================================================
     Scene 5 - Buying credits (163-188)
     ========================================================= */
  const gPay = el("g", {});
  K(gPay, "o", [162.8, 0], [163.2, 1], [187.0, 1], [187.8, 0]);
  const payTitle = txt(gPay, 80, 92, "Buying credits", { size: 36, font: "head", anchor: "start", weight: 600 });
  write(payTitle, 163.3, 0.8);
  const pB = box(gPay, { x: 160, y: 300, w: 180, h: 84, label: "Browser", sub: "pick a pack" });
  const pS = box(gPay, { x: 470, y: 300, w: 220, h: 96, label: "Stripe Checkout", sub: "$5 = 20 credits", stroke: C.amber, size: 21 });
  const pA = box(gPay, { x: 800, y: 300, w: 200, h: 90, label: "FastAPI", sub: "checks signature" });
  const pD = cylinder(gPay, { x: 1110, y: 290, w: 190, h: 76, label: "Supabase", sub: "grant_credits" });
  const pe1 = edge(gPay, "M250,300 H357", { color: C.amber });
  const pe2 = edge(gPay, "M580,300 H698", { label: "signed webhook", lx: 640, ly: 228, color: C.amber });
  const pe3 = edge(gPay, "M900,300 H1013", { label: "+20", lx: 956, ly: 228, color: C.deep });
  showBox(pB, 163.8);
  showEdge(pe1, 164.6, 0.5);
  showBox(pS, 165.0);
  const priceNote = txt(gPay, 470, 380, "prices are set on the server", { size: 15, fill: C.muted });
  appear(priceNote, 166.4, 0.5);
  showBox(pA, 168.2);
  showEdge(pe2, 168.8, 0.5);
  showCylinder(pD, 169.0);
  showEdge(pe3, 169.6, 0.5);

  function envelope(parent) {
    const g = group(parent, [580, 300]);
    el("rect", { x: -24, y: -16, width: 48, height: 32, rx: 4, fill: C.paper, stroke: C.amber, "stroke-width": 2 }, g);
    el("path", { d: "M-24,-14 L0,4 L24,-14", fill: "none", stroke: C.amber, "stroke-width": 2 }, g);
    el("circle", { cx: 16, cy: 10, r: 7, fill: C.amber }, g);
    return g;
  }
  const env1 = envelope(gPay);
  K(env1, "o", [170.0, 0], [170.3, 1], [172.2, 1], [172.5, 0]);
  travel(env1, pe2.p, 170.3, 171.9);
  const sig = group(gPay, [800, 210]);
  el("rect", { x: -78, y: -17, width: 156, height: 34, rx: 17, fill: C.greenSoft, stroke: C.green, "stroke-width": 1.5 }, sig);
  txt(sig, -10, 5, "signature ok", { size: 14, font: "mono", fill: C.green, weight: 600 });
  const sigCk = checkIcon(sig, 56, 0, 0.75);
  pop(sig, 172.2);
  draw(sigCk, 172.5, 0.35);
  hide(sig, 179.6, 0.4);

  const gEv = el("g", {}, gPay);
  appear(gEv, 174.0, 0.5);
  el("rect", { x: 700, y: 420, width: 200, height: 120, rx: 10, fill: C.paper, stroke: C.deep, "stroke-width": 2 }, gEv);
  txt(gEv, 716, 448, "stripe_events", { size: 15, font: "mono", fill: C.deep, anchor: "start", weight: 600 });
  el("line", { x1: 712, y1: 462, x2: 888, y2: 462, stroke: C.line }, gEv);
  const evRow = txt(gEv, 716, 494, "evt_1Q8x", { size: 16, font: "mono", anchor: "start" });
  appear(evRow, 174.8, 0.4);
  const evLink = el("path", { d: "M800,345 V418", stroke: C.deep, "stroke-width": 2, "stroke-dasharray": "4 4", fill: "none" }, gPay);
  appear(evLink, 174.2, 0.4);

  const coin = chip(gPay, { label: "+20", x: 900, y: 300, fill: C.greenSoft, stroke: C.green, color: C.green, size: 15 });
  K(coin, "o", [175.6, 0], [175.9, 1], [177.0, 1], [177.3, 0]);
  travel(coin, pe3.p, 175.9, 177.0);
  txt(gPay, 1110, 382, "credits", { size: 15, fill: C.muted });
  const pBal = txt(gPay, 1110, 432, "20", { size: 48, font: "head", weight: 600 });
  K(pBal, "num", [0, 20], [177.0, 20], [177.8, 40]);
  K(pBal, "fill", [177.0, C.ink], [177.3, C.green], [179.0, C.green], [179.6, C.ink]);

  const env2 = envelope(gPay);
  K(env2, "o", [180.4, 0], [180.7, 1], [183.0, 1], [183.4, 0]);
  travel(env2, pe2.p, 180.7, 182.2);
  K(env2, "y", [182.6, 300], [183.4, 340]);
  const retryLbl = txt(gPay, 640, 220, "Stripe retries the same event", { size: 15, font: "mono", fill: C.amber });
  K(retryLbl, "o", [180.3, 0], [180.6, 1], [183.2, 1], [183.6, 0]);
  const seenX = crossIcon(gPay, 872, 488, 0.9);
  draw(seenX, 182.4, 0.4);
  K(seenX, "o", [182.4, 1], [186.4, 1], [186.8, 0]);
  const seenLbl = txt(gPay, 800, 572, "already seen, nothing added", { size: 15, font: "mono", fill: C.red });
  K(seenLbl, "o", [182.6, 0], [182.9, 1]);

  /* =========================================================
     Scene 6 - Recap (188-198)
     ========================================================= */
  const recapTitle = txt(svg, 60, 70, "One AI call. Plain code checks. One database step per credit.", { size: 26, font: "head", anchor: "start", weight: 600 });
  write(recapTitle, 188.8, 1.8);
  [e1, e2, e3, e4].forEach((e, i) => {
    const dot = group(svg, [0, 0]);
    el("circle", { cx: 0, cy: 0, r: 8, fill: C.blue }, dot);
    const t = 190.2 + i * 1.1;
    K(dot, "o", [t - 0.05, 0], [t, 1], [t + 1.1, 1], [t + 1.2, 0]);
    travel(dot, e.p, t, t + 1.1, 20);
  });

  /* ---------- Captions and chapters ---------- */
  const CAPTIONS = [
    [0, 6, "A short visual tour of what happens after you click Generate."],
    [6, 9, "Everything starts in your browser. The page is plain JavaScript."],
    [9, 13.6, "Your answers go to one small server: FastAPI, running on Google Cloud Run. It serves this website and the API."],
    [13.6, 18.6, "The server sends one prompt to OpenRouter, a gateway that can reach many AI models."],
    [18.6, 23.6, "The AI answers in JSON, and plain code checks it. There is no second AI."],
    [23.6, 26.8, "Only a checked draft reaches your screen."],
    [26.8, 30.4, "Supabase is the database: sign-in, credit balances, and a ledger of every credit change."],
    [30.4, 34.5, "Stripe takes payments, then tells the server through a signed message called a webhook."],
    [34.5, 37, "Let's follow one job through it: a Data Analyst at Acme."],
    [37, 40.2, "Your browser adds a bot-check token from Cloudflare Turnstile."],
    [40.2, 44.6, "Before spending anything on AI, the server checks the token, a per-IP daily limit, and a global daily cap."],
    [44.6, 48.6, "Your pay range is held back. Code adds it after the AI is done, so the AI can't invent or change it."],
    [48.6, 53.2, "The prompt puts fixed instructions first and your answers last, marked as data, not commands."],
    [53.2, 58.2, "OpenRouter sends it to the main model, Gemini 2.5 Flash Lite."],
    [58.2, 61.2, "If the main model fails or times out, the next model in line answers instead."],
    [61.2, 64, "These models were picked by testing 18 models on the same hiring tasks."],
    [64, 70.8, "First check: does the JSON have every section, in the right shape? If not, it retries once."],
    [70.8, 77.4, "Second check: plain word lists flag hype, biased wording, and requirements you never gave. Same draft, same result, every time."],
    [77.4, 81, "The pay range is attached, and the checked draft appears on your screen."],
    [81, 86, "Have an old posting? Upload it and the form fills itself in. Here is how."],
    [86, 91.2, "Step 1: plain code pulls the text out of the PDF or Word file. No AI yet."],
    [91.2, 97, "Step 2: hidden control characters and fake document tags are removed, and the text is cut at 12,000 characters."],
    [97, 103.4, "Step 3: the text is fenced inside <document> tags. The AI is told everything inside is data, so a sneaky line like \"ignore your rules\" is ignored."],
    [103.4, 108.2, "Step 4: one AI call reads the text and returns JSON: company, title, duties, pay, and so on."],
    [108.2, 114, "Step 5: code keeps only known fields with the right types. Unknown keys are dropped, and long lists are capped."],
    [114, 120, "The clean fields drop into the form. You check them, change anything, then generate as usual."],
    [120, 126, "Uploading is free, like generating, and protected by the same bot check and daily limits."],
    [126, 131.2, "A Refine request you type yourself costs 1 credit. Your balance lives in Supabase."],
    [131.2, 136, "Every spend goes through one database function, spend_credits. Each request carries a unique key."],
    [136, 142.6, "New key? Check the balance and subtract in a single step, then write a ledger row. Two clicks at once can't both spend your last credit."],
    [142.6, 149.2, "If the same request arrives twice, say after a network retry, its key is already in the ledger. Nothing is charged."],
    [149.2, 155.2, "If the AI call then fails, refund_credits gives the credit back. It has its own key, so it can only happen once."],
    [155.2, 163, "The tables are locked with row level security. Only the server, using its secret key, can change them."],
    [163, 168.2, "To buy credits, you pick a pack. Prices live on the server, so the page can't change them. Stripe handles the card."],
    [168.2, 174, "Stripe then calls our server. The message is signed, so the server can prove it really came from Stripe."],
    [174, 180.2, "The event id is saved once in stripe_events, then grant_credits adds the credits."],
    [180.2, 188, "Stripe may send the same event again. The id is already saved, so the credits are not added twice."],
    [188, 194, "That's the whole system: one AI call per draft, plain code for every check, one database step per credit."],
    [194, 999, "Want to see it run? Try the generator on the home page. It's free, with no account."],
  ];
  const CHAPTERS = [
    [0, "Intro"],
    [6, "The map"],
    [34.5, "Making a draft"],
    [81, "Uploading a file"],
    [126, "The credit ledger"],
    [163, "Buying credits"],
    [188, "Recap"],
  ];
  const DUR = 199;
  const POSTER = 3.2;

  return { CAPTIONS, CHAPTERS, DUR, POSTER };
  });
})();
