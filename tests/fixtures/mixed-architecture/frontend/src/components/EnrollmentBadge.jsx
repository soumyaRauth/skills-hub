export function EnrollmentBadge({ enrollment }) {
  if (enrollment.status === "completed") {
    return <span className="badge badge--success">Completed</span>;
  }
  if (enrollment.status === "withdrawn") {
    return <span className="badge badge--muted">Withdrawn</span>;
  }
  return <span className="badge">In progress</span>;
}
