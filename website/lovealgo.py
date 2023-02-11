import nltk
import string
import re
from models import User, Matches
from __init__ import db
from werkzeug.security import generate_password_hash, check_password_hash

#--------------------------------------------------------------------
# GENDER/SEXUALITY COMPATIBILITY
#--------------------------------------------------------------------
# hardcoding this for now

def compatible_with(gender, sexuality):
    """ which genders is this gender compatible with
        based on the sexuality.

    Args:
        gender (str): the gender
        sexuality (str): the sexuality
    
    Returns
        genders (list of str): list of compatible genders
    """
    # heterosexuals
    if sexuality == 'hetero':
        if gender == 'male':
            genders = ['female']
        elif gender == 'female':
            genders = ['male']
        else:
            genders = list()

    # gay & lesbian
    elif sexuality in ['gay', 'lesbian']:
        if gender == 'male':
            genders = ['male']
        elif gender == 'female':
            genders = ['female']
        else:
            genders = list()

    # bisexual & bicurious
    elif sexuality in ['bisexual', 'bicurious']:
        if gender in ['male', 'female']:
            genders = ['female', 'male']
        else:
            genders = list()

    # pansexual, demisexual, asexuals, aromantics, & queer
    # elif sexuality in ['pansexual', 'demisexual', 'queer', 'asexual', 'aromantic']:
    else:
        genders = ['female', 'male', 'nb', 'bigender', 'nonc',
                   'gqueer', 'gfluid', 'transgender', 'agender',
                   'intersex', 'twospirit', 'thirdsex']
        
    return genders
    

#--------------------------------------------------------------------
# POLY TEST
#--------------------------------------------------------------------

def same_poly_view(answ1, answ2):
    """ do both answers share the same view on polygamy
        * both yes, both no, both maybe, or one yes the other maybe
    
    Args:
        answ1 (int): 1 = yes, 0 = no, -1 = maybe
        answ2 (int): 1 = yes, 0 = no, -1 = maybe

    Returns:
        same_view (bool): do they share the same view
    """

    same_view = ((answ1 == answ2) or abs(answ1 - answ2) == 2)
    return same_view


#--------------------------------------------------------------------
# FILTER USERS
#--------------------------------------------------------------------
# yes, i know i should make this into a class method but
# im confused how that works when my class attributes are
# actually columns in a database? 
def filter_out_matches(this_user, potential_matches):
    """ filter out potential matches if they do not share
        the same 'base' features.

    Args:
        this_user (User): the user whose standards we are
                          using in the filtering process
        potential_matches (list of User): potential matches
                                          we are filtering
                                          through.

    Returns:
        suited_matches (list of User): users who pass the given
                                       filters/standards.
    """
    suited_matches = []

    # Will:
    #---------
    # check age difference within 5 years - later feature for silver foxes ;)
    this_age = this_user.age

    # TODO figure out the whole zipcode situation
    # # check within 20 miles of each other
    # this_zipcode = this_user.zipcode

    # check gender compatibility based on sexuality
    this_gender = this_user.gender
    this_sexuality = this_user.sexuality
    compatible_genders = compatible_with(gender=this_gender, sexuality=this_sexuality)

    # check if they both said either 'yes' or 'maybe' to poly
    this_poly = this_user.poly

    # check they are looking for the same thing
    this_looking_for = this_user.looking_for

    # iterate through list of users
    for p_user in potential_matches:
        
        if (abs(this_age - p_user.age) <= 5) \
            and (p_user.gender in compatible_genders) \
            and same_poly_view(this_poly, p_user.poly) \
            and (this_looking_for == p_user.looking_for):

            suited_matches.append(p_user)

    return suited_matches


# examples of users -- not saved to database
user_1 = User(f_name="Manda", l_name="Ro", email="manda@gmail.com",
              password=generate_password_hash("randopasso", method='sha256'),
              dob="2004-02-01", age=19, zipcode=00000, gender="female",
              pronouns="she/her", sexuality="bisexual", poly=1, 
              passions="reading,writing,coding,baking", looking_for="fairytale",
              fav_book="The Fifth Season", fav_book_auth="NK Jemisin", genre="romance",
              profile_pic="default.png")

user_2 = User(f_name="Lola", l_name="Ley", email="lola@gmail.com",
              password=generate_password_hash("randopassotasso", method='sha256'),
              dob="2002-01-31", age=21, zipcode=10010, gender="gfluid",
              pronouns="she/they", sexuality="bicurious", poly=-1, 
              passions="football,reading,gaming", looking_for="fairytale",
              fav_book="Get a life chloe brown", fav_book_auth="Talia Hibbert", genre="comedy",
              profile_pic="default.png")

user_3 = User(f_name="Joe", l_name="Johnson", email="joejo@gmail.com",
              password=generate_password_hash("randopassotassolasso", method='sha256'),
              dob="2000-12-05", age=23, zipcode=21, gender="male",
              pronouns="he/him", sexuality="hetero", poly=1, 
              passions="tv,film,hiking", looking_for="fairytale",
              fav_book="Rage of dragons", fav_book_auth="Evan winters", genre="horror",
              profile_pic="default.png")

