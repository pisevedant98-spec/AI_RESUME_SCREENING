from app import db
class Candidate(db.Model):
    __tablename__ = "candidates"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    phone = db.Column(db.String(15))
    education = db.Column(db.String(100))