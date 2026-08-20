import { EnrollmentBadge } from "./EnrollmentBadge";

export function EnrollmentList({ enrollments, onlyFinished }) {
  const visible = onlyFinished
    ? enrollments.filter((e) => e.status === "completed")
    : enrollments;

  return (
    <ul>
      {visible.map((enrollment) => (
        <li key={enrollment.id}>
          {enrollment.course_id} <EnrollmentBadge enrollment={enrollment} />
        </li>
      ))}
    </ul>
  );
}
