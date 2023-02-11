from flask import Blueprint, jsonify, render_template, flash, request
from flask_login import login_required, current_user
from .models import User, Matches, BookQuotes
from . import db

views = Blueprint('views', __name__)

#--------------------------------------------------------------------
# LANDING PAGE
#--------------------------------------------------------------------

@views.route('/', methods=['GET', 'POST'])
def landing():
    """ page a user will see for the first time they
        open the site

    Returns: renders landing.html
    """
    return render_template("landing.html")


#--------------------------------------------------------------------
# HOME PAGE
#--------------------------------------------------------------------

@views.route('/home')
@login_required
def home():
    """ the home page of the website
    Returns: renders home.html
    """
    return render_template("home.html", user=current_user)


#--------------------------------------------------------------------
# MATCHES PAGE
#--------------------------------------------------------------------

@views.route('/matches')
@login_required
def matches():
    """ the page where a user can go through all 
        their different potential matches.
    Returns: renders matches.html
    """
    return render_template("matches.html", user=current_user)


#--------------------------------------------------------------------
# MESSAGES PAGE
#--------------------------------------------------------------------

@views.route('/messages', methods=['GET', 'POST'])
@login_required
def messages():
    """ where a user can chat with people they
        have matched with.
    Returns: renders messages.html
    """
    return render_template("messages.html", user=current_user)


#--------------------------------------------------------------------
# PROFILE PAGE
#--------------------------------------------------------------------

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """ where a user can see their profile, and make
        changes/updates to it.
    Returns: renders profile.html
    """
    return render_template("profile.html", user=current_user)