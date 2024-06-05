from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SearchSchoolForm(FlaskForm):
    school_name = StringField('School_name', validators=[DataRequired()]) # This is basically saying that we are trying to get entry regarding the name of the school
    submit = SubmitField('Find School')