const API_BASE_URL = "https://linkedin-job-generator-api.onrender.com/";
// const API_BASE_URL = "http://127.0.0.1:8000";
const RAIL_PIN_STORAGE_KEY = "linkedinJobGeneratorRailPinned";
const AUTH_TOKEN_STORAGE_KEY = "linkedinJobGeneratorAccessToken";

const fallbackQuestions = [
  { question_name: "company_name", question_text: "What is your company name?", required: true, answer_type: "text" },
  { question_name: "role_title", question_text: "What role are you hiring for?", required: true, answer_type: "text" },
  { question_name: "role_summary", question_text: "Why is the company hiring this role, and what should this person help accomplish?", required: true, answer_type: "text" },
  { question_name: "responsibilities", question_text: "What will this person be responsible for?", required: true, answer_type: "list" },
  { question_name: "requirements", question_text: "What skills, experience, or qualifications are required?", required: true, answer_type: "list" },
  { question_name: "nice_to_haves", question_text: "What skills or experience would be nice to have, but not required?", required: false, answer_type: "list" },
  { question_name: "company_description", question_text: "How would you describe the company in a few sentences?", required: false, answer_type: "text" },
  { question_name: "why_join_us", question_text: "Why should candidates be excited to join this company or team?", required: false, answer_type: "text" },
  { question_name: "benefits", question_text: "Are there any benefits, perks, or compensation details to include?", required: false, answer_type: "list" },
  { question_name: "tone", question_text: "What tone do you want the job description to sound?", required: false, answer_type: "text" },
  { question_name: "target_length", question_text: "How long should the job description be: short, medium, or long?", required: false, answer_type: "text" },
  { question_name: "equal_opportunity", question_text: "Do you want to include an equal opportunity statement?", required: false, answer_type: "text" },
];

const sampleAnswers = {
  company_name: "Alex AI",
  role_title: "AI Engineer Intern",
  role_summary: "Help build, monitor, and evaluate AI systems that generate high-quality LinkedIn job descriptions.",
  responsibilities: "Monitor machine learning pipelines\nEvaluate model output quality\n Prepare and clean training data\n Support prompt testing and model comparison",
  requirements: "Python\n SQL\n Basic machine learning knowledge\n Experience working with data pipelines",
  company_description: "Alex AI is a startup building tools that help companies create better hiring content using AI.",
  nice_to_haves:  "System design\nFigma\n Frontend development\nSignal processing",
  benefits:"Health insurance\nLunch\nbreakfast\nand covered \nHands-on AI engineering experience",
  why_join_us: "Join a fast-moving startup where interns can work on real AI systems, learn quickly, and have visible impact.",
  equal_opportunity: "yes",
  tone: "enthusiastic, startup-like, and professional",
  target_length: "long",
};

const sampleDraft = {
  title: "Product Manager",
  about_company: "Northstar Labs builds practical hiring tools for small recruiting teams that need clearer workflows, better candidate communication, and faster role planning.",
  about_role: "The Product Manager will lead planning and delivery for a growing hiring platform. This person will work closely with design, engineering, and customer-facing teams to turn recruiter feedback into focused product improvements.",
  responsibilities: [
    "Define product requirements, priorities, and success metrics for new hiring workflow features.",
    "Coordinate design and engineering work from discovery through launch.",
    "Review product analytics, customer feedback, and user research to identify practical improvements.",
    "Partner with stakeholders to keep releases focused, useful, and aligned with business goals.",
  ],
  requirements: [
    "Experience managing software products from planning through delivery.",
    "Strong written communication and comfort turning ambiguity into clear product direction.",
    "Ability to work with cross-functional teams across design, engineering, and go-to-market.",
    "Comfort using product metrics and qualitative feedback to make decisions.",
  ],
  nice_to_haves: [
    "Experience with recruiting, HR technology, or workflow automation products.",
    "Familiarity with B2B SaaS product development.",
  ],
  benefits: [
    "Flexible remote-friendly work culture.",
    "Health, dental, and vision coverage.",
    "Learning budget for courses, books, and conferences.",
  ],
  why_join_us: "This is a chance to shape a product that helps lean recruiting teams write better roles, move faster, and create a more thoughtful candidate experience.",
  equal_opportunity: "Northstar Labs is an equal opportunity employer and welcomes applicants from all backgrounds.",
};

