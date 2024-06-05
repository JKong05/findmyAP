from flask import render_template, request, jsonify
from app import app
from app.db_operations import query_database
from app.models import School
from sqlalchemy import func

# Whenever web browser requests these two URLs, Flask is going to invoke this function and pass its return value back to the browser
@app.route('/') # decorators - modifies the function that follows it
@app.route('/index')
def index():

    return render_template('index.html')

@app.route('/query', methods=['GET'])
def get_school():
    school_name = request.args.get('school_name')
    schools = query_database(school_name)
    return render_template('index.html', schools=schools)

@app.route('/autocomplete')
def autocomplete():
    query = request.args.get('query')
    print("Received query:", query)
    if query:
        matching_schools = School.query.filter(School.school_name.ilike(f'%{query}%')).group_by(School.school_name).with_entities(School.school_name).distinct(School.school_name).all()
        suggestions = [school.school_name for school in matching_schools]
        return jsonify(suggestions)
    else:
        all_schools = School.query.with_entities(School.school_name).distinct(School.school_name).all()
        suggestions = [school.school_name for school in all_schools]
        return jsonify(suggestions)
