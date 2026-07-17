import ReactMarkdown from "react-markdown";
import { StatusMessage } from "./StatusMessage";

interface DraftPanelProps {
  markdown: string;
  refinementRequest: string;
  busyAction: "generate" | "refine" | null;
  error: string;
  status: string;
  onGenerate: () => void;
  onRefinementChange: (value: string) => void;
  onRefine: () => void;
}

export function DraftPanel({
  markdown,
  refinementRequest,
  busyAction,
  error,
  status,
  onGenerate,
  onRefinementChange,
  onRefine,
}: DraftPanelProps) {
  const busy = busyAction !== null;
  return (
    <aside className="draft-panel" aria-labelledby="draft-panel-title">
      <div className="draft-panel-header">
        <div>
          <p className="section-label">Generated output</p>
          <h2 id="draft-panel-title">Job description</h2>
        </div>
        <button className="primary-button" type="button" disabled={busy} onClick={onGenerate}>
          {busyAction === "generate" ? "GENERATING" : "GENERATE"}
        </button>
      </div>

      <StatusMessage message={error} kind="error" />
      {!error && <StatusMessage message={status} kind="status" />}

      <div className="draft-preview" aria-live="polite">
        {markdown ? <ReactMarkdown>{markdown}</ReactMarkdown> : <p className="empty-draft">Your generated job description will appear here.</p>}
      </div>

      <div className="refinement-form">
        <label htmlFor="refinement-request">Refinement request</label>
        <textarea
          id="refinement-request"
          aria-label="Refinement request"
          rows={4}
          value={refinementRequest}
          onChange={(event) => onRefinementChange(event.target.value)}
        />
        <button className="secondary-button" type="button" disabled={busy} onClick={onRefine}>
          {busyAction === "refine" ? "Refining" : "Refine"}
        </button>
      </div>
    </aside>
  );
}
