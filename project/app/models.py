from app import db
from flask_login import UserMixin


class School(db.Model):
    __tablename__ = 'school'
    id = db.Column(db.Integer, primary_key = True)
    school_name = db.Column(db.Text)
    course_name = db.Column(db.Text)
    min_ap_score = db.Column(db.Integer, nullable=True)
    equivalent_credit = db.Column(db.Text)

# This is the table that will house a user who decides to login to access the all-in-one function.
# I did this because my assumption is that some students will go to one school and fill out their information
# for a one-time use of the application which means making an account is not necessary. However,
# a student may want to use this service to see whether a list of schools they are interested in will give them credit
# and so they will want to not have to keep re-entering data (this also incentivizes signing up on the application). 
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    school_name = db.Column(db.Text)
    course_name = db.Column(db.Text)
    ap_score = db.Column(db.Integer)

class tempUser(db.Model):
    __tablename__ = 'temp'
    id = db.Column(db.Integer, primary_key = True)
    session_id = db.Column(db.String(36), nullable=False)
    temp_school_name = db.Column(db.Text)
    temp_course_name = db.Column(db.Text)
    temp_ap_score = db.Column(db.Integer)