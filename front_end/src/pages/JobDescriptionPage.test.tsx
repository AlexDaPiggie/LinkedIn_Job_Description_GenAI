import { act, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { JobDescriptionPage } from "./JobDescriptionPage";
import * as api from "../api/jobDescriptionApi";
import type { GenerateResponse, QuestionResponse } from "../types/api";

const questions: QuestionResponse[] = [
  { question_name: "company_name", question_text: "Company?", required: true, answer_type: "text" },
  { question_name: "role_title", question_text: "Role?", required: true, answer_type: "text" },
  { question_name: "role_summary", question_text: "Summary?", required: true, answer_type: "text" },
  { question_name: "responsibilities", question_text: "Responsibilities?", required: true, answer_type: "list" },
  { question_name: "requirements", question_text: "Requirements?", required: true, answer_type: "list" },
  { question_name: "benefits", question_text: "Benefits?", required: false, answer_type: "list" },
  { question_name: "salary_range", question_text: "Salary range?", required: false, answer_type: "text" },
];

const generated: GenerateResponse = {
  draft: {
    title: "AI Engineer",
    about_company: "Alex AI builds hiring tools.",
    about_role: "Build reliable AI products.",
    responsibilities: ["Build systems."],
    requirements: ["Use Python."],
    nice_to_haves: [],
    benefits: [],
    why_join_us: "Do meaningful work.",
    equal_opportunity: "",
  },
  markdown: "# AI Engineer\n\n## About the role\n\nBuild reliable AI products.",
};

beforeEach(() => {
  vi.clearAllMocks();
  vi.restoreAllMocks();
  vi.spyOn(api, "getQuestions").mockResolvedValue(questions);
});

async function answerQuestion(user: ReturnType<typeof userEvent.setup>, text: string, answer: string) {
  let input = screen.queryByLabelText(`Answer for ${text}`);
  if (!input) {
    await user.click(screen.getByRole("button", { name: new RegExp(text) }));
    input = screen.getByLabelText(`Answer for ${text}`);
  }
  await user.clear(input);
  if (answer) await user.type(input, answer);
}

async function answerRequiredQuestions(user: ReturnType<typeof userEvent.setup>) {
  await answerQuestion(user, "Company?", "Alex AI");
  await answerQuestion(user, "Role?", "AI Engineer");
  await answerQuestion(user, "Summary?", "Build hiring tools");
  await answerQuestion(user, "Responsibilities?", "Build systems\nReview models");
  await answerQuestion(user, "Requirements?", "Python, SQL");
}

async function renderReady(user: ReturnType<typeof userEvent.setup>) {
  render(<JobDescriptionPage />);
  await screen.findByText("Company?");
  await answerRequiredQuestions(user);
}

async function generateReadyDraft(user: ReturnType<typeof userEvent.setup>) {
  await renderReady(user);
  await user.click(screen.getByRole("button", { name: "GENERATE" }));
  expect(await screen.findByRole("heading", { name: "AI Engineer" })).toBeVisible();
}

it("loads questions collapsed and scrolls from number navigation", async () => {
  const user = userEvent.setup();
  render(<JobDescriptionPage />);
  expect(await screen.findByText("Company?")).toBeVisible();
  expect(screen.queryByLabelText("Answer for Company?")).not.toBeInTheDocument();

  const target = document.getElementById("question-role_title");
  await user.click(screen.getByRole("button", { name: "Go to question 2" }));
  expect(target?.scrollIntoView).toHaveBeenCalledWith({ behavior: "smooth", block: "start" });
});

it("renders a question-load error", async () => {
  vi.mocked(api.getQuestions).mockRejectedValueOnce(new Error("Network unavailable"));

  render(<JobDescriptionPage />);

  expect(await screen.findByRole("alert")).toHaveTextContent(
    "Unable to load questions. Network unavailable",
  );
});

it("blocks generation, opens the first missing required question, and clears the error on edit", async () => {
  const user = userEvent.setup();
  render(<JobDescriptionPage />);
  await screen.findByText("Company?");

  await user.click(screen.getByRole("button", { name: "GENERATE" }));
  expect(screen.getByRole("alert")).toHaveTextContent("Please answer: Company?");
  const firstMissingAnswer = screen.getByLabelText("Answer for Company?");
  expect(firstMissingAnswer).toBeVisible();
  await waitFor(() => expect(firstMissingAnswer).toHaveFocus());

  await user.type(firstMissingAnswer, "Alex AI");
  expect(screen.queryByRole("alert")).not.toBeInTheDocument();
});

it("clears an empty-refinement error when the request is edited", async () => {
  const user = userEvent.setup();
  vi.spyOn(api, "generateJobDescription").mockResolvedValue(generated);
  await generateReadyDraft(user);

  await user.click(screen.getByRole("button", { name: "Refine" }));
  expect(screen.getByRole("alert")).toHaveTextContent("Enter a refinement request.");

  await user.type(screen.getByLabelText("Refinement request"), "Make it warmer.");
  expect(screen.queryByRole("alert")).not.toBeInTheDocument();
});

it("sends the exact normalized generate request and keeps unsupported answers out of job_info", async () => {
  const user = userEvent.setup();
  const generateMock = vi.spyOn(api, "generateJobDescription").mockResolvedValue(generated);
  await renderReady(user);
  await answerQuestion(user, "Benefits?", ",\n,  ");
  await answerQuestion(user, "Salary range?", "$150,000 - $180,000");

  await user.click(screen.getByRole("button", { name: "GENERATE" }));

  await waitFor(() => expect(generateMock).toHaveBeenCalledTimes(1));
  expect(generateMock).toHaveBeenCalledWith({
    job_info: {
      company_name: "Alex AI",
      role_title: "AI Engineer",
      role_summary: "Build hiring tools",
      responsibilities: ["Build systems", "Review models"],
      requirements: ["Python", "SQL"],
      company_description: null,
      nice_to_haves: [],
      benefits: [],
      why_join_us: "",
      equal_opportunity: "",
      tone: "professional",
      target_length: "medium",
    },
    skipped_fields: ["benefits"],
  });
  expect(generateMock.mock.calls[0][0].skipped_fields).not.toContain("salary_range");
  expect(generateMock.mock.calls[0][0].job_info).not.toHaveProperty("salary_range");
});

it("preserves answers and the existing preview when regeneration fails", async () => {
  const user = userEvent.setup();
  const generateMock = vi
    .spyOn(api, "generateJobDescription")
    .mockResolvedValueOnce(generated)
    .mockRejectedValueOnce(new Error("Service unavailable"));
  await generateReadyDraft(user);
  await answerQuestion(user, "Company?", "Alex AI Labs");

  await user.click(screen.getByRole("button", { name: "GENERATE" }));

  expect(await screen.findByRole("alert")).toHaveTextContent(
    "Generation failed. Service unavailable",
  );
  expect(screen.getByLabelText("Answer for Company?")).toHaveValue("Alex AI Labs");
  expect(screen.getByRole("heading", { name: "AI Engineer" })).toBeVisible();
  expect(screen.getByText("Build reliable AI products.")).toBeVisible();
  expect(generateMock).toHaveBeenCalledTimes(2);
});

it("preserves the current draft preview and request when refinement fails", async () => {
  const user = userEvent.setup();
  vi.spyOn(api, "generateJobDescription").mockResolvedValue(generated);
  vi.spyOn(api, "refineJobDescription").mockRejectedValue(new Error("Try again later"));
  await generateReadyDraft(user);
  await user.type(screen.getByLabelText("Refinement request"), "Make it warmer.");

  await user.click(screen.getByRole("button", { name: "Refine" }));

  expect(await screen.findByRole("alert")).toHaveTextContent(
    "Refinement failed. Try again later",
  );
  expect(screen.getByLabelText("Refinement request")).toHaveValue("Make it warmer.");
  expect(screen.getByRole("heading", { name: "AI Engineer" })).toBeVisible();
  expect(screen.getByText("Build reliable AI products.")).toBeVisible();
});

it("disables generation and refinement actions while a request is pending", async () => {
  const user = userEvent.setup();
  let resolveGenerate: (response: GenerateResponse) => void = () => undefined;
  const pendingResponse = new Promise<GenerateResponse>((resolve) => {
    resolveGenerate = resolve;
  });
  vi.spyOn(api, "generateJobDescription").mockReturnValue(pendingResponse);
  await renderReady(user);

  await user.click(screen.getByRole("button", { name: "GENERATE" }));

  expect(screen.getByRole("button", { name: "GENERATING" })).toBeDisabled();
  expect(screen.getByRole("button", { name: "Refine" })).toBeDisabled();

  await act(async () => {
    resolveGenerate(generated);
  });
  expect(await screen.findByRole("heading", { name: "AI Engineer" })).toBeVisible();
});

it("refines the current draft and uses the latest returned draft for successive refinement", async () => {
  const user = userEvent.setup();
  const firstRefinement: GenerateResponse = {
    draft: { ...generated.draft, about_role: "A warmer role description." },
    markdown: "# AI Engineer\n\nFirst refinement.",
  };
  const secondRefinement: GenerateResponse = {
    draft: { ...firstRefinement.draft, about_role: "A concise role description." },
    markdown: "# AI Engineer\n\nSecond refinement.",
  };
  vi.spyOn(api, "generateJobDescription").mockResolvedValue(generated);
  const refineMock = vi
    .spyOn(api, "refineJobDescription")
    .mockResolvedValueOnce(firstRefinement)
    .mockResolvedValueOnce(secondRefinement);
  await generateReadyDraft(user);

  await user.click(screen.getByRole("button", { name: "Refine" }));
  expect(screen.getByRole("alert")).toHaveTextContent("Enter a refinement request.");

  await user.type(screen.getByLabelText("Refinement request"), "Make the tone warmer.");
  await user.click(screen.getByRole("button", { name: "Refine" }));
  expect(await screen.findByText("First refinement.")).toBeVisible();

  await user.type(screen.getByLabelText("Refinement request"), "Make it shorter.");
  await user.click(screen.getByRole("button", { name: "Refine" }));
  await waitFor(() => expect(refineMock).toHaveBeenCalledTimes(2));
  expect(refineMock.mock.calls[0][0].current_draft).toEqual(generated.draft);
  expect(refineMock.mock.calls[1][0].current_draft).toEqual(firstRefinement.draft);
  expect(await screen.findByText("Second refinement.")).toBeVisible();
});

it("blocks refinement before a generated draft exists", async () => {
  const user = userEvent.setup();
  render(<JobDescriptionPage />);
  await screen.findByText("Company?");

  await user.type(screen.getByLabelText("Refinement request"), "Make it shorter.");
  await user.click(screen.getByRole("button", { name: "Refine" }));
  expect(screen.getByRole("alert")).toHaveTextContent("Generate a draft before refining it.");
});
