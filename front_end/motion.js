"use strict";

// Scroll reveal, score count-up and streaming caret. Pure polish: if this file
// fails or the visitor prefers reduced motion, everything stays visible.
(function () {
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const REVEAL_SELECTORS = [
    ".pricing-card",
    ".seo-header",
    ".seo-step-card",
    ".seo-faq-item",
    ".footer-grid",
    ".pay-card",
    ".sample-card",
  ];
  const COUNT_MS = 700;

  function setupReveal() {
    if (reduceMotion || !("IntersectionObserver" in window)) return;
    const targets = document.querySelectorAll(REVEAL_SELECTORS.join(","));
    if (!targets.length) return;
    document.documentElement.classList.add("js-motion");

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("in");
          observer.unobserve(entry.target);
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.08 }
    );

    targets.forEach((node, index) => {
      node.classList.add("reveal");
      // Stagger siblings that appear together (cards in a row).
      node.style.setProperty("--reveal-delay", `${(index % 4) * 70}ms`);
      observer.observe(node);
    });

    // Safety net: never leave content hidden if the observer does not fire.
    window.setTimeout(() => {
      document.querySelectorAll(".reveal:not(.in)").forEach((node) => {
        const box = node.getBoundingClientRect();
        if (box.top < window.innerHeight) node.classList.add("in");
      });
    }, 1500);
  }

  function countUp(node, target) {
    if (reduceMotion) return;
    const start = performance.now();
    function frame(now) {
      const progress = Math.min((now - start) / COUNT_MS, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      node.textContent = String(Math.round(target * eased));
      if (progress < 1) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }

  // Animate the hero sample score once, and the quality score each time it renders.
  function setupScores() {
    document.querySelectorAll("[data-count-to]").forEach((node) => {
      countUp(node, Number(node.dataset.countTo));
    });
    const panel = document.getElementById("qualityPanel");
    if (!panel) return;
    let last = "";
    new MutationObserver(() => {
      const score = panel.querySelector(".q-score");
      if (!score || score.dataset.counted === "1") return;
      score.dataset.counted = "1";
      const value = Number(score.textContent);
      if (!Number.isFinite(value) || String(value) === last) return;
      last = String(value);
      countUp(score, value);
    }).observe(panel, { childList: true, subtree: true });
  }

  // Mark the preview as "streaming" while raw model text is shown.
  function setupStreamingCaret() {
    const preview = document.getElementById("markdownPreview");
    if (!preview) return;
    new MutationObserver(() => {
      const raw = !preview.querySelector("h1, h2, ul") && preview.textContent.trim().startsWith("{");
      const starting = Boolean(preview.querySelector(".streaming-indicator"));
      preview.classList.toggle("streaming", raw && !starting);
    }).observe(preview, { childList: true, characterData: true, subtree: true });
  }

  // On narrow screens the draft sits below the form: bring it into view when ready.
  function setupScrollToDraft() {
    const preview = document.getElementById("markdownPreview");
    const column = document.querySelector(".result-column");
    if (!preview || !column) return;
    new MutationObserver(() => {
      if (window.innerWidth >= 1000 || reduceMotion) return;
      if (preview.classList.contains("streaming")) return;
    }).observe(preview, { attributes: true, attributeFilter: ["class"] });
    document.getElementById("generateButton")?.addEventListener("click", () => {
      if (window.innerWidth < 1000) {
        window.setTimeout(() => column.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" }), 250);
      }
    });
  }

  try {
    setupReveal();
    setupScores();
    setupStreamingCaret();
    setupScrollToDraft();
  } catch (error) {
    console.warn("Motion polish skipped:", error);
  }
})();
