from nltk.corpus import wordnet as wn
import string
import re
from models import User, Matches
from __init__ import db
from werkzeug.security import generate_password_hash, check_password_hash
import pprint

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



#--------------------------------------------------------------------
# TOP 5 SYNONYMS
#--------------------------------------------------------------------
# not sure how to write tests for this 

def five_synonyms(word):
    """ get five synonyms of the given word

    Args:
        word (str): word to find synonyms of
    Returns:
        five_syns (set): set of five synonyms
                         of the word
    """
    # below code from nltk documentation website and 
    # https://www.holisticseo.digital/python-seo/nltk/wordnet
    synonyms = []

    for syn in wn.synsets(word):
        for i in syn.lemmas():
            synonyms.append(i.name())

    five_syns = set(synonyms) #make it a set so no repeats
    return five_syns



#--------------------------------------------------------------------
# SIMILARITY IN PASSIONS
#--------------------------------------------------------------------
# not sure how to write tests for this 

# TODO figure out the scaling problem for this
def passion_similarity(passions1, passions2):
    """ calculate how similar two users' passions are
        on an ascending scale of 0 to 1.

    Args:
        passions1 (str): a User's passions
        passions2 (str): another User's passions

    Returns
        similarity_idx (double): how similar their passions are
    """
    # turn passions into list for iteration sake
    # first turn to set to remove duplicate words
    passions1 = list(set(passions1.split(',')))
    passions2 = list(set(passions2.split(',')))

    # if the lists happen to be the same
    if passions1 == passions2:
        similarity_idx = 1
        return similarity_idx
    
    # if there is a list with no passions
    elif (passions1 == list()) or (passions2 == list()):
        similarity_idx = 0
        return similarity_idx
    
    # if the lists are not exactly the same
    else:
        # expand the second (could have also been the first)
        # list to include synonyms of each word
        expanded_passions2 = []
        for p2 in passions2:
            five_syns = list(five_synonyms(p2)) # convert set to list
            for syn in five_syns:
                expanded_passions2.append(syn)

        # check how many passions from passions1 are seen in
        # the expanded passions2 list
        num_shared = 0
        for p1 in passions1:
            if p1 in expanded_passions2:
                num_shared += 1
            else:
                continue

            
        # similarity rating = num of similar / total amount before expansion (?)
        similarity_idx = num_shared / (len(passions1) + len(passions2))
        print(f"Num Shared: {num_shared}") 
        print(f"Similarity Index: {similarity_idx}")
        return similarity_idx


# passion_similarity(user_2.passions, user_3.passions)


#--------------------------------------------------------------------
# BONUS FOR RATING
#--------------------------------------------------------------------

def bonus_amount(user1, user2):
    """ additional points to match rating if two
        users share the same favorite book or author

    Args:
        user1 (User): a User
        user2 (User): another User
    Returns
        bonus (double): additional points
    """
    # getting info from objects
    fav_book1 = user1.fav_book
    fav_book2 = user2.fav_book
    fav_auth1 = user1.fav_book_auth
    fav_auth2 = user2.fav_book_auth

    info = [fav_book1, fav_book2, fav_auth1, fav_auth2]
    btr_info = []
    
    # editing the text since some people
    # might type the same thing differently
    for i in info:
        i = i.translate(str.maketrans('', '', string.punctuation)) # remove punctuation
        i = i.lower() # make lowercase
        i = " ".join(i.split()) # remove unnecessary whitespaces and newlines
        btr_info.append(i)


    # check if they share favorite book
    if btr_info[0] == btr_info[1]:
        # 5% extra
        bk_bonus = 0.05
    else:
        bk_bonus = 0 


    # check if they share favorite author
    if btr_info[2] == btr_info[3]:
        # 7% extra
        au_bonus = 0.07
    else:
        au_bonus = 0 

    bonus = bk_bonus + au_bonus
    return bonus


#--------------------------------------------------------------------
# MAKE MATCH
#--------------------------------------------------------------------
# no serious math behind these number options. just examples for now.

def make_matches(user):
    """ add matches (i.e show them a person) if they pass
        certain criteria determined by 'looking_for' field.
        - fairytale = add if rating is 0.7 or above
        - enemies-to-lovers = add if low match rating
        - fake relationship = add if rating is 0.6 or above
        - one bed = add if rating is 0.5 or above
        - friends-to-lovers = add if rating is 0.8 or above

    Args:
        user (User): the user we are finding matches for
    Returns:
        matches (list of Matches): matches the user has
    """
    # in the future i won't query the entire database for matches
    # since that would get impractical as it upscales. for now
    # it is fine since the volume is small
    all_users = User.query.all() # TODO remove this user from this
    print(len(all_users))
    user_passions = user.passions
    user_desire = user.looking_for

    # matches that pass all the filters
    suited_matches = filter_out_matches(user, all_users)

    # get the match_rating for each match
    match_rating_dict = dict()

    for suitor in suited_matches:
        similarity_idx = passion_similarity(user_passions, suitor.passions)
        bonus = bonus_amount(user, suitor)
        total_rating = similarity_idx + bonus
        if total_rating > 1:
            match_rating_dict[suitor] = 1
        else:
            match_rating_dict[suitor] = total_rating

    less_than_val = 1

    # condition based on user_desire
    if user_desire == 'fairytale':
        greater_than_val = 0.7
    elif user_desire == 'etl':
        greater_than_val = 0
        less_than_val = 0.5 # override value just for this case
    elif user_desire == 'frel':
        greater_than_val= 0.6
    elif user_desire == 'onebed':
        greater_than_val = 0.5
    else:
        greater_than_val = 0.8
    

    # use the condition to add new matches
    # key = User class  , value = rating
    for suitor, rating in match_rating_dict.items():
        if less_than_val <= rating <= greater_than_val:
            new_match = Matches(user_id=user.id, id_of_match=suitor.id,
                                rating=rating)
            db.session.add(new_match)
            db.session.commit()
            print(f"Match added between you and {suitor.f_name}")
        else:
            continue
        

#--------------------------------------------------------------------
# EXAMPLES
#--------------------------------------------------------------------
# examples of users -- not saved to database

user_1 = User(f_name="Manda", l_name="Ro", email="manda@gmail.com",
              password=generate_password_hash("randopasso", method='sha256'),
              dob="2004-02-01", age=19, zipcode=00000, gender="female",
              pronouns="she/her", sexuality="bisexual", poly=1, 
              passions="reading,writing,coding,baking", looking_for="fairytale",
              fav_book="Take a hint dani brown", fav_book_auth="Talia hibbert", genre="romance",
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
              passions="writing,coding,baking,soccer,videogames", looking_for="fairytale",
              fav_book="Rage of dragons", fav_book_auth="Evan winters", genre="horror",
              profile_pic="default.png")

