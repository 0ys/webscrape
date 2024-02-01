# scrapetest.py

from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup

def getTitle(url):
    try: 
        html = urlopen(url)
    except HTTPError as e: 
        print(e)
        return None
    except URLError as e:
        print('The server could not be found!')
        return None
    else:
        print('It worked!')
    
    try:
        bs = BeautifulSoup(html, 'html.parser')
        title = bs.body.h1
    except AttributeError as e:
        return None
    return title

title = getTitle('http://pythonscraping.com/pages/page1.html')
if title == None:
    print('Title could not be found')
else:
    print(title)
        
