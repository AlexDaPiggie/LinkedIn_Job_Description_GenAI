import type { QuestionResponse } from "../types/api";

interface QuestionNavProps {
  questions: QuestionResponse[];
  onNavigate: (questionName: string) => void;
}

export function QuestionNav({ questions, onNavigate }: QuestionNavProps) {
  return (
    <nav className="question-nav" aria-label="Question navigation">
      {questions.map((question, index) => (
        <button
          key={question.question_name}
          type="button"
          aria-label={`Go to question ${index + 1}`}
          onClick={() => onNavigate(question.question_name)}
        >
          {index + 1}
        </button>
      ))}
    </nav>
  );
}
