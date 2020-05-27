from urllib.parse import urlparse
from bs4 import BeautifulSoup
from pprint import pprint
import requests

def find_redir_url(url):
    r = requests.get(url,allow_redirects=False)
    try:
        return  fix_relative_url(r.headers["location"],r.url)
    except KeyError:
        pass
    try:
        return fix_relative_url(
        BeautifulSoup(r.text, 'html.parser') \
            .find("meta")["content"] \
            .replace("0; url=","")   \
            .replace("0;URL=", "")   \
            .replace("\"",     "")   \
            .replace('\'',      "")
            ,r.url)
    except KeyError:
        return

    
def fix_relative_url(url,old_host):
    if bool(urlparse(url).netloc):
        return url
    else:
        current_host_parse = urlparse(old_host)
        return current_host_parse.scheme + "://" + current_host_parse.netloc + "/"  + url

def follow_redirects(starting_url):
    urls_redirected = []
    prev_url = find_redir_url(starting_url)
    while prev_url:
        prev_url = find_redir_url(prev_url)
        if prev_url:
            urls_redirected.append(prev_url)
    return urls_redirected
