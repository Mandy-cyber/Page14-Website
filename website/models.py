from email.policy import default
from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func # func will help us get the current date and time

#--------------------------------------------------------------------
# USER MODEL
#--------------------------------------------------------------------
# TODO set some values as nullable=True


class User(db.Model, UserMixin):
    """ 
    describes a user of the website
    """
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(32)) # first name
    l_name = db.Column(db.String(32)) # last name
    # not setting a limit on length of email bc sometimes 
    # people use e.g Apple to hide their email, which can
    # make it super long
    email = db.Column(db.String(), unique=True)  
    password = db.Column(db.String())
    dob = db.Column(db.String(10)) # date of birth as yyyy-mm-dd
    age = db.Column(db.Integer)
    zipcode = db.Column(db.String(5))
    gender = db.Column(db.String())
    pronouns = db.Column(db.String(10))  # e.g they/them
    sexuality = db.Column(db.String())
    # whether or not they are down for polygamy: 
    # 1 means yes, 0 means no, -1 means maybe
    poly = db.Column(db.Integer)
    passions = db.Column(db.String())
    looking_for = db.Column(db.String())
    fav_book = db.Column(db.String())
    fav_book_auth = db.Column(db.String())
    genre = db.Column(db.String()) # the genre that best describes them
    profile_pic = db.Column(db.String(), nullable=True)
    matches = db.relationship('Matches')



#--------------------------------------------------------------------
# MATCHES MODEL
#--------------------------------------------------------------------

class Matches(db.Model):
    """describes matches that a user has"""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    id_of_match = db.Column(db.Integer) # id of who the user matched with
    rating = db.Column(db.Double) # how good the match is


#--------------------------------------------------------------------
# BOOKQUOTES MODEL
#--------------------------------------------------------------------

class BookQuotes(db.Model):
    """ quotes from users' favorite books"""
    # if i have time then maybe make this class related to User class
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    quote = db.Column(db.String())


#--------------------------------------------------------------------
# CHAT MODEL
#--------------------------------------------------------------------
# this one is a little dubios lol... this is in case i cant figure
# out the proper way to make a private messaging feature

# class Chat(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user1 = db.Column(User)
#     user2 = db.Column(User)
#     user1_msgs = db.Column(db.String())
#     user2_msgs = db.Column(db.String())