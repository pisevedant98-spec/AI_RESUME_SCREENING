from sqlalchemy import text

def get_candidate_profile(db, user_id):
    query = text("""
        SELECT *
        FROM candidates
        WHERE user_id = :user_id
    """)

    return db.execute(
        query,
        {"user_id": user_id}
    ).fetchone()