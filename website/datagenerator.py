import nltk
from nltk.corpus import names
import random
import string

# nltk.download("names")
all_names = names.words("male.txt") + names.words("female.txt")

def generate_email(f_name, l_name):
    """ make an email address from a 
        first and last name.
    Args:
        f_name (str): first name
        l_name (str): last name
    Returns:
        email (str): an email address
    """
    assert f_name != "" or l_name != ""
    email = f_name.lower() + l_name.lower() + "@gmail.com"
    return email

assert generate_email('Amanda', 'Rodriques') == "amandarodriques@gmail.com"
assert generate_email('', 'Rodriques') == "rodriques@gmail.com"
assert generate_email('Amanda', '') == "amanda@gmail.com"
# assert generate_email('', '') == "amanda@gmail.com"


def random_name():
    """ generate a random first and last name

    Returns:
        f_name (str): a first name
        l_name (str): a last name
    """

    f_name = random.choice(all_names)
    l_name = random.choice(all_names)
    return f_name, l_name


def random_bday():
    """ generate a random (valid) birthday

    Returns:
        dob (str): a date of birth in the form
                    yyyy-mm-dd
    """
    dob_year = str(random.randint(1970, 2004))
    dob_month = random.choice(['01', '02', '03', '04', '05', '06', '07'
                               , '08', '09', '10', '11', '12'])
    
    # for my current sake, a month will only have 28 days...
    dob_day = random.randint(1,28)

    # if less than 2 characters need to pad it with a zero
    if len(str(dob_day)) < 2:
        dob_day = f"0{dob_day}"
    else:
        dob_day = str(dob_day)

    # put it all together
    dob = dob_year + "-" + dob_month + "-" + dob_day
    return dob


def calc_age(dob):
    """ calculates the age of someone, only taking 
        into account the year they were born.
    
    Args:
        dob (str): a date of birth in the form
                   yyyy-mm-dd
    Returns
        age (int): age of the person
    """
    year = int(dob[:-6])

    age = 2023 - year
    return age


def random_pass():
    """ generate a very basic password

    Returns:
        password (str): a basic password
    """
    password = ''.join(random.choice(string.ascii_letters) for _ in range(12))
    return password


def random_zipcode():
    """ generate a random zipcode in massachussets

    Returns:
        zipcode (str): 5-digit zip code
    """
    number = random.randint(1001, 2791) # range for MA
    zipcode = f"0{number}"
    return zipcode


def random_gender():
    """ select a random gender

    Returns:
        gender (str): a gender
    """
    gender = random.choice(['female', 'male', 'nb', 'bigender', 'nonc', 'gqueer',
                            'gluid', 'transgender', 'agender', 'intersex', 'twospirit',
                            'thirdsex'])
    return gender


def random_pronoun():
    """ select a random pronoun pair

    Returns:
        pronouns (str): a pronouns pair
    """
    pronouns = random.choice(['she/her', 'he/him', 'they/them', 'zie/zim', 'she/they',
                              'he/they', 'ze/hir', 'xie/hir', 'ze/zir', 've/vis'])
    return pronouns


def random_sexuality():
    """ select a random sexuality

    Returns:
        sexuality (str): a sexuality
    """
    sexuality = random.choice(['hetero', 'gay', 'lesbian', 'bisexual', 'bicurious',
                               'pansexual', 'asexual', 'aromantic', 'demisexual', 'queer'])
    return sexuality


def random_poly():
    poly = random.randint(-1,1)
    return poly


def random_passions():
    passions_list = ['reading', 'writing', 'singing', 'dancing', 'cooking',
                'baking', 'crocheting', 'biking', 'cycling', 'walking',
                'running', 'sports', 'netflix', 'film', 'sleep', 'nature',
                'environment', 'tech', 'youtube', 'toys', 'animals', 'trees',
                'knitting', 'ballet', 'coding', 'programming', 'travelling',
                'fishing']
    
    curr_passions = []
    for x in range(random.randint(1,10)):
        passion = random.choice(passions_list)
        curr_passions.append(passion)
    
    passions = " "
    for c_pass in curr_passions:
        passions = c_pass + ',' + passions

    return passions


def random_looking_for():
    looking_for = random.choice(['fairytale', 'etl', 'frel', 'onebed', 'ftl'])
    return looking_for


def random_book():
    fav_book = random.choice(['The Fifth Season', 'Love After Love', 'The Book of Night Women',
                              'Fangirl', 'Carry On', 'A Court of Thorns & Roses', 
                              'The Love Hypothesis', 'Divergent', 'Twilight', 'One of us is lying'
                              ,'Percy Jackson'])
    return fav_book


def random_author():
    fav_book_auth = random.choice(['Talia Hibbert', 'Rebecca Roanhorse',
                               'Ingrid Persaud', 'Marlon James', 'Kei Miller', 'Leone Ross'
                               'Sarah J Maas', 'Chinua Achebe', 'Rainbow Rowell'])
    return fav_book_auth


def random_genre():
    genre = random.choice(['action', 'adventure', 'romance', 'fantasy', 'horror',
                           'thriller', 'scifi', 'comedy', 'smut', 'hfiction', 'nfiction'])
    return genre