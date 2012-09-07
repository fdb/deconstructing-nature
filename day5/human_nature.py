import re

import requests
from BeautifulSoup import BeautifulSoup
from simplejson import loads

def extract_id_from_href(href):
    m = re.match(r'res/([0-9]+)#.*', href)
    if m is None:
        return None
    return m.groups()[0]

def latest_threads(board_name='v'):
    response = requests.get('http://boards.4chan.org/%s/' % board_name)
    soup = BeautifulSoup(response.text)
    thread_links = [a for a in soup.findAll() if a.get('href', '').startswith('res')]
    thread_ids = [extract_id_from_href(a['href']) for a in thread_links]
    thread_ids = [id for id in thread_ids if id is not None]
    return list(set(thread_ids))

def fetch_thread(board_name, thread_id):
    response = requests.get('https://api.4chan.org/%s/res/%s.json' % (board_name, thread_id))
    if response.status_code == 200:
        return loads(response.text)

if __name__=='__main__':
    from pprint import pprint
    board = 'r'
    threads = latest_threads(board)
    pprint( fetch_thread(board, threads[0]))

