from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, DateField
from wtforms.validators import InputRequired, Email, Length, Optional

class UserRegistrationForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(max=20)])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email (Optional)", validators=[Optional(), Email(), Length(max=50)])

class UserLoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(max=20)])
    password = PasswordField("Password", validators=[InputRequired()])

class ParagraphForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(), Length(max=100)])
    public = BooleanField("Public")
    content = TextAreaField("Content", validators=[InputRequired(), Length(max=500)])

class SearchDateForm(FlaskForm):
    date = DateField("Or search for paragraphs by date (MM/DD/YYYY)", format='%m/%d/%Y')
    
