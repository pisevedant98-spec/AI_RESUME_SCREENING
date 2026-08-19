from app import db
class Interview(db.Model):
    __tablename__ = "interviews"

    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer)
    job_id = db.Column(db.Integer)
    interview_date = db.Column(db.Date)
    status = db.Column(db.String(20))