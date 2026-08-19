from sqlalchemy import text

def get_all_jobs(db):
    query = text("""
        SELECT *
        FROM jobs
    """)

    return db.execute(query).fetchall()