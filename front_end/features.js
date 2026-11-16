"use strict";

// Optional feature layer. app.js calls these through `feature(name, ...args)`,
// so the core generate/refine flow still works if anything here fails.
(function () {
  const VERSIONS_KEY = "linkedinJobGeneratorVersions";
  const PAY_KEY = "linkedinJobGeneratorPay";
  const PENDING_KEY = "linkedinJobGeneratorPendingRefine";
  const PENDING_MAX_AGE_MS = 24 * 60 * 60 * 1000;
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
  let pay = { jurisdiction: "none", currency: "USD", period: "year", min: "", max: "" };
  let originalDoc = { text: "", name: "" };
  let configPromise = null;
  let turnstileWidgetId = null;
  let turnstileScriptPromise = null;

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

  // ---------- config + Turnstile ----------

  function loadConfig() {
    configPromise = fetch(apiUrl("/config"))
      .then((response) => (response.ok ? response.json() : null))
      .catch(() => null)
      .then((config) => {
        if (config) {
          state.config = config;
          applyConfig();
        }
        return config;
      });
    return configPromise;
  }

  function applyConfig() {
    const config = state.config;
    if (!config) return;
    const select = $("payJurisdiction");
    if (select && config.jurisdictions) {
      select.innerHTML = config.jurisdictions
        .map((item) => `<option value="${escapeHtml(item.code)}">${escapeHtml(item.label)}</option>`)
        .join("");
      select.value = pay.jurisdiction;
    }
    document.querySelectorAll("[data-free-credits]").forEach((node) => {
      node.textContent = config.free_signup_credits;
    });
    renderPayNotice();
    updateRefineButton();
  }

  function loadTurnstileScript() {
    if (!turnstileScriptPromise) {
      turnstileScriptPromise = new Promise((resolve) => {
        const script = document.createElement("script");
        script.src = "https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit";
        script.async = true;
        script.onload = () => resolve(true);
        script.onerror = () => resolve(false);
        document.head.append(script);
      });
    }
    return turnstileScriptPromise;
  }

  // Returns a fresh one-time token, or null when Turnstile is not enabled.
  features.turnstileToken = async function () {
    await configPromise;
    const siteKey = state.config && state.config.turnstile_site_key;
    if (!siteKey) return null;
    if (!(await loadTurnstileScript()) || !window.turnstile) return null;
    return new Promise((resolve) => {
      const box = $("turnstileBox");
      if (!box) return resolve(null);
      if (turnstileWidgetId !== null) {
        window.turnstile.remove(turnstileWidgetId);
        turnstileWidgetId = null;
      }
      const timer = setTimeout(() => resolve(null), 20000);
      turnstileWidgetId = window.turnstile.render(box, {
        sitekey: siteKey,
        appearance: "interaction-only",
        callback: (token) => {
          clearTimeout(timer);
          resolve(token);
        },
        "error-callback": () => {
          clearTimeout(timer);
          resolve(null);
        },
      });
    });
  };

  // ---------- pay range ----------

  function loadPay() {
    const saved = safeStorage(() => localStorage.getItem(PAY_KEY));
    if (saved) {
      try {
        pay = { ...pay, ...JSON.parse(saved) };
      } catch {
        // Ignore a corrupt saved value.
      }
    }
  }

  function savePay() {
    safeStorage(() => localStorage.setItem(PAY_KEY, JSON.stringify(pay)));
  }

  function payNumbers() {
    const min = parseFloat(pay.min);
    const max = parseFloat(pay.max);
    return {
      min: Number.isFinite(min) && min > 0 ? min : null,
      max: Number.isFinite(max) && max > 0 ? max : null,
    };
  }

  function currentJurisdiction() {
    const list = (state.config && state.config.jurisdictions) || [];
    return list.find((item) => item.code === pay.jurisdiction) || null;
  }

  function payRequired() {
    const jurisdiction = currentJurisdiction();
    return Boolean(jurisdiction && jurisdiction.pay_required);
  }

  features.payJobInfo = function () {
    const { min, max } = payNumbers();
    return {
      pay_min: min,
      pay_max: max,
      pay_currency: pay.currency,
      pay_period: pay.period,
      jurisdiction: pay.jurisdiction,
    };
  };

  features.setPayFromUpload = function (key, value) {
    const number = Number(value);
    if (!Number.isFinite(number) || number <= 0) return;
    pay[key === "pay_min" ? "min" : "max"] = String(number);
    savePay();
    syncPayInputs();
    renderPayNotice();
  };

  function syncPayInputs() {
    const fields = { payJurisdiction: pay.jurisdiction, payCurrency: pay.currency, payPeriod: pay.period, payMin: pay.min, payMax: pay.max };
    for (const [id, value] of Object.entries(fields)) {
      const node = $(id);
      if (node) node.value = value;
    }
  }

  function renderPayNotice() {
    const notice = $("payNotice");
    if (!notice) return;
    const { min, max } = payNumbers();
    const hasRange = min !== null && max !== null;
    const jurisdiction = currentJurisdiction();
    let kind = "info";
    let html;
    if (hasRange && min > max) {
      kind = "error";
      html = "<strong>Minimum is higher than maximum.</strong> Please fix the range.";
    } else if (jurisdiction && jurisdiction.pay_required && !hasRange) {
      kind = "warn";
      html = `<strong>Pay range required in ${escapeHtml(jurisdiction.label)}.</strong> ${escapeHtml(jurisdiction.note)} Add a minimum and maximum. This is a summary, not legal advice.`;
    } else if (hasRange) {
      kind = "ok";
      html = "Pay range will be added to your job description exactly as you typed it. The AI never writes pay numbers.";
    } else {
      html = "Optional. In vendor surveys, 44-60% of candidates say they skip ads with no pay shown. Rules differ by place; pick yours above.";
    }
    notice.className = `pay-notice pay-${kind}`;
    notice.innerHTML = html;
  }

  function onPayChanged() {
    pay.jurisdiction = $("payJurisdiction").value;
    pay.currency = $("payCurrency").value;
    pay.period = $("payPeriod").value;
    pay.min = $("payMin").value;
    pay.max = $("payMax").value;
    savePay();
    renderPayNotice();
    if (state.currentDraft) state.draftOutdated = true;
    renderDraft();
  }

  // Asked before copy/export when the place requires pay and the draft has none.
  features.confirmExport = function () {
    if (!payRequired() || !state.currentDraft) return true;
    const draft = state.currentDraft;
    const benefits = (draft.benefits || []).join(" ").toLowerCase();
    const hasPay = Boolean(draft.pay_range) || /\$|salary|compensation|per hour|per year/.test(benefits);
    if (hasPay) return true;
    return window.confirm(
      "Your selected location usually requires a pay range in job posts, and this draft has none.\n\nCopy or export anyway?"
    );
  };

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

  // Called by app.js after a generate or refine finished.
  features.applyDraftResult = function (data, label) {
    state.currentDraft = data.draft;
    state.currentMarkdown = data.markdown;
    state.quality = data.quality || null;
    saveDraftToStorage();
    pushVersion(label);
    renderDraft();
  };

  // ---------- rendering after each draft render ----------

  features.afterRenderDraft = function () {
    renderQuality();
    renderVersionBar();
    renderChangeNote();
    decoratePreview();
    updateEditControls();
    updateRefineButton();
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

    // Flag requirements the user did not provide.
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
    const fixes = new Set();
    const items = findings
      .map((finding) => {
        const fixAction = FIX_BY_FINDING[finding.code];
        if (fixAction) fixes.add(fixAction);
        const matches = (finding.matches || []).slice(0, 6).map((m) => `<code>${escapeHtml(m)}</code>`).join(" ");
        return `<li class="q-item q-${finding.severity}">
          <span class="q-badge">${escapeHtml(finding.severity)}</span>
          <span><span class="q-msg">${escapeHtml(finding.message)}</span>
          ${finding.suggestion ? `<span class="q-tip">${escapeHtml(finding.suggestion)}</span>` : ""}
          ${matches ? `<span class="q-matches">${matches}</span>` : ""}</span>
        </li>`;
      })
      .join("");
    const fixButtons = [...fixes]
      .map((action) => `<button type="button" class="chip chip-small" data-action="${action}">Fix: ${escapeHtml(ACTION_LABELS[action])}</button>`)
      .join("");
    panel.innerHTML = `
      <details ${findings.length ? "open" : ""}>
        <summary>
          <span class="q-score ${scoreClass(report.score)}">${report.score}</span>
          <span class="q-title"><strong>Quality check</strong>
            <small>${findings.length ? `${findings.length} thing${findings.length === 1 ? "" : "s"} to look at` : "Looks good"} - free, rule-based, no AI used</small></span>
        </summary>
        ${items ? `<ul class="q-list">${items}</ul>` : ""}
        ${fixButtons ? `<div class="q-fixes">One-click fixes (free): ${fixButtons}</div>` : ""}
        <p class="q-stats">${stats.word_count || 0} words - reading grade ${stats.reading_grade || 0} - ${stats.responsibilities || 0} responsibilities - ${stats.requirements || 0} requirements</p>
      </details>`;
  }

  // ---------- free edits: chips + section rewrite ----------

  function updateEditControls() {
    const disabled = busy || !state.currentDraft || state.draftOutdated;
    document.querySelectorAll("#chipRow .chip, .q-fixes .chip, .section-rewrite-btn").forEach((button) => {
      button.disabled = disabled;
    });
  }

  async function runFreeEdit(path, extra, label, eventName, eventDetail) {
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
      features.applyDraftResult(data, label);
      setMessage("");
      logEvent(eventName, eventDetail);
    } catch (error) {
      setMessage(error.message);
    } finally {
      busy = false;
      renderDraft();
    }
  }

  function onChipClick(event) {
    const chip = event.target.closest(".chip[data-action]");
    if (!chip || chip.disabled) return;
    const action = chip.dataset.action;
    runFreeEdit("/quick-edit", { action }, ACTION_LABELS[action] || action, "quick_action", action);
  }

  function onPreviewClick(event) {
    const button = event.target.closest(".section-rewrite-btn");
    if (!button || button.disabled) return;
    const section = button.dataset.section;
    runFreeEdit("/regenerate-section", { section }, `Rewrote ${section.replaceAll("_", " ")}`, "section_regen", section);
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
      <details open>
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

  // ---------- credits, packs, paywall resume ----------

  function updateRefineButton() {
    const button = elements.refineButton;
    if (!button || button.textContent.startsWith("Refining")) return;
    const free = (state.config && state.config.free_signup_credits) || 20;
    const credits = state.credits ?? 0;
    if (!state.accessToken) button.textContent = `Refine - sign in free (${free} credits)`;
    else if (credits < 1) button.textContent = "Refine - buy credits";
    else button.textContent = `Refine - 1 credit (${credits} left)`;
  }

  features.onAuthChanged = updateRefineButton;

  features.renderPacks = function () {
    const list = $("packList");
    if (!list || !state.config) return;
    list.innerHTML = state.config.packs
      .map((pack) => {
        const dollars = pack.price_cents / 100;
        const each = (dollars / pack.credits).toFixed(2);
        const popular = pack.pack_id === "standard";
        return `<button type="button" class="pack-card${popular ? " pack-popular" : ""}" data-pack="${escapeHtml(pack.pack_id)}">
          ${popular ? '<span class="pack-flag">Most popular</span>' : ""}
          <span class="pack-credits">${pack.credits}</span>
          <span class="pack-unit">refines</span>
          <span class="pack-price">$${dollars}</span>
          <span class="pack-each">$${each} each</span>
        </button>`;
      })
      .join("");
  };

  function onPackClick(event) {
    const card = event.target.closest(".pack-card");
    if (card) payCredits(card.dataset.pack, card);
  }

  features.savePendingRefine = function (text) {
    safeStorage(() => localStorage.setItem(PENDING_KEY, JSON.stringify({ text, at: Date.now() })));
  };

  features.clearPendingRefine = function () {
    safeStorage(() => localStorage.removeItem(PENDING_KEY));
  };

  // After sign-in or payment, run the refine the user already asked for.
  features.resumePendingRefine = function () {
    const raw = safeStorage(() => localStorage.getItem(PENDING_KEY));
    if (!raw) return;
    let pending;
    try {
      pending = JSON.parse(raw);
    } catch {
      return features.clearPendingRefine();
    }
    if (!pending.text || Date.now() - pending.at > PENDING_MAX_AGE_MS) return features.clearPendingRefine();
    if (!state.accessToken || !state.currentDraft || state.draftOutdated) return;
    if ((state.credits ?? 0) < 1) {
      setMessage("You are signed in but have no credits left. Pick a pack and your request will run automatically.", "info");
      return openBillingModal();
    }
    elements.refineInput.value = pending.text;
    setMessage("Running the refine you asked for...", "info");
    refineDraft();
  };

  async function handleCheckoutReturn() {
    const params = new URLSearchParams(window.location.search);
    const sessionId = params.get("session_id");
    if (!sessionId) return;
    params.delete("session_id");
    const query = params.toString();
    window.history.replaceState(null, "", window.location.pathname + (query ? `?${query}` : "") + window.location.hash);
    if (!state.accessToken) return;
    try {
      const result = await callApi(`/confirm-checkout?session_id=${encodeURIComponent(sessionId)}`, {});
      state.credits = result.credits;
      renderAuth();
      updateRefineButton();
      closeBillingModal();
      setMessage(`Payment received. You now have ${result.credits} refine credits.`, "info");
      features.resumePendingRefine();
    } catch {
      setMessage("Payment is still processing. Your credits will appear in a moment. Refresh the page to check.", "info");
    }
  }

  // ---------- workspace reset ----------

  features.onWorkspaceCleared = function () {
    versions = [];
    versionIndex = -1;
    state.quality = null;
    originalDoc = { text: "", name: "" };
    persistVersions();
    features.clearPendingRefine();
    ["diffPanel", "screeningList", "changeNote"].forEach((id) => {
      const node = $(id);
      if (node) node.classList.add("hidden");
    });
  };

  // ---------- init ----------

  function bind() {
    ["payJurisdiction", "payCurrency", "payPeriod", "payMin", "payMax"].forEach((id) => {
      const node = $(id);
      if (!node) return;
      node.addEventListener(node.tagName === "SELECT" ? "change" : "input", onPayChanged);
    });
    $("chipRow")?.addEventListener("click", onChipClick);
    $("qualityPanel")?.addEventListener("click", onChipClick);
    $("markdownPreview")?.addEventListener("click", onPreviewClick);
    $("undoBtn")?.addEventListener("click", () => goToVersion(versionIndex - 1));
    $("redoBtn")?.addEventListener("click", () => goToVersion(versionIndex + 1));
    $("highlightToggle")?.addEventListener("change", (event) => {
      highlightChanges = event.target.checked;
      renderDraft();
    });
    $("screeningBtn")?.addEventListener("click", onScreeningClick);
    $("packList")?.addEventListener("click", onPackClick);
  }

  function init() {
    loadPay();
    loadVersions();
    syncPayInputs();
    bind();
    if (state.currentDraft && !versions.length) {
      versions = [{ label: "Restored draft", draft: state.currentDraft, markdown: state.currentMarkdown, quality: null, at: Date.now() }];
      versionIndex = 0;
    } else if (versions[versionIndex]) {
      state.quality = versions[versionIndex].quality;
    }
    renderPayNotice();
    renderDraft();
    loadConfig().then(() => handleCheckoutReturn());
  }

  init();
})();
