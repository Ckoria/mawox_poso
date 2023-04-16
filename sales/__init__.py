#Python Modules
from flask import Flask
from flask_wtf.csrf import CSRFProtect
#Own Modules
from .exts import db, login_manager, bcrypt
from .blueprints.dashboard import dash
from .blueprints.accounts import account
from .blueprints.customers import customers
from .routes import main
from .forms import Register_form

#Creates Flask app
app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sales_data.db'
app.config.update(dict(
    SECRET_KEY="ghsdabbjvslksagy12sagh515d*-fb#", WTF_CSRF_SECRET_KEY="ghsdabbjvslksagy12sagh515d*-fb#"
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
from sales import routes
""" with app.app_context():
        db.create_all() """
