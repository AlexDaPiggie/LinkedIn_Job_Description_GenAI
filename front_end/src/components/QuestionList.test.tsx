import { useState } from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { QuestionList } from "./QuestionList";
import { QuestionNav } from "./QuestionNav";
import type { QuestionResponse } from "../types/api";

const questions: QuestionResponse[] = [
  {
    question_name: "company_name",
    question_text: "What is your company name?",
    required: true,
    answer_type: "text",
  },
  {
    question_name: "benefits",
    question_text: "Which benefits should be included?",
    required: false,
    answer_type: "list",
  },
];

it("starts collapsed and expands more than one question", async () => {
  const user = userEvent.setup();
  function Harness() {
    const [expandedQuestions, setExpandedQuestions] = useState<Set<string>>(new Set());
    return (
      <QuestionList
        questions={questions}
        answers={{}}
        expandedQuestions={expandedQuestions}
        onToggle={(questionName) => {
          setExpandedQuestions((current) => {
            const next = new Set(current);
            if (next.has(questionName)) next.delete(questionName);
            else next.add(questionName);
            return next;
          });
        }}
        onAnswerChange={vi.fn()}
      />
    );
  }
  render(<Harness />);

  expect(screen.queryByLabelText("Answer for What is your company name?")).not.toBeInTheDocument();
  expect(screen.queryByLabelText("Answer for Which benefits should be included?")).not.toBeInTheDocument();
  const companyButton = screen.getByRole("button", { name: /What is your company name/ });
  const benefitsButton = screen.getByRole("button", { name: /Which benefits should be included/ });
  expect(companyButton).not.toHaveAttribute("aria-controls");
  expect(benefitsButton).not.toHaveAttribute("aria-controls");

  await user.click(companyButton);
  expect(screen.getByLabelText("Answer for What is your company name?")).toBeVisible();
  expect(companyButton).toHaveAttribute("aria-controls", "answer-company_name");

  await user.click(benefitsButton);
  expect(screen.getByLabelText("Answer for What is your company name?")).toBeVisible();
  expect(screen.getByLabelText("Answer for Which benefits should be included?")).toBeVisible();
  expect(benefitsButton).toHaveAttribute("aria-controls", "answer-benefits");
});

it("reports answer edits", async () => {
  const user = userEvent.setup();
  const onAnswerChange = vi.fn();
  function Harness() {
    const [answers, setAnswers] = useState<Record<string, string>>({});
    return (
      <QuestionList
        questions={questions}
        answers={answers}
        expandedQuestions={new Set(["company_name"])}
        onToggle={vi.fn()}
        onAnswerChange={(name, value) => {
          setAnswers((current) => ({ ...current, [name]: value }));
          onAnswerChange(name, value);
        }}
      />
    );
  }
  render(<Harness />);

  await user.type(screen.getByLabelText("Answer for What is your company name?"), "Alex AI");
  expect(onAnswerChange).toHaveBeenLastCalledWith("company_name", "Alex AI");
});

it("reports the selected question number", async () => {
  const user = userEvent.setup();
  const onNavigate = vi.fn();
  render(<QuestionNav questions={questions} onNavigate={onNavigate} />);

  await user.click(screen.getByRole("button", { name: "Go to question 2" }));
  expect(onNavigate).toHaveBeenCalledWith("benefits");
});
