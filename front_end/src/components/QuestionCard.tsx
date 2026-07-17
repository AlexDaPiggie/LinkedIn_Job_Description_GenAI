import type { QuestionResponse } from "../types/api";

interface QuestionCardProps {
  question: QuestionResponse;
  index: number;
  value: string;
  expanded: boolean;
  onToggle: (questionName: string) => void;
  onAnswerChange: (questionName: string, value: string) => void;
}

export function QuestionCard({
  question,
  index,
  value,
  expanded,
  onToggle,
  onAnswerChange,
}: QuestionCardProps) {
  const answerId = `answer-${question.question_name}`;
  return (
    <article className="question-card" id={`question-${question.question_name}`}>
      <button
        className="question-header"
        type="button"
        aria-expanded={expanded}
        aria-controls={expanded ? answerId : undefined}
        onClick={() => onToggle(question.question_name)}
      >
        <span className="question-index">{String(index + 1).padStart(2, "0")}</span>
        <span className="question-copy">
          <span>{question.question_text}</span>
          <span className="question-meta">{question.required ? "Required" : "Optional"}</span>
        </span>
        <span className="question-action">{expanded ? "Close" : "Answer"}</span>
      </button>
      {expanded && (
        <div className="answer-region" id={answerId}>
          <label htmlFor={`${answerId}-input`}>Answer for {question.question_text}</label>
          <textarea
            id={`${answerId}-input`}
            aria-label={`Answer for ${question.question_text}`}
            value={value}
            rows={question.answer_type === "list" ? 5 : 4}
            onChange={(event) => onAnswerChange(question.question_name, event.target.value)}
          />
          {question.answer_type === "list" && (
            <p className="field-guidance">Enter one item per line. Commas are also accepted.</p>
          )}
        </div>
      )}
    </article>
  );
}
