from app.models import School
from app import db

def query_database(school_name):
    # creating a session
    session = db.session

    # filter out the table for rows that include school name that is same as user input
    schools = session.query(School).filter(School.school_name == school_name).all()

    # end querying session
    session.close()
    return schools