"use strict";

// Draft tools: quality check, free quick edits, section rewrite, "verify" marks,
// undo history, upload change summary and screening questions.
// app.js calls these through `feature(name, ...args)`, so the core generate and
// refine flow keeps working even if anything here fails.
(function () {
  const VERSIONS_KEY = "linkedinJobGeneratorVersions";
  const MAX_VERSIONS = 8;
  const MIN_LINE_CHARS = 15;
  const MAX_DIFF_ITEMS = 8;
  const SECTION_BY_HEADING = {
    "About the Role": "about_role",
    "Responsibilities": "responsibilities",
    "Requirements": "requirements",
    "Nice to Have": "nice_to_haves",
    "Benefits": "benefits",
    "Why Join Us": "why_join_us",
  };
  const FIX_BY_FINDING = {
    age_coded: "more_inclusive",
    exclusionary: "more_inclusive",
    gender_masculine: "more_inclusive",
    gender_feminine: "more_inclusive",
    hard_to_read: "simplify",
    too_long: "shorter",
    too_many_responsibilities: "cut_bullets",
    too_many_requirements: "cut_bullets",
  };
  const ACTION_LABELS = {
    shorter: "Shorter",
    more_inclusive: "More inclusive",
    simplify: "Simplify wording",
    more_casual: "More casual",
    more_formal: "More formal",
    cut_bullets: "Cut to 6 bullets",
    nice_to_have: "Move extras to nice-to-have",
  };

  const features = {};
  window.__features = features;
  const $ = (id) => document.getElementById(id);

  let versions = [];
  let versionIndex = -1;
  let busy = false;
  let highlightChanges = true;
  let originalDoc = { text: "", name: "" };

  // ---------- helpers ----------

  function safeStorage(action) {
    try {
      return action();
    } catch (err) {
      console.warn("Storage unavailable:", err);
      return null;
    }
  }

  function normalizeLine(text) {
    return text.toLowerCase().replace(/[^a-z0-9\s]/g, " ").replace(/\s+/g, " ").trim();
  }

  function tokens(text) {
    return new Set(normalizeLine(text).split(" ").filter((word) => word.length > 2));
  }

  function jaccard(a, b) {
    if (!a.size || !b.size) return 0;
    let shared = 0;
    for (const word of a) if (b.has(word)) shared++;
    return shared / (a.size + b.size - shared);
  }

  function splitIntoLines(text) {
    return text
      .split(/\n+|(?<=[.!?])\s+/)
      .map((line) => line.replace(/^[\s#>*\-•]+/, "").trim())
      .filter((line) => line.length >= MIN_LINE_CHARS);
  }

  // ---------- versions / undo ----------

  function persistVersions() {
    safeStorage(() => localStorage.setItem(VERSIONS_KEY, JSON.stringify({ versions, versionIndex })));
  }

  function loadVersions() {
    const saved = safeStorage(() => localStorage.getItem(VERSIONS_KEY));
    if (!saved) return;
    try {
      const parsed = JSON.parse(saved);
      if (Array.isArray(parsed.versions)) {
        versions = parsed.versions.slice(-MAX_VERSIONS);
        versionIndex = Math.min(parsed.versionIndex ?? versions.length - 1, versions.length - 1);
      }
    } catch {
      versions = [];
      versionIndex = -1;
    }
  }

  function pushVersion(label) {
    versions = versions.slice(0, versionIndex + 1);
    versions.push({
      label,
      draft: state.currentDraft,
      markdown: state.currentMarkdown,
      quality: state.quality || null,
      at: Date.now(),
    });
    if (versions.length > MAX_VERSIONS) versions.shift();
    versionIndex = versions.length - 1;
    persistVersions();
  }

  function saveDraftToStorage() {
    safeStorage(() => {
      localStorage.setItem(DRAFT_STORAGE_KEY, JSON.stringify(state.currentDraft));
      localStorage.setItem(MARKDOWN_STORAGE_KEY, state.currentMarkdown);
    });
  }

  function goToVersion(index) {
    if (index < 0 || index >= versions.length) return;
    versionIndex = index;
    const version = versions[index];
    state.currentDraft = version.draft;
    state.currentMarkdown = version.markdown;
    state.quality = version.quality;
    persistVersions();
    saveDraftToStorage();
    renderDraft();
  }

  function renderVersionBar() {
    const bar = $("versionBar");
    if (!bar) return;
    const hasHistory = versions.length > 1;
    bar.classList.toggle("hidden", !state.currentDraft || !hasHistory);
    if (!hasHistory) return;
    const current = versions[versionIndex];
    $("versionLabel").textContent = `Version ${versionIndex + 1} of ${versions.length}: ${current ? current.label : ""}`;
    $("undoBtn").disabled = versionIndex <= 0;
    $("redoBtn").disabled = versionIndex >= versions.length - 1;
  }

  // Called by app.js after a generate or refine finished (state already updated).
  features.onDraftReady = function (label) {
    saveDraftToStorage();
    pushVersion(label);
  };

  // A free edit returned a new draft.
  function applyEditResult(data, label) {
    state.currentDraft = data.draft;
    state.currentMarkdown = data.markdown;
    state.quality = data.quality || null;
    saveDraftToStorage();
    pushVersion(label);
    renderDraft();
    showToast(label);
  }

  let toastTimer = null;
  function showToast(label) {
    const toast = $("toast");
    if (!toast || versionIndex < 1) return;
    toast.innerHTML = `<span>${escapeHtml(label)}</span> <button type="button" class="toast-undo">Undo</button>`;
    toast.classList.remove("hidden");
    toast.querySelector(".toast-undo").addEventListener("click", () => {
      toast.classList.add("hidden");
      goToVersion(versionIndex - 1);
    });
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.add("hidden"), 6000);
  }

  // ---------- rendering after each draft render ----------

  features.afterRenderDraft = function () {
    renderQuality();
    renderVersionBar();
    renderChangeNote();
    decoratePreview();
    updateEditControls();
    $("adjustBlock")?.classList.toggle("hidden", !state.currentDraft);
    const screeningBtn = $("screeningBtn");
    if (screeningBtn) screeningBtn.disabled = !state.currentDraft || busy;
  };

  function previousMarkdown() {
    return versionIndex > 0 && versions[versionIndex - 1] ? versions[versionIndex - 1].markdown : "";
  }

  function lastWasEdit() {
    const current = versions[versionIndex];
    return Boolean(current && !current.label.startsWith("Generated") && !current.label.startsWith("Restored"));
  }

  function renderChangeNote() {
    const note = $("changeNote");
    if (!note) return;
    const before = previousMarkdown();
    if (!state.currentMarkdown || !before || !lastWasEdit()) {
      note.classList.add("hidden");
      return;
    }
    const oldSet = new Set(splitIntoLines(before).map(normalizeLine));
    const newLines = splitIntoLines(state.currentMarkdown);
    const newSet = new Set(newLines.map(normalizeLine));
    const added = newLines.filter((line) => !oldSet.has(normalizeLine(line))).length;
    const removed = [...oldSet].filter((line) => !newSet.has(line)).length;
    note.classList.remove("hidden");
    $("changeNoteText").textContent = `What changed: ${added} line${added === 1 ? "" : "s"} new or reworded, ${removed} removed.`;
    $("highlightToggle").checked = highlightChanges;
  }

  function decoratePreview() {
    const preview = $("markdownPreview");
    if (!preview || preview.classList.contains("empty")) return;

    // Highlight lines that changed in the last edit.
    if (highlightChanges && lastWasEdit()) {
      const before = previousMarkdown();
      if (before) {
        const oldSet = new Set(splitIntoLines(before).map(normalizeLine));
        preview.querySelectorAll("li, p").forEach((node) => {
          const text = node.textContent.trim();
          if (text.length >= MIN_LINE_CHARS && !oldSet.has(normalizeLine(text))) node.classList.add("changed-line");
        });
      }
    }

    // Mark requirements that do not come from the user's answers.
    const unverified = new Set(
      ((state.quality && state.quality.findings) || [])
        .filter((finding) => finding.code === "unverified_requirements")
        .flatMap((finding) => finding.matches)
        .map((text) => text.trim())
    );
    if (unverified.size) {
      preview.querySelectorAll("li").forEach((node) => {
        if (unverified.has(node.textContent.trim())) {
          node.classList.add("assumption");
          const badge = document.createElement("span");
          badge.className = "assumption-badge";
          badge.textContent = "verify";
          badge.title = "Not from your answers. Check it is true, or remove it.";
          node.append(badge);
        }
      });
    }

    // Per-section rewrite buttons (free).
    preview.querySelectorAll("h2").forEach((heading) => {
      const text = heading.firstChild ? heading.firstChild.textContent.trim() : "";
      let section = SECTION_BY_HEADING[text];
      if (!section && text.startsWith("About ") && text !== "About the Role") section = "about_company";
      if (!section) return;
      const button = document.createElement("button");
      button.type = "button";
      button.className = "section-rewrite-btn";
      button.dataset.section = section;
      button.textContent = "Rewrite";
      button.title = "Rewrite only this section. Free.";
      button.disabled = busy || state.draftOutdated;
      heading.append(button);
    });
  }

  // ---------- quality panel ----------

  function scoreClass(score) {
    if (score >= 80) return "q-good";
    if (score >= 60) return "q-ok";
    return "q-bad";
  }

  function renderQuality() {
    const panel = $("qualityPanel");
    if (!panel) return;
    const report = state.quality;
    if (!report || !state.currentDraft) {
      panel.classList.add("hidden");
      return;
    }
    panel.classList.remove("hidden");
    const findings = report.findings || [];
    const stats = report.stats || {};
    const items = findings
      .map((finding) => {
        const fixAction = FIX_BY_FINDING[finding.code];
        const fix = fixAction
          ? `<button type="button" class="fix-btn" data-action="${fixAction}">Fix: ${escapeHtml(ACTION_LABELS[fixAction])}</button>`
          : "";
        const matches = (finding.matches || []).slice(0, 6).map((m) => `<code>${escapeHtml(m)}</code>`).join(" ");
        return `<li class="q-item q-${finding.severity}">
          <span class="q-dot" aria-hidden="true"></span>
          <span class="q-body"><span class="q-msg">${escapeHtml(finding.message)}</span>
          ${finding.suggestion ? `<span class="q-tip">${escapeHtml(finding.suggestion)}</span>` : ""}
          ${matches ? `<span class="q-matches">${matches}</span>` : ""}</span>
          ${fix}
        </li>`;
      })
      .join("");
    const count = findings.length;
    panel.innerHTML = `
      <details>
        <summary>
          <span class="q-score ${scoreClass(report.score)}">${report.score}</span>
          <strong>Quality</strong>
          <span class="q-count">${count ? `${count} to look at` : "looks good"}</span>
          <span class="q-chevron" aria-hidden="true"></span>
        </summary>
        ${items ? `<ul class="q-list">${items}</ul>` : ""}
        <p class="q-stats">${stats.word_count || 0} words - reading grade ${stats.reading_grade || 0}. Free, rule-based, no AI used.</p>
      </details>`;
  }

  // ---------- free edits: chips + section rewrite ----------

  function updateEditControls() {
    const disabled = busy || !state.currentDraft || state.draftOutdated;
    document.querySelectorAll("#adjustBlock [data-action], .fix-btn, .section-rewrite-btn").forEach((button) => {
      button.disabled = disabled;
    });
  }

  async function runFreeEdit(path, extra, label) {
    if (busy || !state.currentDraft) return;
    busy = true;
    updateEditControls();
    setMessage("Working on it. This edit is free.", "info");
    try {
      const headers = await guestHeaders();
      const data = await callApi(
        path,
        {
          company_name: state.answers.company_name || "",
          current_draft: state.currentDraft,
          skipped_fields: getSkippedFields(),
          job_info: buildJobInfo(),
          ...extra,
        },
        headers
      );
      busy = false;
      applyEditResult(data, label);
      setMessage("");
    } catch (error) {
      setMessage(error.message);
    } finally {
      busy = false;
      renderDraft();
    }
  }

  function onChipClick(event) {
    const chip = event.target.closest("[data-action]");
    if (!chip || chip.disabled) return;
    const action = chip.dataset.action;
    runFreeEdit("/quick-edit", { action }, ACTION_LABELS[action] || action);
  }

  function onPreviewClick(event) {
    const button = event.target.closest(".section-rewrite-btn");
    if (!button || button.disabled) return;
    const section = button.dataset.section;
    runFreeEdit("/regenerate-section", { section }, `Rewrote ${section.replaceAll("_", " ")}`);
  }

  // ---------- upload diff ----------

  features.setOriginalDoc = function (text, name) {
    originalDoc = { text, name };
    const panel = $("diffPanel");
    if (panel) panel.classList.add("hidden");
  };

  features.showUploadDiff = function () {
    const panel = $("diffPanel");
    if (!panel) return;
    if (!originalDoc.text || !state.currentMarkdown) {
      panel.classList.add("hidden");
      return;
    }
    const originalLines = splitIntoLines(originalDoc.text);
    const newLines = splitIntoLines(state.currentMarkdown.replace(/^#+ .*$/gm, ""));
    const originalTokens = originalLines.map(tokens);
    const newTokens = newLines.map(tokens);
    const bestScore = (source, targets) => targets.reduce((best, target) => Math.max(best, jaccard(source, target)), 0);

    let kept = 0;
    let reworded = 0;
    const fresh = [];
    newTokens.forEach((set, index) => {
      const score = bestScore(set, originalTokens);
      if (score >= 0.85) kept++;
      else if (score >= 0.4) reworded++;
      else fresh.push(newLines[index]);
    });
    const dropped = originalLines.filter((_, index) => bestScore(originalTokens[index], newTokens) < 0.4);

    const list = (items) => items.slice(0, MAX_DIFF_ITEMS).map((line) => `<li>${escapeHtml(line.slice(0, 160))}</li>`).join("");
    panel.classList.remove("hidden");
    panel.innerHTML = `
      <details>
        <summary><strong>What changed from ${escapeHtml(originalDoc.name || "your file")}</strong>
          <small>${kept} kept - ${reworded} reworded - ${fresh.length} new - ${dropped.length} dropped</small></summary>
        <div class="diff-cols">
          <div><h4>New in the draft (check these are true)</h4>${fresh.length ? `<ul class="diff-new">${list(fresh)}</ul>` : "<p>Nothing new added.</p>"}</div>
          <div><h4>Left out from your file</h4>${dropped.length ? `<ul class="diff-dropped">${list(dropped)}</ul>` : "<p>Nothing dropped.</p>"}</div>
        </div>
        <p class="q-stats">Estimated by comparing wording. A rewrite is not a fact check: please read the new lines.</p>
      </details>`;
  };

  // ---------- screening questions ----------

  async function onScreeningClick() {
    if (!state.currentDraft || busy) return;
    const button = $("screeningBtn");
    const list = $("screeningList");
    busy = true;
    button.disabled = true;
    button.textContent = "Writing questions...";
    try {
      const headers = await guestHeaders();
      const data = await callApi("/screening-questions", { current_draft: state.currentDraft }, headers);
      const labels = { must_have: "Must-have", culture: "Culture", logistics: "Logistics" };
      list.classList.remove("hidden");
      list.innerHTML = `<ol>${data.questions
        .map(
          (item) => `<li><span class="tag">${escapeHtml(labels[item.type] || item.type)}</span>
            <strong>${escapeHtml(item.question)}</strong>
            ${item.ideal_answer ? `<em>Good answer: ${escapeHtml(item.ideal_answer)}</em>` : ""}</li>`
        )
        .join("")}</ol>
        <button type="button" class="secondary-button" id="copyScreeningBtn">Copy questions</button>`;
      $("copyScreeningBtn").addEventListener("click", async () => {
        const text = data.questions.map((item, index) => `${index + 1}. ${item.question}`).join("\n");
        await navigator.clipboard.writeText(text);
        showButtonSuccess($("copyScreeningBtn"), "Copied");
      });
    } catch (error) {
      setMessage(error.message);
    } finally {
      busy = false;
      button.textContent = "Suggest screening questions";
      renderDraft();
    }
  }

  // ---------- workspace reset ----------

  features.onWorkspaceCleared = function () {
    versions = [];
    versionIndex = -1;
    state.quality = null;
    originalDoc = { text: "", name: "" };
    persistVersions();
    ["diffPanel", "screeningList", "changeNote"].forEach((id) => {
      const node = $(id);
      if (node) node.classList.add("hidden");
    });
  };

  // ---------- init ----------

  function bind() {
    $("adjustBlock")?.addEventListener("click", onChipClick);
    $("qualityPanel")?.addEventListener("click", onChipClick);
    $("markdownPreview")?.addEventListener("click", onPreviewClick);
    $("undoBtn")?.addEventListener("click", () => goToVersion(versionIndex - 1));
    $("redoBtn")?.addEventListener("click", () => goToVersion(versionIndex + 1));
    $("highlightToggle")?.addEventListener("change", (event) => {
      highlightChanges = event.target.checked;
      renderDraft();
    });
    $("screeningBtn")?.addEventListener("click", onScreeningClick);
  }

  function init() {
    loadVersions();
    bind();
    if (state.currentDraft && !versions.length) {
      versions = [{ label: "Restored draft", draft: state.currentDraft, markdown: state.currentMarkdown, quality: null, at: Date.now() }];
      versionIndex = 0;
    } else if (versions[versionIndex]) {
      state.quality = versions[versionIndex].quality;
    }
    renderDraft();
  }

  init();
})();
