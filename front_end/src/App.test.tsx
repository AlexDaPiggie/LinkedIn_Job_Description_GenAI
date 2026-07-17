import { render, screen } from "@testing-library/react";
import App from "./App";

vi.mock("./api/jobDescriptionApi", () => ({
  getQuestions: vi.fn().mockResolvedValue([
    {
      question_name: "company_name",
      question_text: "What is your company name?",
      required: true,
      answer_type: "text",
    },
  ]),
  generateJobDescription: vi.fn(),
  refineJobDescription: vi.fn(),
}));

it("renders the shell and job-description workspace", async () => {
  render(<App />);

  expect(screen.getByRole("link", { name: "Job Description Studio" })).toBeVisible();
  expect(await screen.findByText("What is your company name?")).toBeVisible();
});
