const API_BASE_URL = "http://127.0.0.1:8000";
const PROVIDER = "openai";
const MODEL = "gpt-5.5";
const RAIL_PIN_STORAGE_KEY = "linkedinJobGeneratorRailPinned";

const fallbackQuestions = [
  { question_name: "company_name", question_text: "What is your company name?", required: true, answer_type: "text" },
  { question_name: "role_title", question_text: "What role are you hiring for?", required: true, answer_type: "text" },
  { question_name: "role_summary", question_text: "Why is the company hiring this role, and what should this person help accomplish?", required: true, answer_type: "text" },
  { question_name: "responsibilities", question_text: "What will this person be responsible for?", required: true, answer_type: "list" },
  { question_name: "requirements", question_text: "What skills, experience, or qualifications are required?", required: true, answer_type: "list" },
  { question_name: "nice_to_haves", question_text: "What skills or experience would be nice to have, but not required?", required: false, answer_type: "list" },
  { question_name: "salary_range", question_text: "What salary range do you want to include?", required: false, answer_type: "text" },
  { question_name: "company_description", question_text: "How would you describe the company in a few sentences?", required: false, answer_type: "text" },
  { question_name: "why_join_us", question_text: "Why should candidates be excited to join this company or team?", required: false, answer_type: "text" },
  { question_name: "benefits", question_text: "Are there any benefits, perks, or compensation details to include?", required: false, answer_type: "list" },
  { question_name: "tone", question_text: "What tone do you want the job description to sound?", required: false, answer_type: "text" },
  { question_name: "target_length", question_text: "How long should the job description be: short, medium, or long?", required: false, answer_type: "text" },
  { question_name: "equal_opportunity", question_text: "Do you want to include an equal opportunity statement?", required: false, answer_type: "text" },
];

const sampleAnswers = {
  company_name: "Northstar Labs",
  role_title: "Product Manager",
  role_summary: "Lead planning and delivery for a growing hiring platform used by small recruiting teams.",
  responsibilities: "Define product requirements\nCoordinate design and engineering work\nReview product metrics and user feedback",
  requirements: "Product management experience\nStrong written communication\nComfort working with cross-functional teams",
  tone: "professional",
  target_length: "long",
};

const fieldsAcceptedByApi = new Set([
  "company_name",
  "role_title",
  "role_summary",
  "responsibilities",
  "requirements",
  "company_description",
  "nice_to_haves",
  "benefits",
  "why_join_us",
  "equal_opportunity",
  "tone",
  "target_length",
]);

const state = {
  questions: [],
  answers: {},
  openQuestion: null,
  missingRequired: new Set(),
  currentDraft: null,
  currentMarkdown: "",
  draftOutdated: false,
  railPinned: localStorage.getItem(RAIL_PIN_STORAGE_KEY) === "true",
};

const elements = {
  apiStatus: document.querySelector("#apiStatus"),
  progressText: document.querySelector("#progressText"),
  questionRail: document.querySelector("#questionRail"),
  railToggle: document.querySelector("#railToggle"),
  questionList: document.querySelector("#questionList"),
  sampleButton: document.querySelector("#sampleButton"),
  generateButton: document.querySelector("#generateButton"),
  draftWarning: document.querySelector("#draftWarning"),
  messageBox: document.querySelector("#messageBox"),
  markdownPreview: document.querySelector("#markdownPreview"),
  copyButton: document.querySelector("#copyButton"),
  exportDocxButton: document.querySelector("#exportDocxButton"),
  refineInput: document.querySelector("#refineInput"),
  refineButton: document.querySelector("#refineButton"),
};

function apiUrl(path) {
  return `${API_BASE_URL}${path}`;
}

function parseList(value) {
  return value.split(/\n|,/).map((item) => item.trim()).filter(Boolean);
}

