import re
import os
from time import sleep
from random import randint
from StringIO import StringIO

import requests
from BeautifulSoup import BeautifulSoup
from simplejson import loads
from PIL import Image
from pymongo import Connection, DESCENDING
from pymongo.database import Database

connection = Connection()
db = Database(connection, '4chan')

def extract_id_from_href(href):
    m = re.match(r'res/([0-9]+)#.*', href)
    if m is None:
        return None
    return m.groups()[0]

def latest_thread_ids(board_name='v', page_number='0'):
    response = requests.get('http://boards.4chan.org/%s/%s' % (board_name, page_number))
    soup = BeautifulSoup(response.text)
    thread_links = [a for a in soup.findAll() if a.get('href', '').startswith('res')]
    thread_ids = [extract_id_from_href(a['href']) for a in thread_links]
    thread_ids = [id for id in thread_ids if id is not None]
    return list(set(thread_ids))

def fetch_thread(board_name, thread_id, force_fetch=True):
    thread = db.threads.find_one({'id': thread_id})
    if thread is not None and not force_fetch:
        return thread

    response = requests.get('https://api.4chan.org/%s/res/%s.json' % (board_name, thread_id))
    response.raise_for_status()
    thread = loads(response.text)
    thread['board'] = board_name
    thread['id'] = thread_id
    db.threads.remove({'id': thread_id})
    db.threads.save(thread)
    return thread


def save_threads(board_name='r'):
    sleep(1)
    thread_ids = latest_thread_ids(board_name, randint(0, 10))
    for thread_id in thread_ids:
        if db.threads.find_one({'id': thread_id}):
            print "Thread %s already fetched." % thread_id
            continue
        sleep(2)
        try:
            thread = fetch_thread(board_name, thread_id)
            if thread is not None:
                t = thread.get('posts', [])[0]
                if t is not None:
                    print thread_id, t.get('com')[:100]
                db.threads.save(thread)
        except: 
            print "Thread %s not found" % thread_id
            pass
    
def save_images(board_name, thread_id):
    thread = fetch_thread(board_name, thread_id)
    for post in thread['posts']:
        image_url = 'http://images.4chan.org/%s/src/%s%s' % (board_name, post['tim'], post['ext'])
        print image_url
        try:
            r = requests.get(image_url)
            img = Image.open(StringIO(r.content))
            img.save('images/%s%s' % (post['tim'], post['ext']))
        except:
            print "Post 404: %s" % post['tim']
            continue
        sleep(2)

if __name__=='__main__':
    try:
        os.mkdir('images')
    except OSError:
        pass
    board_name = 'mlp'
    while True:
        thread_ids = latest_thread_ids(board_name, randint(0, 10))
        for thread_id in thread_ids:
            try:
                save_images(board_name, thread_id)
            except:
                print "Thread 404 %s" % thread_id
            sleep(5)
