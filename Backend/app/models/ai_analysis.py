from app import db
class AIAnalysis(db.Model):
    __tablename__ = "ai_analysis"

    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer)
    job_id = db.Column(db.Integer)
    match_score = db.Column(db.Float)
    missing_skills = db.Column(db.Text)