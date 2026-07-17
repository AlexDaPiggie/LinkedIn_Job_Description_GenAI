import { QuestionCard } from "./QuestionCard";
import type { QuestionResponse } from "../types/api";

interface QuestionListProps {
  questions: QuestionResponse[];
  answers: Record<string, string>;
  expandedQuestions: Set<string>;
  onToggle: (questionName: string) => void;
  onAnswerChange: (questionName: string, value: string) => void;
}

export function QuestionList({
  questions,
  answers,
  expandedQuestions,
  onToggle,
  onAnswerChange,
}: QuestionListProps) {
  return (
    <div className="question-list">
      {questions.map((question, index) => (
        <QuestionCard
          key={question.question_name}
          question={question}
          index={index}
          value={answers[question.question_name] ?? ""}
          expanded={expandedQuestions.has(question.question_name)}
          onToggle={onToggle}
          onAnswerChange={onAnswerChange}
        />
      ))}
    </div>
  );
}
