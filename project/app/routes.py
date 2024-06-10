from flask import render_template, request, jsonify
import uuid
from app import app
from app.db_operations import query_database, get_suggestions, get_course_suggestions
from app.models import School, User
from app.forms import SignInForm, SignUpForm

# Whenever web browser requests these two URLs, Flask is going to invoke this function and pass its return value back to the browser
@app.route('/') # decorators - modifies the function that follows it
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/query', methods=['GET'])
def get_school():
    school_name = request.args.get('school_name')
    schools = query_database(school_name)
    return render_template('index.html', schools=schools)


@app.route('/autocomplete')
def autocomplete():
    query = request.args.get('query')
    print("Received query:", query)
    return jsonify(get_suggestions(query))


@app.route('/autocomplete_courses')
def autocomplete_courses():
    query = request.args.get('query')
    print("Received query:", query)
    return jsonify(get_course_suggestions(query))


