from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_session import Session
from .models import User, Matches, BookQuotes
from . import db
import nltk
from nltk.corpus import stopwords, names
from nltk.stem import WordNetLemmatizer
import os
from .goodreadscraper import get_quote
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import uuid as uuid
from flask_login import login_user, login_required, logout_user, current_user
import shutil
import string
import re
import random
from .datagenerator import *

# nltk.download('wordnet')
auth = Blueprint('auth', __name__)

#--------------------------------------------------------------------
# GENERATE RANDOM DATA
#--------------------------------------------------------------------

def generate_data():
    for x in range(100):
        names = random_name()
        f_name = names[0]
        l_name = names[1]
        dob = random_bday()
        rando_user = User(f_name=f_name, 
                            l_name=l_name, 
                            email=generate_email(f_name, l_name),
                            dob=dob, 
                            password=generate_password_hash(random_pass(), method='sha256'),
                            age=calc_age(dob), 
                            zipcode=random_zipcode(), 
                            gender=random_gender(),
                            pronouns=random_pronoun(),
                            sexuality=random_sexuality(),
                            poly=random_poly(),
                            passions=random_passions(),
                            looking_for=random_looking_for(),
                            fav_book=random_book(),
                            fav_book_auth=random_author(), 
                            genre=random_genre(), 
                            profile_pic="default.png")
        db.session.add(rando_user)
        db.session.commit()
        print(f"Made {rando_user.f_name}")




#--------------------------------------------------------------------
# MISC STUFF
#--------------------------------------------------------------------

def list_to_string(los):
    """ converts a list into a string
    Args:
        los (list): list of strings
    Returns:
        s (string): a string which is the list
    """
    s = " "
    for str in los:
        if str == None:
            continue
        else:
            s = str + "," + s
    return s


def text_pre_processing(text):
    """ preprocesses text to be used in recommendation engine.
        e.g removes stop words, lemmatizes text, lowercase, etc
    
    Args:
        text (str): text to be processed
    Returns:
        processed_text (list): a list of valuable & formatted words from the text
    """
    # remove numbers
    text = re.sub(r'[0-9]', '', text)

    # remove punctuation 
    text = text.translate(str.maketrans('', '', string.punctuation))

    # lowercase the text
    text = text.lower()

    # remove duplicate spaces + newline characters
    text = " ".join(text.split())

    # remove default stopwords
    stop_words = set(stopwords.words('english'))
    new_text = []

    for word in text.split():
        if word not in stop_words:
            new_text.append(word)
        else:
            continue

    # lemmatization
    # TODO make this better
    lemma = WordNetLemmatizer()
    lemma_text = list()

    for word in new_text:
        word = lemma.lemmatize(word)
        lemma_text.append(word)

    processed_text = lemma_text
    return processed_text




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
    # all_users = User.query.all()
    # for u in all_users:
    #     print(f"Image: {u.profile_pic}")
    # generate_data()

    if request.method == 'POST': 
        
        # get info from form
        email = request.form.get('email')
        password = request.form.get('password')

        # try find associated user
        user = User.query.filter_by(email=email).first()

        #if user (email) actually exists
        if user: 
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                # return redirect(url_for("views.home"))
                return render_template("home.html", user=current_user)
            else:
                flash('Incorrect email or password, try again.', category='error')

        # user with that email doesnt exist
        else: 
            flash('Incorrect email or password, try again.', category='error')

    
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
    # old passions method of doing stuff
    #------------------------------------
    # passions_list = []
        # for x in range(1,5):
        #     try: 
        #         passions_list.append(request.form.get(f"passion{x}"))
        #     except:
        #         continue

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
        passions_list = text_pre_processing(request.form.get("passions"))
        fav_book = request.form.get("fav_book")
        fav_book_auth = request.form.get("fav_book_auth")
        genre = request.form.get("genre")
        looking_for = request.form.get("looking_for")
        zipcode = request.form.get("zipcode")


        # dealing with the profile pic
        #---------------------------------
        profile_pic = request.files['ppic'] # the actual file
        pic_filename = secure_filename(profile_pic.filename)
        # date & time randomizing name of filename so no two users
        # have the same profile pic filename
        pic_name = str(uuid.uuid1()) + "_" + pic_filename
        
        profile_pic.save(pic_name)
        full_file_path = pic_name
        new_file_path = "./website/static/"  + pic_name
        os.rename(full_file_path, new_file_path)


        # seeing if a user exists with the given email
        user = User.query.filter_by(email=email).first()
        if user:
            flash('An account already exists with that email. Try logging in', category='error')
        else:
            # checking validity of inputs
            if len(f_name) < 2 or len(l_name) < 2:
                flash('That name is too short!', category='error')
            elif len(password1) < 8:
                flash("Passwords should be at least 8 characters long.", category='error')
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
                                fav_book=fav_book, fav_book_auth=fav_book_auth, genre=genre, profile_pic=pic_name)
                
                print(list_to_string(passions_list))
                # adding the user to the database
                db.session.add(new_user)
                db.session.commit()

                # # finding a quote from their favorite book which will join
                # # the collection for the homepage
                # # TODO figure out how to not make this take forever
                # if (fav_book != None) and (fav_book_auth != None):
                #     book_name , quote = get_quote(fav_book, fav_book_auth)
                #     if quote != "":
                #         # make a new book quote object
                #         new_quote = BookQuotes(name=book_name, quote=quote)

                #         # adding the book quote to the database
                #         db.session.add(new_quote)
                #         db.session.commit()

                #         # login
                #         login_user(new_user, remember=True)
                #         return redirect(url_for('views.home'))
   
                flash("You're all set!", category='success')
                
                # logging them in and bringing them to the home page
                login_user(new_user, remember=True)
                # return redirect(url_for('views.home'))
                return render_template("home.html", user=current_user)

    return render_template("signup.html")


#--------------------------------------------------------------------
# LOGOUT
#--------------------------------------------------------------------

@login_required
@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    """ where an existing user logs out of the website.
    
    Returns: - home.html (if successful)
             - login.html (if unsuccessful)
    """
    return redirect(url_for('views.landing'))