from flask import render_template, request, jsonify, redirect, url_for, session
import uuid
from app import app
from app.db_operations import query_database
from app.models import School, User
from app.forms import SignInForm, SignUpForm, submitTempData


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
    if query:
        matching_schools = School.query.filter(School.school_name.ilike(f'%{query}%')).group_by(School.school_name).with_entities(School.school_name).distinct(School.school_name).all()
        suggestions = [school.school_name for school in matching_schools]
        return jsonify(suggestions)
    else:
        all_schools = School.query.with_entities(School.school_name).distinct(School.school_name).all()
        suggestions = [school.school_name for school in all_schools]
        return jsonify(suggestions)


course_scores = []
@app.route('/school_details', methods=['GET', 'POST'])
def school_details():
    # Handling 'get' requests such as displaying the name of the school on the page
    school_name = request.args.get('school_name')
    schools = query_database(school_name)

    form = submitTempData()  # Create the form instance

    if request.method == 'POST' and form.validate_on_submit():
        course_name = form.course_name.data
        ap_score = form.score.data
        course_scores.append({'temp_course_name': course_name, 'temp_ap_score': ap_score})
        # Redirect to avoid form resubmission on page reload
        return redirect(url_for('school_details'))
    

    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())

    # We are going to need to get data regarding school_name, course_name, and ap_score
    return render_template('details.html', schools=schools, form=form, course_scores=course_scores)
