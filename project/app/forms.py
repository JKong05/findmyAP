from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, Length, ValidationError
from app.models import User

class submitTempData(FlaskForm):
    course_name = TextAreaField('Course Name', validators=[DataRequired()])
    ap_score = SelectField('Score', choices=[(str(i), str(i)) for i in range(1, 6)], validators=[InputRequired()])
    submit = SubmitField('Submit')

class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Sign up")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username = username.data).first()
        if existing_user_username:
            raise ValidationError("That username already exists. Please choose a different one!")

class SignInForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Sign in")
