from app import db

# need to figure out where to put this 
class School(db.Model):
    __tablename__ = 'school'
    id = db.Column(db.Integer, primary_key = True)
    school_name = db.Column(db.String)
    course_name = db.Column(db.String)
    min_ap_score = db.Column(db.Integer)
    equivalent_credit = db.Column(db.String)
