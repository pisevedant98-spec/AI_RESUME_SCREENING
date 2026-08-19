from sqlalchemy import text
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )

def get_user_by_email(db, email):
    query = text("""
        SELECT id, name, email, password, role
        FROM users
        WHERE email = :email
    """)

    return db.execute(
        query,
        {"email": email}
    ).fetchone()