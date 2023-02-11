from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Matches, BookQuotes
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

#--------------------------------------------------------------------
# LOGIN PAGE
#--------------------------------------------------------------------

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """ where an existing user logs in to the website.

    Requeries if:
        - invalid/nonexistent email
        - wrong password
    
    Returns: - home.html (if successful)
             - login.html (if unsuccessful)
    """
    return render_template("login.html")


#--------------------------------------------------------------------
# SIGNUP PAGE
#--------------------------------------------------------------------

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    """ where a new user signs up for the website.

    Requeries if:
        - first and/or last name is too short
        - email already exists or is invalid
        - passwords do not match
        - age is too young
        - required fields not filled in
    
    Returns: - home.html (if successful)
             - signup.html (if unsuccessful)
    """
    return render_template("signup.html")


#--------------------------------------------------------------------
# LOGOUT
#--------------------------------------------------------------------

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """ where an existing user logs out of the website.
    
    Returns: - home.html (if successful)
             - login.html (if unsuccessful)
    """
    return redirect(url_for('views.landing'))