from sqlalchemy import text


def sync_completions_to_partner(connection, partner_client) -> int:
    """Pushes finished enrollments to the partner LMS each night."""
    rows = connection.execute(
        text("SELECT id, user_id, course_id, status FROM enrollments")
    )

    pushed = 0
    for row in rows:
        record = dict(row._mapping)
        if record["status"] == "completed":
            partner_client.push_completion(
                user_id=record["user_id"],
                course_id=record["course_id"],
                state="completed",
            )
            pushed += 1
    return pushed
