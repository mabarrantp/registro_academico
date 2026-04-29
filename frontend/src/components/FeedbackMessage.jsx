export default function FeedbackMessage({ type, message }) {
  if (!message) return null;

  return (
    <div className={`feedback ${type}`}>
      {message}
    </div>
  );
}