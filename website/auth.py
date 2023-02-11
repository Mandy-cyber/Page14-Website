from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Matches, BookQuotes
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

def list_to_string(los):
    """ converts a list into a string
    Args:
        los (list): list of strings
    Returns:
        s (string): a string which is the list
    """
    str1 = ""
    s = str1.join(los)
    return s

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
    # this current year. will replace with automatic time func later
    this_yr = 2023


    if request.method == 'POST':
        # getting input from forms
        f_name = request.form.get("f_name")
        l_name = request.form.get("l_name")
        dob = request.form.get("dob")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        pronouns = request.form.get("pronouns")
        gender = request.form.get("gender")
        sexuality = request.form.get("sexuality")
        poly = request.form.get("poly")
        
        passions_list = []
        for x in range(1,5):
            passions_list.append(request.form.get(f"passion{x}"))

        fav_book = request.form.get("fav_book")
        fav_book_auth = request.form.get("fav_book_auth")
        genre = request.form.get("genre")
        looking_for = request.form.get("looking_for")
        zipcode = request.form.get("zipcode")
        profile_pic = request.form.get("ppic")
        if profile_pic == None: 
            profile_pic = "default.png" 
        else: 
            profile_pic = profile_pic
        
        # checking validity of inputs
        # seeing if a user exists with the given email
        user = User.query.filter_by(email=email).first()
        if user:
            flash('An account already exists with that email. Try logging in', category='error')
        else:
            if len(f_name) < 2 or len(l_name) < 2:
                flash('That name is too short!', category='error')
            elif password1 != password2:
                flash("Hmmm, passwords don't match. Try again.", category='error')
            elif len(zipcode) != 5:
                flash('Yikes, invalid zipcode. It should be 5 digits long.', category='error')
            elif (this_yr - int(dob[:-6])) < 18:
                flash("You're a bit *too* young to be chillin' round these parts...", category='error')
            else:
                # constructing new user
                new_user = User(f_name=f_name, l_name=l_name, dob=dob, age=(this_yr- int(dob[:-6])),
                                email=email, password=generate_password_hash(password1, method='sha256'),
                                zipcode=zipcode, gender=gender, pronouns=pronouns, sexuality=sexuality,
                                poly=poly, passions=list_to_string(passions_list), looking_for=looking_for,
                                fav_book=fav_book, fav_book_auth=fav_book_auth, genre=genre, profile_pic=profile_pic)
                
                # adding them to the database
                db.session.add(new_user)
                db.session.commit()
                flash("You're all set!", category='success')
                print("Success")
                
                # logging them in and bringing them to the home page
                login_user(user, remember=True)
                return redirect(url_for('views.home'))

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