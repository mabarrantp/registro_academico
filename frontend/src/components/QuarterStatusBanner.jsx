export default function QuarterStatusBanner({ quarter }) {
  if (quarter.status !== "CLOSED") return null;

  return (
    <div className="feedback error">
      🔒 <strong>Quarter cerrado.</strong> Este período ya no admite cambios.
    </div>
  );
}