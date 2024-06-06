from app.models import School, User, tempUser
from app import db
import sqlite3

def query_database(school_name):
    # creating a session
    session = db.session

    # filter out the table for rows that include school name that is same as user input
    schools = session.query(School).filter(School.school_name == school_name).all()

    # end querying session
    session.close()
    return schools

def temp_access(school_name, course_name, ap_score):
    temp_session = db.session
    temp_table = tempUser(temp_school_name=school_name, temp_course_name=course_name, temp_ap_score=ap_score)
    temp_session.add(temp_table)
    results = table_comparison()

    return results

def table_comparison():
    ...