const sampleMarkdown = `# Product Manager

## About Northstar Labs
Northstar Labs builds practical hiring tools for small recruiting teams that need clearer workflows, better candidate communication, and faster role planning.

## About the Role
The Product Manager will lead planning and delivery for a growing hiring platform. This person will work closely with design, engineering, and customer-facing teams to turn recruiter feedback into focused product improvements.

## Responsibilities
- Define product requirements, priorities, and success metrics for new hiring workflow features.
- Coordinate design and engineering work from discovery through launch.
- Review product analytics, customer feedback, and user research to identify practical improvements.
- Partner with stakeholders to keep releases focused, useful, and aligned with business goals.

## Requirements
- Experience managing software products from planning through delivery.
- Strong written communication and comfort turning ambiguity into clear product direction.
- Ability to work with cross-functional teams across design, engineering, and go-to-market.
- Comfort using product metrics and qualitative feedback to make decisions.

## Nice to Have
- Experience with recruiting, HR technology, or workflow automation products.
- Familiarity with B2B SaaS product development.

## Benefits
- Flexible remote-friendly work culture.
- Health, dental, and vision coverage.
- Learning budget for courses, books, and conferences.

## Why Join Us
This is a chance to shape a product that helps lean recruiting teams write better roles, move faster, and create a more thoughtful candidate experience.

## Equal Opportunity
Northstar Labs is an equal opportunity employer and welcomes applicants from all backgrounds.`;

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
  authMode: "login",
  accessToken: localStorage.getItem(AUTH_TOKEN_STORAGE_KEY) || "",
  user: null,
  credits: null,
};

