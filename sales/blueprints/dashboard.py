#Python Modules
from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_required, current_user
from datetime import datetime
#Own Modules

#To display Business perfomance visuals
dash = Blueprint('dashboard', __name__)
@dash.route('/dashboard')
@login_required
def dashboard():
    return render_template('acc.html', 
                            Curr_Date_Time= (datetime.now()).strftime("%c") )