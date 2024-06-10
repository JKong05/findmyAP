from app.models import School, Course, User, tempUser
from app import db
import sqlite3
from contextlib import contextmanager

def query_database(school_name):
    # creating a session
    session = db.session

    # filter out the table for rows that include school name that is same as user input
    schools = session.query(School).filter(School.school_name == school_name).all()

    # end querying session
    session.close()
    return schools

# Main school search autocomplete
def get_suggestions(query):
    if query:
        matching_schools = School.query.filter(School.school_name.ilike(f'%{query}%')).group_by(School.school_name).with_entities(School.school_name).distinct(School.school_name).all()
        suggestions = [school.school_name for school in matching_schools]
        return suggestions
    else:
        all_schools = School.query.with_entities(School.school_name).distinct(School.school_name).all()
        suggestions = [school.school_name for school in all_schools]
        return suggestions

# Course suggestions autocomplete
def get_course_suggestions(query):
    if query:
        matching_courses = Course.query.filter(Course.course_name.ilike(f'%{query}%')).group_by(Course.course_name).with_entities(Course.course_name).all()
        suggestions = [course.course_name for course in matching_courses]
        return suggestions
    else:
        all_courses = Course.query.with_entities(Course.course_name).all()
        suggestions = [course.course_name for course in all_courses]
        return suggestions

def create_instance(school_name, instance_user, course_data):
    conn = db.engine.raw_connection()
    cursor = conn.cursor()

    cursor.execute(f"CREATE TEMPORARY TABLE IF NOT EXISTS {instance_user} (course_name TEXT, ap_score INTEGER)")
    for course in course_data:
        course_name = course['courseName']
        ap_score = int(course['apScore'])

        cursor.execute(f"INSERT INTO {instance_user} (course_name, ap_score) VALUES (?, ?)", (course_name, ap_score))
    
    conn.commit()

    cursor.execute(f'''
        SELECT et.school_name, et.course_name, et.min_ap_score, et.credit, et.equivalent_credit
        FROM updateschool et
        JOIN {instance_user} t
        ON et.course_name = t.course_name
        WHERE et.school_name = ? AND et.min_ap_score <= t.ap_score
    ''', (school_name,))

    conn.close()
    results = cursor.fetchall()
    return results

# fetch unique course names to display a list of ap classes you took that you get credit for
def fetch_course_names(school_name, course_data):
    conn = db.engine.raw_connection()
    cursor = conn.cursor()  
    
    course_names = []

    for course in course_data:
        course_name = course['courseName']
        ap_score = int(course['apScore'])
        cursor.execute('''
            SELECT DISTINCT course_name 
            FROM updateschool
            WHERE school_name = ? AND course_name = ? AND min_ap_score <= ?
        ''', (school_name, course_name, ap_score))
        result = cursor.fetchone()
        if result:
            course_names.append(result[0])
    
    conn.close()
    return course_names

def fetch_credits(school_name, course_data):
    conn = db.engine.raw_connection()
    cursor = conn.cursor()  
    
    credit_hours = []

    for course in course_data:
        course_name = course['courseName']
        ap_score = int(course['apScore'])
        cursor.execute('''
            SELECT MAX(credit) 
            FROM updateschool
            WHERE school_name = ? AND course_name = ? AND min_ap_score <= ?
        ''', (school_name, course_name, ap_score))
        result = cursor.fetchone()
        if result:
            credit_hours.append(result[0] or 0)
    
    conn.close()
    return credit_hours

def temp_access(school_name, course_name, ap_score):
    temp_session = db.session
    temp_table = tempUser(temp_school_name=school_name, temp_course_name=course_name, temp_ap_score=ap_score)
    temp_session.add(temp_table)
    results = table_comparison()

    return results

def table_comparison():
    ...