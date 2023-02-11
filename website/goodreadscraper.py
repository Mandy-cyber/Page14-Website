from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def get_quote(book, author):
    """ get a quote from a given book via goodreads

    Args:
        book (str): name of the book
        author (str): name of the book's author
    
    Returns:
        book_name (str): the book's full name including
                         the author's name
        quote (str): a quote from the book
    """
    # SETTING UP BROWSER
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(options=chrome_options)
    chrome_options.add_argument("--log-level=3")

    # goodreads quote links follow the same structure
    # (see below this function) so I am just reformatting
    # the text to fit that
    author = "by " + author
    all_words = book.lower().split() + author.lower().split()
    formatted_text = "+".join(all_words)

    # navigating to page and getting the first quote
    browser.get(f"https://www.goodreads.com/quotes/search?utf8=%E2%9C%93&q={formatted_text}&commit=Search")
    try:
        quote = browser.find_element(By.CLASS_NAME, "quoteText")
        quote = quote.text
    except:
        quote = ""

    book_name = book + " by " + author
    return book_name, quote



"""
EXAMPLES OF LINKS TO GOODREADS QUOTES
---------------------------------------
https://www.goodreads.com/quotes/search?utf8=%E2%9C%93&q=get+a+life+chloe+brown&commit=Search
https://www.goodreads.com/quotes/search?utf8=%E2%9C%93&q=get+a+life+chloe+brown+by+talia+hibbert&commit=Search
https://www.goodreads.com/quotes/search?utf8=%E2%9C%93&q=the+fifth+season+by+nk+jemisin&commit=Search

"""