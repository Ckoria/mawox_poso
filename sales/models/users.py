from ..exts import db, login_manager, bcrypt
from sqlalchemy import create_engine, ForeignKey, String, Integer, Column, CHAR
from flask_login import UserMixin

login_manager.login_view = 'main.login_page'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

#Users Registration Database
class Users(db.Model, UserMixin):
    #Creating a Database for Users
    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(length=30), nullable = False, unique = True)
    email = db.Column(db.String(length= 30), nullable = False, unique = True)
    pwd_hash = db.Column(db.String(), nullable = False)
    
    @property
    def password(self):
        return self.password
    #Responsible for password encryption
    @password.setter
    def password(self, plain_txt_pwd):
        self.pwd_hash = bcrypt.generate_password_hash(plain_txt_pwd).decode('utf-8')
        
    def check_password_correction(self, pwd_attempt):
        return bcrypt.check_password_hash(self.pwd_hash, pwd_attempt)


