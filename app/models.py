from app import db

class School(db.Model):
    __tablename__ = 'updateschool'
    id = db.Column(db.Integer, primary_key = True)
    school_name = db.Column(db.Text)
    course_name = db.Column(db.Text)
    min_ap_score = db.Column(db.Integer, nullable=True)
    equivalent_credit = db.Column(db.Text)
    location = db.Column(db.Text)
    url = db.Column(db.Text)

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key = True)
    course_name = db.Column(db.Text)
