from sqlalchemy import text


def completions_by_course(connection) -> list[dict]:
    """Powers the admin completion dashboard."""
    rows = connection.execute(
        text(
            """
            SELECT course_id, COUNT(*) AS total
            FROM enrollments
            WHERE status = 'completed'
            GROUP BY course_id
            ORDER BY total DESC
            """
        )
    )
    return [dict(row._mapping) for row in rows]