const elements = {
  authModal: document.querySelector("#authModal"),
  signInBtn: document.querySelector("#signInBtn"),
  userProfile: document.querySelector("#userProfile"),
  creditsContainer: document.querySelector("#creditsContainer"),
  workspaceCredits: document.querySelector("#workspaceCredits"),
  buyCreditsBtn: document.querySelector("#buyCreditsBtn"),
  userUsername: document.querySelector("#userUsername"),
  signOutBtn: document.querySelector("#signOutBtn"),
  closeModalBtn: document.querySelector("#closeModalBtn"),
  
  billingModal: document.querySelector("#billingModal"),
  closeBillingModalBtn: document.querySelector("#closeBillingModalBtn"),
  billingAmountInput: document.querySelector("#billingAmountInput"),
  billingDecBtn: document.querySelector("#billingDecBtn"),
  billingIncBtn: document.querySelector("#billingIncBtn"),
  billingCreditCount: document.querySelector("#billingCreditCount"),
  payCreditsBtn: document.querySelector("#payCreditsBtn"),
  billingMessageBox: document.querySelector("#billingMessageBox"),
  
  authView: document.querySelector("#authView"),
  otpView: document.querySelector("#otpView"),
  modalTitle: document.querySelector("#modalTitle"),
  modalSubtitle: document.querySelector("#modalSubtitle"),
  modalAuthForm: document.querySelector("#modalAuthForm"),
  modalUsername: document.querySelector("#modalUsername"),
  modalEmail: document.querySelector("#modalEmail"),
  modalPassword: document.querySelector("#modalPassword"),
  modalSubmitBtn: document.querySelector("#modalSubmitBtn"),
  modalToggleModeBtn: document.querySelector("#modalToggleModeBtn"),
  
  modalOtpForm: document.querySelector("#modalOtpForm"),
  modalOtp: document.querySelector("#modalOtp"),
  modalOtpSubmitBtn: document.querySelector("#modalOtpSubmitBtn"),
  modalMessageBox: document.querySelector("#modalMessageBox"),
  modalForgotPasswordBtn: document.querySelector("#modalForgotPasswordBtn"),
  resetPasswordView: document.querySelector("#resetPasswordView"),
  modalResetPasswordForm: document.querySelector("#modalResetPasswordForm"),
  resetOtp: document.querySelector("#resetOtp"),
  resetNewPassword: document.querySelector("#resetNewPassword"),
  modalCancelResetBtn: document.querySelector("#modalCancelResetBtn"),
  modalResetPasswordSubmitBtn: document.querySelector("#modalResetPasswordSubmitBtn"),
  usernameModal: document.querySelector("#usernameModal"),
  closeUsernameModalBtn: document.querySelector("#closeUsernameModalBtn"),
  modalUsernameForm: document.querySelector("#modalUsernameForm"),
  newUsernameInput: document.querySelector("#newUsernameInput"),
  usernameMessageBox: document.querySelector("#usernameMessageBox"),

  // Core workspace elements
  questionRail: document.querySelector("#questionRail"),
  railToggle: document.querySelector("#railToggle"),
  questionList: document.querySelector("#questionList"),
  sampleButton: document.querySelector("#sampleButton"),
  sampleOutputButton: document.querySelector("#sampleOutputButton"),
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
  if (name == "nice_to_haves") return "Nice To Have";
  return name.replaceAll("_", " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function setMessage(text = "", type = "error") {
  elements.messageBox.textContent = text;
  elements.messageBox.classList.toggle("hidden", !text);
  elements.messageBox.classList.toggle("info", type === "info");
}

function setAuthState(data) {
  state.user = data?.user || null;
  state.credits = data?.credits || null;
  if (data?.access_token) {
    state.accessToken = data.access_token;
    localStorage.setItem(AUTH_TOKEN_STORAGE_KEY, data.access_token);
  }
  renderAuth();
}

function clearAuthState() {
  state.user = null;
  state.credits = null;
  state.accessToken = "";
  localStorage.removeItem(AUTH_TOKEN_STORAGE_KEY);
  renderAuth();
}

function renderAuth() {
  const loggedIn = Boolean(state.user);

  elements.signInBtn.classList.toggle("hidden", loggedIn);
  elements.userProfile.classList.toggle("hidden", !loggedIn);
  elements.creditsContainer.classList.toggle("hidden", !loggedIn);

  if (loggedIn && state.user) {
    const displayName = state.user.username || state.user.email.split("@")[0];
    elements.userUsername.textContent = `Hi, ${displayName}`;
    elements.workspaceCredits.textContent = `${state.credits ?? 0} Credits`;
  }
}

function creditValue(primaryKey, responseKey, fallback = 0) {
  if (!state.credits) return fallback;
  const value = state.credits[primaryKey] ?? state.credits[responseKey];
  return typeof value === "number" ? value : fallback;
}

function creditWord(value) {
  return value === 0 || value === 1 ? "Credit" : "Credits";
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
  if (elements.progressText) elements.progressText.textContent = `${answeredCount} answered`;
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

function showButtonSuccess(button, successText) {
  const originalText = button.dataset.originalText || button.textContent;
  button.dataset.originalText = originalText;
  button.textContent = successText;
  button.classList.add("button-success");
  window.clearTimeout(button._successTimer);
  button._successTimer = window.setTimeout(() => {
    button.textContent = originalText;
    button.classList.remove("button-success");
  }, 1800);
}

function formatErrorDetail(detail) {
  if (!detail) return "Request failed";
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    return detail.map(err => {
      const field = err.loc ? err.loc.join(".") : "field";
      return `${field}: ${err.msg}`;
    }).join("; ");
  }
  if (typeof detail === "object") return JSON.stringify(detail);
  return String(detail);
}

async function callApi(path, body = null) {
  const headers = {
    "Content-Type": "application/json",
  };
  if (state.accessToken) {
    headers["Authorization"] = `Bearer ${state.accessToken}`;
  }
  const options = {
    method: body ? "POST" : "GET",
    headers,
  };
  if (body) {
    options.body = JSON.stringify(body);
  }
  const response = await fetch(apiUrl(path), options);
  const data = await response.json();
  if (!response.ok) {
    throw new Error(formatErrorDetail(data.detail || data));
  }
  return data;
}

async function getApi(path) {
  const headers = {};
  if (state.accessToken) headers.Authorization = `Bearer ${state.accessToken}`;
  const response = await fetch(apiUrl(path), { headers });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(formatErrorDetail(data.detail || data));
  }
  return data;
}

function openModal() {
  elements.authModal.classList.remove("hidden");
  setModalMessage("");
  showAuthView();
}

function closeModal() {
  elements.authModal.classList.add("hidden");
}

function openBillingModal() {
  elements.billingAmountInput.value = 1;
  updateBillingCalculations();
  setBillingMessage("");
  elements.billingModal.classList.remove("hidden");
}

