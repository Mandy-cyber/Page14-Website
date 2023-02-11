import nltk
import string
import re
from .models import User, Matches

#--------------------------------------------------------------------
# GENDER/SEXUALITY COMPATIBILITY
#--------------------------------------------------------------------
# hardcoding this for now
sex_and_gender = {
                    'hetero': 'opp',
                    'gay': 'same',
                    'lesbian': 'same',
                    'bisexual': 'this or opp',
                    'bicurious': 'this or opp',
                    'pansexual': 'all',
                    'asexual': 'ace',
                    'aromantic': 'ace',
                    'demisexual': 'all',
                    'queer': 'all',
}

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

    # check if they both said either 'yes' or 'maybe' to poly
    this_poly = this_user.poly

    # check they are looking for the same thing
    this_looking_for = this_user.looking_for


    # iterate through list of users
    for p_user in potential_matches:
        
        if (abs(this_age - p_user.age) <= 5) and ():
            print("")
        
        


    # return those that passed all the tests
    return suited_matches