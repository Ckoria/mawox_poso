
from dotenv import load_dotenv
import os
import base64
from download_creds import download_file_from_google_drive

current_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else os.getcwd()
url = f"https://drive.google.com/file/d/1_f_v7c133PzVKCG6SDsyVYYrFqCNZ6uc/view?usp=sharing"
download_file_from_google_drive(url, current_dir +"\.env")

# ----------------------------------------------------- APP STARTS HERE -------------------------------------------------

#Python Modules
from flask import Flask
from flask_wtf.csrf import CSRFProtect
#Own Modules
from .extensions import db, login_manager, bcrypt
from .blueprints.dashboard import dash
from .blueprints.accounts import account
from .blueprints.customers import customers
from .routes import main
from .forms import Register_form


def generate_random_base64_key(length=32):
    return base64.urlsafe_b64encode(os.urandom(length)).decode('utf-8').rstrip('=')


#SECRETE_KEYS
# Load environment variables from .env file
load_dotenv()

SECRET_KEY= generate_random_base64_key(24)           #os.getenv("SECRET_KEY")
WTF_CSRF_SECRET_KEY= generate_random_base64_key(24)  #os.getenv("WTF_CSRF_SECRET_KEY")
#Creates Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE")
app.config.update(dict(
    SECRET_KEY= SECRET_KEY, WTF_CSRF_SECRET_KEY= WTF_CSRF_SECRET_KEY
    ))
@app.context_processor
def base():
    form = Register_form()
    return dict(form= form)
#Generate CSRF Token to encrypt URLs
csrf = CSRFProtect()
csrf.__init__(app)

#Register Blueprints
app.register_blueprint(main)
app.register_blueprint(dash)
app.register_blueprint(account)
app.register_blueprint(customers)

#For password encryption
#bcrypt = Bcrypt(app)

db.init_app(app)

#Manages Logins
login_manager.init_app(app)
#For password hashing
bcrypt.init_app(app)


