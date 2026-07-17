interface StatusMessageProps {
  message: string;
  kind: "error" | "status";
}

export function StatusMessage({ message, kind }: StatusMessageProps) {
  if (!message) return null;
  return (
    <p className={`status-message status-message--${kind}`} role={kind === "error" ? "alert" : "status"}>
      {message}
    </p>
  );
}
