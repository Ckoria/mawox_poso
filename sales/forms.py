from flask_wtf import FlaskForm
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from wtforms import StringField, PasswordField, SubmitField
from .models.users import Users

class Register_form(FlaskForm):
    def validate_username(self, username_to_check):
        user = Users.query.filter_by(username= username_to_check.data).first()
        if user:
            raise ValidationError("Ooops, the username address already exists! Try a different one." )
        
    def validate_email(self, email_to_check):
        email = Users.query.filter_by(email= email_to_check.data).first()
        if email:
            raise ValidationError("Ooops, an email address already exists! Try a different one." )
    #Creating a Form 
    username = StringField(label= 'Username:', validators= [Length(min=2, max=30), DataRequired()])
    email = StringField(label= 'Email:', validators=[Email(), DataRequired()])
    pwd_1 = PasswordField(label= 'Password: ', validators=[Length(min=8, max=60), DataRequired()])
    passwords = PasswordField(label= 'Confirm Password: ', validators=[ EqualTo('pwd_1'), DataRequired()])
    submit = SubmitField(label= 'Create Account')
  
class Login_form(FlaskForm):
    #Creating a Form
    username = StringField(label= 'Username', validators=[DataRequired()])
    pwd_1 = PasswordField(label= 'Password', validators=[DataRequired()])
    submit = SubmitField(label= 'Sign in')
    