function closeBillingModal() {
  elements.billingModal.classList.add("hidden");
}

function setBillingMessage(text = "", type = "error") {
  elements.billingMessageBox.textContent = text;
  elements.billingMessageBox.classList.toggle("hidden", !text);
  elements.billingMessageBox.classList.toggle("info", type === "info");
}

function updateBillingCalculations() {
  let val = parseInt(elements.billingAmountInput.value, 10);
  const dollars = (isNaN(val) || val < 1) ? 0 : val;
  const credits = dollars * 30;
  elements.billingCreditCount.textContent = credits;
  elements.payCreditsBtn.textContent = `Pay $${dollars.toFixed(2)}`;
  elements.payCreditsBtn.disabled = (dollars === 0);
}

function handleAmountChange() {
  let val = parseInt(elements.billingAmountInput.value, 10);
  if (!isNaN(val)) {
    if (val < 1) val = 1;
    elements.billingAmountInput.value = val;
  }
  updateBillingCalculations();
}

function handleAmountBlur() {
  let val = parseInt(elements.billingAmountInput.value, 10);
  if (isNaN(val) || val < 1) {
    elements.billingAmountInput.value = 1;
  }
  updateBillingCalculations();
}

function incrementBillingAmount() {
  let val = parseInt(elements.billingAmountInput.value, 10);
  if (isNaN(val) || val < 1) {
    val = 1;
  } else {
    val += 1;
  }
  elements.billingAmountInput.value = val;
  updateBillingCalculations();
}

function decrementBillingAmount() {
  let val = parseInt(elements.billingAmountInput.value, 10);
  if (isNaN(val) || val <= 1) {
    val = 1;
  } else {
    val -= 1;
  }
  elements.billingAmountInput.value = val;
  updateBillingCalculations();
}

function showAuthView() {
  elements.authView.classList.remove("hidden");
  elements.otpView.classList.add("hidden");
  elements.resetPasswordView.classList.add("hidden");
}

function showOtpView() {
  elements.authView.classList.add("hidden");
  elements.otpView.classList.remove("hidden");
  elements.resetPasswordView.classList.add("hidden");
}

function showResetView() {
  elements.authView.classList.add("hidden");
  elements.otpView.classList.add("hidden");
  elements.resetPasswordView.classList.remove("hidden");
}

function setModalMessage(text = "", type = "error") {
  elements.modalMessageBox.textContent = text;
  elements.modalMessageBox.classList.toggle("hidden", !text);
  elements.modalMessageBox.classList.toggle("info", type === "info");
}

function toggleAuthMode() {
  if (state.authMode === "login") {
    state.authMode = "signup";
    elements.modalTitle.textContent = "Create Account";
    elements.modalSubtitle.textContent = "Each new account receives 30 credits.";
    elements.modalUsername.classList.remove("hidden");
    elements.modalForgotPasswordBtn.classList.add("hidden");
    elements.modalSubmitBtn.textContent = "Register";
    elements.modalToggleModeBtn.textContent = "Already have an account? Sign In";
  } else {
    state.authMode = "login";
    elements.modalTitle.textContent = "Sign In";
    elements.modalSubtitle.textContent = "Access your credits and history.";
    elements.modalUsername.classList.add("hidden");
    elements.modalForgotPasswordBtn.classList.remove("hidden");
    elements.modalSubmitBtn.textContent = "Sign In";
    elements.modalToggleModeBtn.textContent = "Create account";
  }
  setModalMessage("");
}

async function submitAuth(event) {
  event.preventDefault();
  const email = elements.modalEmail.value.trim();
  const password = elements.modalPassword.value;
  const username = elements.modalUsername.value.trim();

  if (state.authMode === "signup" && !username) {
    setModalMessage("Username is required.");
    return;
  }

  const restore = setLoading(elements.modalSubmitBtn, state.authMode === "signup" ? "Registering..." : "Signing in...");
  setModalMessage("");

  try {
    if (state.authMode === "signup") {
      const data = await callApi("/auth/signup", { username, email, password });
      showOtpView();
    } else {
      const data = await callApi("/auth/login", { email, password });
      setAuthState(data);
      closeModal();
    }
  } catch (err) {
    setModalMessage(err.message || "Authentication failed.");
  } finally {
    restore();
  }
}

