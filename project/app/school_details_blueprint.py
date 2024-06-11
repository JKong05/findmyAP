from flask import Blueprint, render_template, request, session
import json
import uuid
import pandas as pd


school_details_blueprint = Blueprint('school_details', __name__)

@school_details_blueprint.route('/school_details', methods=['GET', 'POST'])
def school_details():
    # Done to avoid circular import
    from app.db_operations import query_database, create_instance, fetch_course_names, fetch_credits

    if request.method == 'GET':
        school_name = request.args.get('school_name')
        if school_name:
            session['school_name'] = school_name
        else:
            school_name = session.get('school_name')

        schools = query_database(school_name)
        name, url, location = schools[0].school_name, schools[0].url, schools[0].location
        return render_template('details.html', school_name=name, url=url, location=location)
    else:
        course_data_json = request.form.get('courseData')
        course_data = json.loads(course_data_json)

        session['course_data'] = course_data

        if 'instance_user' not in session:
            session['instance-user'] = 'temp_user_data_' + str(uuid.uuid4()).replace('-', '_')

        instance_user = session['instance-user']
        school_name = session.get('school_name')

        results = create_instance(school_name, instance_user, course_data)
        course_names = fetch_course_names(school_name, course_data)
        credit_hours = sum(fetch_credits(school_name, course_data))
        result_details, csv_content = result_append(results, school_name)
        
        schools = query_database(school_name)
        name, url, location = schools[0].school_name, schools[0].url, schools[0].location

        course_data = session.get('course_data', [])
        
        return render_template('details.html', school_name=name, url=url, location=location, result_details=result_details
                               , show_details=True, unique_course_name=course_names, credits=credit_hours, csv_content=csv_content,
                               course_data=course_data) 

def result_append(results, school_name):
    result_details = []
    for result in results:
            result_details.append({
                'course_name': result[1],
                'min_ap_score': result[2],
                'credit': result[3],
                'equal_credit': result[4]
            })

    df = pd.DataFrame(result_details)
    csv_string = df.to_csv(index=False)

    return result_details, csv_string

    



