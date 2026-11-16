"use strict";

// Small polish only: scroll reveal, score count-up, streaming caret, mobile bar.
// If this file fails or the visitor prefers reduced motion, everything stays visible.
(function () {
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const REVEAL_SELECTORS = [".pricing-inner", ".faq-section", ".app-footer"];
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
      { rootMargin: "0px 0px -8% 0px", threshold: 0.05 }
    );
    targets.forEach((node) => {
      node.classList.add("reveal");
      observer.observe(node);
    });

    // Safety net: never leave content hidden if the observer does not fire.
    window.setTimeout(() => {
      document.querySelectorAll(".reveal:not(.in)").forEach((node) => {
        if (node.getBoundingClientRect().top < window.innerHeight) node.classList.add("in");
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

  // The quality score counts up each time it is drawn.
  function setupScores() {
    const panel = document.getElementById("qualityPanel");
    if (!panel) return;
    new MutationObserver(() => {
      const score = panel.querySelector(".q-score");
      if (!score || score.dataset.counted === "1") return;
      score.dataset.counted = "1";
      const value = Number(score.textContent);
      if (Number.isFinite(value)) countUp(score, value);
    }).observe(panel, { childList: true, subtree: true });
  }

  // Blinking caret while raw model text streams into the sheet.
  function setupStreamingCaret() {
    const preview = document.getElementById("markdownPreview");
    if (!preview) return;
    new MutationObserver(() => {
      const raw = !preview.querySelector("h2, ul, .doc-title") && preview.textContent.trim().startsWith("{");
      preview.classList.toggle("streaming", raw);
    }).observe(preview, { childList: true, characterData: true, subtree: true });
  }

  // Mobile bar: Generate while composing, Copy and Word once a draft exists.
  function setupMobileBar() {
    const generate = document.getElementById("generateButton");
    const mobileGenerate = document.getElementById("mobileGenerate");
    if (mobileGenerate && generate) {
      mobileGenerate.addEventListener("click", () => generate.click());
      const mirror = () => {
        mobileGenerate.disabled = generate.disabled;
        mobileGenerate.textContent = generate.disabled ? generate.textContent : "Generate (free)";
      };
      new MutationObserver(mirror).observe(generate, { attributes: true, childList: true, characterData: true, subtree: true });
      generate.addEventListener("click", () => {
        if (window.innerWidth < 900) {
          window.setTimeout(() => document.getElementById("paneResult")?.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" }), 250);
        }
      });
    }
    document.getElementById("mobileCopy")?.addEventListener("click", () => document.getElementById("copyButton")?.click());
    document.getElementById("mobileWord")?.addEventListener("click", () => document.getElementById("exportDocxButton")?.click());
  }

  try {
    setupMobileBar();
    setupReveal();
    setupScores();
    setupStreamingCaret();
  } catch (error) {
    console.warn("Motion polish skipped:", error);
  }
})();