async function submitOtp(event) {
  event.preventDefault();
  const email = elements.modalEmail.value.trim();
  const token = elements.modalOtp.value.trim();

  const restore = setLoading(elements.modalOtpSubmitBtn, "Verifying...");
  setModalMessage("");

  try {
    const data = await callApi("/auth/verify-otp", { email, token });
    setAuthState(data);
    closeModal();
  } catch (err) {
    setModalMessage(err.message || "Invalid verification code.");
  } finally {
    restore();
  }
}

async function loadSession() {
  if (!state.accessToken) {
    renderAuth();
    return;
  }
  try {
    const data = await getApi("/auth/me");
    setAuthState(data);
  } catch {
    clearAuthState();
  }
}

async function generateDraft() {
  if (!state.accessToken) {
    setMessage("Please sign in before generating. Each generate costs 1 credit.");
    return;
  }

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
  const restore = setLoading(elements.generateButton, "Generating...");
  setMessage("Generating your draft. This can take a moment.", "info");
  try {
    const data = await callApi("/generate", {
      job_info: buildJobInfo(),
      skipped_fields: getSkippedFields(),
    });
    state.currentDraft = data.draft;
    state.currentMarkdown = data.markdown;
    if (typeof data.credits_remaining === "number") {
      state.credits = data.credits_remaining;
      renderAuth();
    }
    state.draftOutdated = false;
    setMessage("");
  } catch (error) {
    setMessage(error.message);
  } finally {
    restore();
  }
}