function formatFieldName(name) {
  return name.replaceAll("_", " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function setMessage(text = "", type = "error") {
  elements.messageBox.textContent = text;
  elements.messageBox.classList.toggle("hidden", !text);
  elements.messageBox.classList.toggle("info", type === "info");
}

function updateAnswer(field, value) {
  state.answers[field] = value;
  if (value.trim()) state.missingRequired.delete(field);
  if (state.currentDraft) state.draftOutdated = true;
  renderProgress();
  renderDraft();
  renderQuestionStatus(field);
}

function getSkippedFields() {
  return state.questions
    .filter((question) => !question.required && !state.answers[question.question_name]?.trim())
    .map((question) => question.question_name);
}

function buildJobInfo() {
  const jobInfo = {
    company_name: "",
    role_title: "",
    role_summary: "",
    responsibilities: [],
    requirements: [],
    company_description: null,
    nice_to_haves: [],
    benefits: [],
    why_join_us: "",
    equal_opportunity: "",
    tone: "professional",
    target_length: "medium",
  };

  for (const question of state.questions) {
    const field = question.question_name;
    const rawValue = state.answers[field]?.trim();
    if (!fieldsAcceptedByApi.has(field) || !rawValue) continue;
    jobInfo[field] = question.answer_type === "list" ? parseList(rawValue) : rawValue;
  }

  return jobInfo;
}

function renderQuestions() {
  elements.questionList.innerHTML = "";
  elements.questionRail.innerHTML = "";

  for (const [index, question] of state.questions.entries()) {
    const isOpen = state.openQuestion === question.question_name;
    const value = state.answers[question.question_name] || "";
    const isMissing = state.missingRequired.has(question.question_name);
    const isAnswered = Boolean(value.trim());

    const railButton = document.createElement("button");
    railButton.className = `rail-button${isOpen ? " active" : ""}${isMissing ? " missing" : ""}${isAnswered ? " answered" : ""}`;
    railButton.type = "button";
    railButton.textContent = String(index + 1).padStart(2, "0");
    railButton.setAttribute("aria-label", `Go to question ${index + 1}: ${formatFieldName(question.question_name)}`);
    railButton.addEventListener("click", () => {
      state.openQuestion = question.question_name;
      renderQuestions();
      const target = document.querySelector(`[data-field="${question.question_name}"]`);
      target?.scrollIntoView({ behavior: "smooth", block: "center" });
      const nextInput = document.querySelector(`[data-field="${question.question_name}"] textarea`);
      if (nextInput) setTimeout(() => nextInput.focus(), 260);
    });
    elements.questionRail.append(railButton);

    const card = document.createElement("section");
    card.className = `question-card${isOpen ? " open" : ""}${isMissing ? " missing" : ""}${isAnswered ? " answered" : ""}`;
    card.dataset.field = question.question_name;

    const summary = document.createElement("button");
    summary.className = "question-summary";
    summary.type = "button";
    summary.setAttribute("aria-expanded", String(isOpen));
    summary.addEventListener("click", () => {
      state.openQuestion = isOpen ? null : question.question_name;
      renderQuestions();
      const nextInput = document.querySelector(`[data-field="${question.question_name}"] textarea`);
      if (!isOpen && nextInput) setTimeout(() => nextInput.focus(), 210);
    });

    const number = document.createElement("span");
    number.className = "question-number";
    number.textContent = String(index + 1).padStart(2, "0");

    const title = document.createElement("span");
    title.className = "question-title";
    const titleStrong = document.createElement("strong");
    titleStrong.textContent = formatFieldName(question.question_name);
    const titleMeta = document.createElement("span");
    titleMeta.className = "question-meta";
    titleMeta.textContent = questionMetaText(question, value, isMissing);
    title.append(titleStrong, titleMeta);

    const expand = document.createElement("span");
    expand.className = "expand-label";
    expand.textContent = isOpen ? "Close" : "Expand";

    summary.append(number, title, expand);

    const body = document.createElement("div");
    body.className = "question-body";
    const bodyInner = document.createElement("div");
    bodyInner.className = "question-body-inner";
    const prompt = document.createElement("p");
    prompt.textContent = question.question_text;
    const input = document.createElement("textarea");
    input.value = value;
    input.rows = question.answer_type === "list" ? 5 : 4;
    input.placeholder = question.answer_type === "list" ? "Add one item per line." : "Type your answer.";
    input.addEventListener("input", (event) => updateAnswer(question.question_name, event.target.value));

    const hint = document.createElement("div");
    hint.className = "hint-row";
    const leftHint = document.createElement("span");
    leftHint.textContent = question.answer_type === "list" ? "Use separate lines for multiple items." : "Answer before generating.";
    const rightHint = document.createElement("span");
    rightHint.textContent = question.required ? "Required" : "Optional";
    hint.append(leftHint, rightHint);

    bodyInner.append(prompt, input, hint);
    body.append(bodyInner);
    card.append(summary, body);
    elements.questionList.append(card);
  }
}

function renderRailPin() {
  document.body.classList.toggle("rail-pinned", state.railPinned);
  elements.railToggle.setAttribute("aria-pressed", String(state.railPinned));
  elements.railToggle.title = state.railPinned ? "Hide question numbers until hover" : "Keep question numbers visible";
  const label = elements.railToggle.querySelector(".rail-toggle-text");
  if (label) label.textContent = state.railPinned ? "Auto hide" : "Keep open";
}

function questionMetaText(question, value, isMissing) {
  if (isMissing) return "Required answer missing";
  if (value.trim()) return "Answered";
  return question.required ? "Required" : "Optional";
}

function renderQuestionStatus(field) {
  const question = state.questions.find((item) => item.question_name === field);
  const card = document.querySelector(`[data-field="${field}"]`);
  if (!question || !card) return;
  const value = state.answers[field] || "";
  const isMissing = state.missingRequired.has(field);
  card.classList.toggle("missing", isMissing);
  card.classList.toggle("answered", Boolean(value.trim()));
  const meta = card.querySelector(".question-meta");
  if (meta) meta.textContent = questionMetaText(question, value, isMissing);
  const questionIndex = state.questions.findIndex((item) => item.question_name === field);
  const railButton = elements.questionRail.children[questionIndex];
  if (railButton) {
    railButton.classList.toggle("missing", isMissing);
    railButton.classList.toggle("answered", Boolean(value.trim()));
  }
}

function renderProgress() {
  const answeredCount = state.questions.filter((question) => state.answers[question.question_name]?.trim()).length;
  elements.progressText.textContent = `${answeredCount} answered`;
}

function renderDraft() {
  elements.draftWarning.classList.toggle("hidden", !state.draftOutdated);
  elements.refineButton.disabled = !state.currentDraft || state.draftOutdated;
  elements.copyButton.disabled = !state.currentMarkdown;
  elements.exportDocxButton.disabled = !state.currentMarkdown;

  if (!state.currentMarkdown) {
    elements.markdownPreview.classList.add("empty");
    elements.markdownPreview.textContent = "Generate a draft to preview the job description.";
    return;
  }

  elements.markdownPreview.classList.remove("empty");
  elements.markdownPreview.innerHTML = markdownToHtml(state.currentMarkdown);
}

function renderAll() {
  renderQuestions();
  renderProgress();
  renderDraft();
}

function missingRequiredFields() {
  return state.questions
    .filter((question) => question.required && !state.answers[question.question_name]?.trim())
    .map((question) => question.question_name);
}

function setLoading(button, loadingText) {
  const originalText = button.textContent;
  button.textContent = loadingText;
  button.disabled = true;
  return () => {
    button.textContent = originalText;
    button.disabled = false;
    renderDraft();
  };
}

async function callApi(path, payload) {
  const response = await fetch(apiUrl(path), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  const contentType = response.headers.get("content-type") || "";
  const data = contentType.includes("application/json") ? await response.json() : await response.text();

  if (!response.ok) {
    const detail = typeof data === "string" ? data : data.detail || JSON.stringify(data, null, 2);
    throw new Error(detail);
  }
  return data;
}

async function generateDraft() {
  const missing = missingRequiredFields();
  if (missing.length) {
    state.missingRequired = new Set(missing);
    state.openQuestion = missing[0];
    renderAll();
    setMessage(`Please answer the required questions before generating: ${missing.map(formatFieldName).join(", ")}`);
    const firstMissing = document.querySelector(`[data-field="${missing[0]}"]`);
    firstMissing?.scrollIntoView({ behavior: "smooth", block: "center" });
    return;
  }

  state.missingRequired.clear();
  renderQuestions();
  const restore = setLoading(elements.generateButton, "Generating");
  setMessage("Generating your draft. This can take a moment.", "info");
  try {
    const data = await callApi("/generate", {
      job_info: buildJobInfo(),
      skipped_fields: getSkippedFields(),
      provider: PROVIDER,
      model: MODEL,
    });
    state.currentDraft = data.draft;
    state.currentMarkdown = data.markdown;
    state.draftOutdated = false;
    setMessage("");
  } catch (error) {
    setMessage(error.message);
  } finally {
    restore();
  }
}

async function refineDraft() {
  const request = elements.refineInput.value.trim();
  if (!state.currentDraft) {
    setMessage("Generate a draft before refining.");
    return;
  }
  if (state.draftOutdated) {
    setMessage("Regenerate before refining because the answers have changed.");
    return;
  }
  if (!request) {
    setMessage("Add a refinement request first.");
    return;
  }

  const restore = setLoading(elements.refineButton, "Refining");
  setMessage("Refining your draft. This can take a moment.", "info");
  try {
    const data = await callApi("/refine", {
      job_info: buildJobInfo(),
      current_draft: state.currentDraft,
      user_request: request,
      skipped_fields: getSkippedFields(),
      provider: PROVIDER,
      model: MODEL,
    });
    state.currentDraft = data.draft;
    state.currentMarkdown = data.markdown;
    elements.refineInput.value = "";
    setMessage("");
  } catch (error) {
    setMessage(error.message);
  } finally {
    restore();
  }
}

function markdownToHtml(markdown) {
  const lines = markdown.split("\n");
  const html = [];
  let inList = false;

  for (const rawLine of lines) {
    const line = rawLine.trim();
    if (!line) {
      if (inList) {
        html.push("</ul>");
        inList = false;
      }
      continue;
    }
    if (line.startsWith("### ")) {
      if (inList) html.push("</ul>");
      inList = false;
      html.push(`<h3>${escapeHtml(line.slice(4))}</h3>`);
    } else if (line.startsWith("## ")) {
      if (inList) html.push("</ul>");
      inList = false;
      html.push(`<h2>${escapeHtml(line.slice(3))}</h2>`);
    } else if (line.startsWith("# ")) {
      if (inList) html.push("</ul>");
      inList = false;
      html.push(`<h1>${escapeHtml(line.slice(2))}</h1>`);
    } else if (line.startsWith("- ") || line.startsWith("* ")) {
      if (!inList) {
        html.push("<ul>");
        inList = true;
      }
      html.push(`<li>${escapeHtml(line.slice(2))}</li>`);
    } else {
      if (inList) {
        html.push("</ul>");
        inList = false;
      }
      html.push(`<p>${escapeHtml(line)}</p>`);
    }
  }

  if (inList) html.push("</ul>");
  return html.join("");
}

function cleanPreviewText() {
  return elements.markdownPreview.innerText.replace(/\n{3,}/g, "\n\n").trim();
}

function stripInlineMarkdown(value) {
  return value
    .replace(/\*\*(.*?)\*\*/g, "$1")
    .replace(/\*(.*?)\*/g, "$1")
    .replace(/`(.*?)`/g, "$1")
    .trim();
}

function fileSafeName(value) {
  return value
    .replace(/[<>:"/\\|?*]+/g, "")
    .replace(/\s+/g, "_")
    .replace(/^_+|_+$/g, "")
    .slice(0, 80) || "Generated_Job_Description";
}

function docxParagraphsFromMarkdown(markdown) {
  const { HeadingLevel, Paragraph, TextRun } = window.docx;
  const paragraphs = [];

  for (const rawLine of markdown.split("\n")) {
    const line = rawLine.trim();
    if (!line) {
      paragraphs.push(new Paragraph({ text: "", spacing: { after: 120 } }));
      continue;
    }

    if (line.startsWith("# ")) {
      paragraphs.push(new Paragraph({
        text: stripInlineMarkdown(line.slice(2)),
        heading: HeadingLevel.HEADING_1,
        spacing: { after: 180 },
      }));
      continue;
    }

    if (line.startsWith("## ")) {
      paragraphs.push(new Paragraph({
        text: stripInlineMarkdown(line.slice(3)),
        heading: HeadingLevel.HEADING_2,
        spacing: { before: 220, after: 120 },
      }));
      continue;
    }

    if (line.startsWith("### ")) {
      paragraphs.push(new Paragraph({
        text: stripInlineMarkdown(line.slice(4)),
        heading: HeadingLevel.HEADING_3,
        spacing: { before: 160, after: 80 },
      }));
      continue;
    }

    if (line.startsWith("- ") || line.startsWith("* ")) {
      paragraphs.push(new Paragraph({
        children: [new TextRun(stripInlineMarkdown(line.slice(2)))],
        bullet: { level: 0 },
        spacing: { after: 80 },
      }));
      continue;
    }

    paragraphs.push(new Paragraph({
      children: [new TextRun(stripInlineMarkdown(line))],
      spacing: { after: 120 },
    }));
  }

  return paragraphs;
}

async function exportDocx() {
  if (!state.currentMarkdown) return;
  if (!window.docx) {
    setMessage("DOCX export library did not load. Check your internet connection and try again.");
    return;
  }

  const { Document, Packer } = window.docx;
  const roleTitle = state.answers.role_title?.trim() || "Generated";
  const fileName = `${fileSafeName(roleTitle)}_Job_Description.docx`;
  const doc = new Document({
    creator: "LinkedIn Job Description Generator",
    title: `${roleTitle} Job Description`,
    sections: [{
      properties: {},
      children: docxParagraphsFromMarkdown(state.currentMarkdown),
    }],
  });

  const blob = await Packer.toBlob(doc);
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = fileName;
  document.body.append(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
  setMessage("DOCX downloaded.", "info");
}

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

async function checkApi() {
  try {
    const health = await fetch(apiUrl("/health")).then((response) => response.json());
    elements.apiStatus.textContent = health.status === "ok" ? "Service online" : "Service check failed";
    elements.apiStatus.classList.toggle("ok", health.status === "ok");
    elements.apiStatus.classList.toggle("fail", health.status !== "ok");
  } catch {
    elements.apiStatus.textContent = "Service offline";
    elements.apiStatus.classList.add("fail");
  }
}

async function loadQuestions() {
  try {
    const response = await fetch(apiUrl("/questions"));
    if (!response.ok) throw new Error("Could not load questions");
    state.questions = await response.json();
  } catch {
    state.questions = fallbackQuestions;
    setMessage("");
  }
  state.openQuestion = state.questions[0]?.question_name || null;
  renderAll();
}

function loadSample() {
  state.answers = { ...sampleAnswers };
  state.missingRequired.clear();
  state.openQuestion = null;
  if (state.currentDraft) state.draftOutdated = true;
  renderAll();
}

elements.sampleButton.addEventListener("click", loadSample);
elements.railToggle.addEventListener("click", () => {
  state.railPinned = !state.railPinned;
  localStorage.setItem(RAIL_PIN_STORAGE_KEY, String(state.railPinned));
  renderRailPin();
});
elements.generateButton.addEventListener("click", generateDraft);
elements.refineButton.addEventListener("click", refineDraft);
elements.copyButton.addEventListener("click", async () => {
  const textToCopy = cleanPreviewText();
  if (!state.currentMarkdown || !textToCopy) return;
  await navigator.clipboard.writeText(textToCopy);
  setMessage("Job description copied.", "info");
});
elements.exportDocxButton.addEventListener("click", exportDocx);

checkApi();
renderRailPin();
loadQuestions();
