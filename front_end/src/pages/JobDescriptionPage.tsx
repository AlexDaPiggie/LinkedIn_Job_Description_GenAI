import { useEffect, useMemo, useState } from "react";
import { DraftPanel } from "../components/DraftPanel";
import { QuestionList } from "../components/QuestionList";
import { QuestionNav } from "../components/QuestionNav";
import { StatusMessage } from "../components/StatusMessage";
import {
  generateJobDescription,
  getQuestions,
  refineJobDescription,
} from "../api/jobDescriptionApi";
import type { JobDescriptionDraft, JobInfo, QuestionResponse } from "../types/api";

type BusyAction = "generate" | "refine" | null;

function parseListAnswer(value: string): string[] {
  return value
    .split(/[\n,]/)
    .map((item) => item.trim())
    .filter(Boolean);
}

function textAnswer(answers: Record<string, string>, name: string): string {
  return answers[name]?.trim() ?? "";
}

function answerIsEmpty(question: QuestionResponse, answers: Record<string, string>): boolean {
  const value = textAnswer(answers, question.question_name);
  return question.answer_type === "list" ? parseListAnswer(value).length === 0 : value.length === 0;
}

function buildJobInfo(answers: Record<string, string>): JobInfo {
  return {
    company_name: textAnswer(answers, "company_name"),
    role_title: textAnswer(answers, "role_title"),
    role_summary: textAnswer(answers, "role_summary"),
    responsibilities: parseListAnswer(textAnswer(answers, "responsibilities")),
    requirements: parseListAnswer(textAnswer(answers, "requirements")),
    company_description: textAnswer(answers, "company_description") || null,
    nice_to_haves: parseListAnswer(textAnswer(answers, "nice_to_haves")),
    benefits: parseListAnswer(textAnswer(answers, "benefits")),
    why_join_us: textAnswer(answers, "why_join_us"),
    equal_opportunity: textAnswer(answers, "equal_opportunity"),
    tone: textAnswer(answers, "tone") || "professional",
    target_length: textAnswer(answers, "target_length") || "medium",
  };
}

function buildSkippedFields(questions: QuestionResponse[], answers: Record<string, string>): string[] {
  return questions
    .filter((question) => answerIsEmpty(question, answers))
    .map((question) => question.question_name);
}

function missingRequiredQuestions(questions: QuestionResponse[], answers: Record<string, string>) {
  return questions.filter((question) => question.required && answerIsEmpty(question, answers));
}

function errorMessage(error: unknown): string {
  return error instanceof Error ? error.message : "An unexpected error occurred.";
}

export function JobDescriptionPage() {
  const [questions, setQuestions] = useState<QuestionResponse[]>([]);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [expandedQuestions, setExpandedQuestions] = useState<Set<string>>(new Set());
  const [draft, setDraft] = useState<JobDescriptionDraft | null>(null);
  const [markdown, setMarkdown] = useState("");
  const [refinementRequest, setRefinementRequest] = useState("");
  const [loadingQuestions, setLoadingQuestions] = useState(true);
  const [busyAction, setBusyAction] = useState<BusyAction>(null);
  const [error, setError] = useState("");
  const [status, setStatus] = useState("");
  const [questionToFocus, setQuestionToFocus] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    getQuestions()
      .then((loadedQuestions) => {
        if (active) setQuestions(loadedQuestions);
      })
      .catch((requestError) => {
        if (active) setError(`Unable to load questions. ${errorMessage(requestError)}`);
      })
      .finally(() => {
        if (active) setLoadingQuestions(false);
      });
    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    if (!questionToFocus || !expandedQuestions.has(questionToFocus)) return;
    const input = document.getElementById(`answer-${questionToFocus}-input`);
    if (input instanceof HTMLTextAreaElement) {
      input.focus();
      setQuestionToFocus(null);
    }
  }, [expandedQuestions, questionToFocus]);

  const skippedFields = useMemo(() => buildSkippedFields(questions, answers), [questions, answers]);

  function toggleQuestion(questionName: string) {
    setExpandedQuestions((current) => {
      const next = new Set(current);
      if (next.has(questionName)) next.delete(questionName);
      else next.add(questionName);
      return next;
    });
  }

  function navigateToQuestion(questionName: string) {
    document.getElementById(`question-${questionName}`)?.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function updateAnswer(questionName: string, value: string) {
    setAnswers((current) => ({ ...current, [questionName]: value }));
    setError("");
    setStatus("");
  }

  function updateRefinementRequest(value: string) {
    setRefinementRequest(value);
    setError("");
    setStatus("");
  }

  async function generate() {
    const missing = missingRequiredQuestions(questions, answers);
    if (missing.length) {
      const first = missing[0];
      setExpandedQuestions((current) => new Set(current).add(first.question_name));
      navigateToQuestion(first.question_name);
      setQuestionToFocus(first.question_name);
      setError(`Please answer: ${missing.map((question) => question.question_text).join("; ")}`);
      return;
    }

    setBusyAction("generate");
    setError("");
    setStatus("");
    try {
      const response = await generateJobDescription({
        job_info: buildJobInfo(answers),
        skipped_fields: skippedFields,
      });
      setDraft(response.draft);
      setMarkdown(response.markdown);
      setStatus("Draft generated.");
    } catch (requestError) {
      setError(`Generation failed. ${errorMessage(requestError)}`);
    } finally {
      setBusyAction(null);
    }
  }

  async function refine() {
    if (!draft) {
      setError("Generate a draft before refining it.");
      return;
    }
    const request = refinementRequest.trim();
    if (!request) {
      setError("Enter a refinement request.");
      return;
    }

    setBusyAction("refine");
    setError("");
    setStatus("");
    try {
      const response = await refineJobDescription({
        job_info: buildJobInfo(answers),
        current_draft: draft,
        user_request: request,
        skipped_fields: skippedFields,
      });
      setDraft(response.draft);
      setMarkdown(response.markdown);
      setRefinementRequest("");
      setStatus("Draft refined.");
    } catch (requestError) {
      setError(`Refinement failed. ${errorMessage(requestError)}`);
    } finally {
      setBusyAction(null);
    }
  }

  if (loadingQuestions) {
    return <p className="page-state" role="status">Loading questions...</p>;
  }

  if (!questions.length) {
    return <StatusMessage kind="error" message={error || "No questions are available."} />;
  }

  return (
    <section id="job-description-workspace" className="workspace" aria-labelledby="workspace-title">
      <h1 className="sr-only" id="workspace-title">Job description workspace</h1>
      <QuestionNav questions={questions} onNavigate={navigateToQuestion} />
      <section className="question-column" aria-label="Job description questions">
        <div className="column-heading">
          <p className="section-label">Role intake</p>
          <h2>Tell us about the role</h2>
          <p>Answer the required questions, then add any optional context that will improve the draft.</p>
        </div>
        <QuestionList
          questions={questions}
          answers={answers}
          expandedQuestions={expandedQuestions}
          onToggle={toggleQuestion}
          onAnswerChange={updateAnswer}
        />
      </section>
      <DraftPanel
        markdown={markdown}
        refinementRequest={refinementRequest}
        busyAction={busyAction}
        error={error}
        status={status}
        onGenerate={generate}
        onRefinementChange={updateRefinementRequest}
        onRefine={refine}
      />
    </section>
  );
}