async function refineDraft() {
  if (!state.accessToken) {
    setMessage("Please sign in before refining. Each refine costs 1 credit.");
    return;
  }

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

  const restore = setLoading(elements.refineButton, "Refining...");
  setMessage("Refining your draft. This can take a moment.", "info");
  try {
    const data = await callApi("/refine", {
      company_name: buildJobInfo().company_name,
      current_draft: state.currentDraft,
      user_request: request,
      skipped_fields: getSkippedFields(),
    });
    state.currentDraft = data.draft;
    state.currentMarkdown = data.markdown;
    if (typeof data.credits_remaining === "number") {
      state.credits = data.credits_remaining;
      renderAuth();
    }
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

function stripInlineMarkdown(value) {
  return value
    .replace(/\*\*(.*?)\*\*/g, "$1")
    .replace(/\*(.*?)\*/g, "$1")
    .replace(/`(.*?)`/g, "$1")
    .trim();
}

function formatMarkdownForCopy(markdown) {
  const lines = [];

  for (const rawLine of markdown.split("\n")) {
    const line = rawLine.trim();
    if (!line) {
      if (lines.length && lines[lines.length - 1] !== "") lines.push("");
      continue;
    }

    if (line.startsWith("# ")) {
      if (lines.length && lines[lines.length - 1] !== "") lines.push("");
      lines.push(stripInlineMarkdown(line.slice(2)));
      lines.push("");
      continue;
    }

    if (line.startsWith("## ")) {
      if (lines.length && lines[lines.length - 1] !== "") lines.push("");
      lines.push(stripInlineMarkdown(line.slice(3)));
      continue;
    }

    if (line.startsWith("### ")) {
      if (lines.length && lines[lines.length - 1] !== "") lines.push("");
      lines.push(stripInlineMarkdown(line.slice(4)));
      continue;
    }

    if (line.startsWith("- ") || line.startsWith("* ")) {
      lines.push(`- ${stripInlineMarkdown(line.slice(2))}`);
      continue;
    }

    lines.push(stripInlineMarkdown(line));
  }

  return lines.join("\n").replace(/\n{3,}/g, "\n\n").trim();
}

function markdownToClipboardHtml(markdown) {
  const blocks = [];
  let listItems = [];

  const closeList = () => {
    if (!listItems.length) return;
    blocks.push(`<ul style="margin: 0 0 12px 22px; padding: 0;">${listItems.join("")}</ul>`);
    listItems = [];
  };

  for (const rawLine of markdown.split("\n")) {
    const line = rawLine.trim();
    if (!line) {
      closeList();
      continue;
    }

    if (line.startsWith("# ")) {
      closeList();
      blocks.push(`<p style="margin: 0 0 14px; color: #102033; font-size: 22px; font-weight: 700; line-height: 1.25;">${escapeHtml(stripInlineMarkdown(line.slice(2)))}</p>`);
      continue;
    }

    if (line.startsWith("## ")) {
      closeList();
      blocks.push(`<p style="margin: 18px 0 8px; color: #102033; font-size: 18px; font-weight: 700; line-height: 1.3;">${escapeHtml(stripInlineMarkdown(line.slice(3)))}</p>`);
      continue;
    }

    if (line.startsWith("### ")) {
      closeList();
      blocks.push(`<p style="margin: 14px 0 6px; color: #102033; font-size: 16px; font-weight: 700; line-height: 1.35;">${escapeHtml(stripInlineMarkdown(line.slice(4)))}</p>`);
      continue;
    }

    if (line.startsWith("- ") || line.startsWith("* ")) {
      listItems.push(`<li style="margin: 0 0 5px;">${escapeHtml(stripInlineMarkdown(line.slice(2)))}</li>`);
      continue;
    }

    closeList();
    blocks.push(`<p style="margin: 0 0 10px; color: #102033; font-size: 14px; line-height: 1.55;">${escapeHtml(stripInlineMarkdown(line))}</p>`);
  }

  closeList();
  return `<div style="color: #102033; font-family: Arial, sans-serif;">${blocks.join("")}</div>`;
}

async function copyDraft() {
  const textToCopy = formatMarkdownForCopy(state.currentMarkdown);
  if (!state.currentMarkdown || !textToCopy) return;

  if (window.ClipboardItem) {
    const htmlToCopy = markdownToClipboardHtml(state.currentMarkdown);
    await navigator.clipboard.write([
      new ClipboardItem({
        "text/html": new Blob([htmlToCopy], { type: "text/html" }),
        "text/plain": new Blob([textToCopy], { type: "text/plain" }),
      }),
    ]);
  } else {
    await navigator.clipboard.writeText(textToCopy);
  }

  showButtonSuccess(elements.copyButton, "Copied");
  setMessage("Job description copied.", "info");
}

function fileSafeName(value) {
  return value
    .replace(/[<>:"/\\|?*]+/g, "")
    .replace(/\s+/g, "_")
    .replace(/^_+|_+$/g, "")
    .slice(0, 80) || "Generated_Job_Description";
}

function docxParagraphsFromMarkdown(markdown) {
  const { Paragraph, TextRun } = window.docx;
  const paragraphs = [];

  for (const rawLine of markdown.split("\n")) {
    const line = rawLine.trim();
    if (!line) {
      paragraphs.push(new Paragraph({ text: "", spacing: { after: 120 } }));
      continue;
    }

    if (line.startsWith("# ")) {
      paragraphs.push(new Paragraph({
        children: [new TextRun({
          text: stripInlineMarkdown(line.slice(2)),
          bold: true,
          color: "102033",
          size: 34,
        })],
        spacing: { after: 220 },
      }));
      continue;
    }

    if (line.startsWith("## ")) {
      paragraphs.push(new Paragraph({
        children: [new TextRun({
          text: stripInlineMarkdown(line.slice(3)),
          bold: true,
          color: "102033",
          size: 28,
        })],
        spacing: { before: 220, after: 120 },
      }));
      continue;
    }

    if (line.startsWith("### ")) {
      paragraphs.push(new Paragraph({
        children: [new TextRun({
          text: stripInlineMarkdown(line.slice(4)),
          bold: true,
          color: "102033",
          size: 24,
        })],
        spacing: { before: 160, after: 80 },
      }));
      continue;
    }

    if (line.startsWith("- ") || line.startsWith("* ")) {
      paragraphs.push(new Paragraph({
        children: [new TextRun({
          text: stripInlineMarkdown(line.slice(2)),
          color: "102033",
          size: 22,
        })],
        bullet: { level: 0 },
        spacing: { after: 80 },
      }));
      continue;
    }

    paragraphs.push(new Paragraph({
      children: [new TextRun({
        text: stripInlineMarkdown(line),
        color: "102033",
        size: 22,
      })],
      spacing: { after: 120 },
    }));
  }

  return paragraphs;
}

async function exportDocx() {
  if (!state.currentMarkdown) return;
  if (!window.docx) {
    setMessage("Word export library did not load. Check your internet connection and try again.");
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
  showButtonSuccess(elements.exportDocxButton, "Exported");
  setMessage("Word file downloaded.", "info");
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

function loadSampleOutput() {
  state.currentDraft = { ...sampleDraft };
  state.currentMarkdown = sampleMarkdown;
  state.draftOutdated = false;
  renderDraft();
  setMessage("Sample draft loaded.", "info");
}

async function buyCredits(event) {
  event.preventDefault();
  if (!state.accessToken || !state.user) {
    openModal();
    return;
  }
  openBillingModal();
}

async function payCredits(event) {
  event.preventDefault();
  let val = parseInt(elements.billingAmountInput.value, 10);
  if (isNaN(val) || val < 1) {
    setBillingMessage("Please enter a valid positive dollar amount.");
    return;
  }

  const restore = setLoading(elements.payCreditsBtn, "Loading...");
  setBillingMessage("");
  try {
    const redirectUrl = window.location.href;
    const session = await callApi(
      `/create-checkout-session?user_id=${state.user.id}&amount=${val}&redirect_url=${encodeURIComponent(redirectUrl)}`,
      {}
    );
    if (session && session.checkout_url) {
      window.location.href = session.checkout_url;
    }
  } catch (err) {
    setBillingMessage(err.message || "Failed to create checkout session.");
  } finally {
    restore();
  }
}

elements.sampleButton.addEventListener("click", loadSample);
elements.sampleOutputButton.addEventListener("click", loadSampleOutput);
elements.signInBtn.addEventListener("click", openModal);
elements.closeModalBtn.addEventListener("click", closeModal);
elements.modalToggleModeBtn.addEventListener("click", toggleAuthMode);
elements.modalAuthForm.addEventListener("submit", submitAuth);
elements.modalOtpForm.addEventListener("submit", submitOtp);
elements.buyCreditsBtn.addEventListener("click", buyCredits);
elements.closeBillingModalBtn.addEventListener("click", closeBillingModal);
elements.billingAmountInput.addEventListener("input", handleAmountChange);
elements.billingAmountInput.addEventListener("blur", handleAmountBlur);
elements.billingDecBtn.addEventListener("click", decrementBillingAmount);
elements.billingIncBtn.addEventListener("click", incrementBillingAmount);
elements.payCreditsBtn.addEventListener("click", payCredits);
elements.signOutBtn.addEventListener("click", () => {
  clearAuthState();
  setMessage("Signed out.", "info");
});
async function forgotPassword() {
  const email = elements.modalEmail.value.trim();
  if (!email) {
    setModalMessage("Please enter your email first.");
    return;
  }
  
  const restore = setLoading(elements.modalForgotPasswordBtn, "Sending...");
  setModalMessage("");
  try {
    await callApi("/auth/forgot-password", { email });
    setModalMessage("Reset code sent! Check your inbox.", "info");
    showResetView();
  } catch (err) {
    setModalMessage(err.message || "Failed to request password reset.");
  } finally {
    restore();
  }
}

async function submitResetPassword(event) {
  event.preventDefault();
  const email = elements.modalEmail.value.trim();
  const token = elements.resetOtp.value.trim();
  const new_password = elements.resetNewPassword.value;
  
  if (!email) {
    setModalMessage("Email is required.");
    return;
  }
  
  if (new_password.length < 6) {
    setModalMessage("Password must be at least 6 characters.");
    return;
  }
  
  const restore = setLoading(elements.modalResetPasswordSubmitBtn, "Resetting...");
  setModalMessage("");
  try {
    await callApi("/auth/reset-password", { email, token, new_password });
    setModalMessage("Password reset successful! Please Sign In.", "info");
    showAuthView();
    elements.resetOtp.value = "";
    elements.resetNewPassword.value = "";
  } catch (err) {
    setModalMessage(err.message || "Failed to reset password.");
  } finally {
    restore();
  }
}

function openUsernameModal() {
  if (!state.user) return;
  elements.usernameModal.classList.remove("hidden");
  elements.newUsernameInput.value = state.user.username || "";
  setUsernameMessage("");
}

function closeUsernameModal() {
  elements.usernameModal.classList.add("hidden");
}

function setUsernameMessage(text = "", type = "error") {
  elements.usernameMessageBox.textContent = text;
  elements.usernameMessageBox.classList.toggle("hidden", !text);
  elements.usernameMessageBox.classList.toggle("info", type === "info");
}

async function submitUsernameChange(event) {
  event.preventDefault();
  const newUsername = elements.newUsernameInput.value.trim();
  if (!newUsername) {
    setUsernameMessage("Username cannot be empty.");
    return;
  }
  
  const restore = setLoading(elements.usernameModal.querySelector(".primary-button"), "Saving...");
  setUsernameMessage("");
  try {
    const data = await callApi("/auth/change-username", { new_username: newUsername });
    setAuthState(data);
    closeUsernameModal();
    setMessage("Username updated successfully.", "info");
  } catch (err) {
    setUsernameMessage(err.message || "Failed to update username.");
  } finally {
    restore();
  }
}

elements.railToggle.addEventListener("click", () => {
  state.railPinned = !state.railPinned;
  localStorage.setItem(RAIL_PIN_STORAGE_KEY, String(state.railPinned));
  renderRailPin();
});
elements.generateButton.addEventListener("click", generateDraft);
elements.refineButton.addEventListener("click", refineDraft);
elements.copyButton.addEventListener("click", copyDraft);
elements.exportDocxButton.addEventListener("click", exportDocx);
elements.modalForgotPasswordBtn.addEventListener("click", forgotPassword);
elements.modalResetPasswordForm.addEventListener("submit", submitResetPassword);
elements.modalCancelResetBtn.addEventListener("click", showAuthView);
elements.userUsername.addEventListener("click", openUsernameModal);
elements.closeUsernameModalBtn.addEventListener("click", closeUsernameModal);
elements.modalUsernameForm.addEventListener("submit", submitUsernameChange);

// Toggle password visibility
document.querySelectorAll(".toggle-password-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    const input = btn.previousElementSibling;
    if (input) {
      const isPassword = input.type === "password";
      input.type = isPassword ? "text" : "password";
      const slashLine = btn.querySelector(".eye-slash");
      slashLine?.classList.toggle("hidden", !isPassword);
    }
  });
});

// SPA routing logic
const navLinks = document.querySelectorAll(".nav-link");
const pageViews = document.querySelectorAll(".page-view");

navLinks.forEach(link => {
  link.addEventListener("click", () => {
    const target = link.dataset.target;
    
    // Toggle active link class
    navLinks.forEach(l => l.classList.toggle("active", l === link));
    
    // Toggle page views display
    pageViews.forEach(view => view.classList.toggle("hidden", view.id !== target));
  });
});

// Scroll event for glassmorphism nav bar
window.addEventListener("scroll", () => {
  const navBar = document.querySelector(".nav-bar");
  if (navBar) {
    navBar.classList.toggle("scrolled", window.scrollY > 15);
  }
});

// Load and render authors from JSON
async function loadAuthors() {
  const grid = document.getElementById("authorsGrid");
  if (!grid) return;
  
  try {
    const response = await fetch("data/authors.json");
    if (!response.ok) throw new Error("Failed to load authors data");
    const authors = await response.json();
    
    grid.innerHTML = authors.map(author => `
      <div class="author-card">
        <div class="author-photo-wrapper">
          <img class="author-photo" src="${author.image}" alt="${author.name}" onerror="this.style.display='none';" />
          <div class="author-photo-fallback">${author.name.split(' ')[0]}'s Photo<br><span style="font-size: 11px; opacity: 0.7;">${author.image}</span></div>
        </div>
        <h3>${author.name}</h3>
        <p class="author-role">${author.role}</p>
        <p class="author-desc">${author.desc}</p>
        <div class="author-contacts">
          ${author.contacts.map(c => `
            <a href="${c.url}" ${c.url.startsWith('http') ? 'target="_blank"' : ''} class="contact-link">${c.label}</a>
          `).join('')}
        </div>
      </div>
    `).join("");
  } catch (error) {
    console.error("Error loading authors:", error);
    grid.innerHTML = `<p style="grid-column: span 2; text-align: center; color: var(--ink-soft);">Failed to load authors.</p>`;
  }
}

checkApi();
renderRailPin();
loadSession();
loadQuestions();
loadAuthors();
