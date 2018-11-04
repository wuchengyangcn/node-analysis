import os
import re
import sys
import time
import logging
import requests
import urllib.parse
from pyquery import *

def updateQuery(base_url, num):
    params = {'pos': num}
    url_parts = list(urllib.parse.urlparse(base_url))

    query = urllib.parse.parse_qs(url_parts[4])
    query.update(params)
    url_parts[4] = urllib.parse.urlencode(query)
    url = urllib.parse.urlunparse(url_parts)

    return url

def getAuthorName(response, filemode):
    d = pyquery.PyQuery(response)
    res = []
    d('#browse-person-output > div > div > ul > li > a').each(
        lambda i, element: res.append(pyquery.PyQuery(this).text())
    )
    if res:
        with open('result.txt', filemode, encoding = 'utf-8') as fout:
            print('\n'.join(res), file = fout)
    return len(res)

if __name__ == '__main__':
    fileHandler = logging.FileHandler('scrape.log')
    streamHandler = logging.StreamHandler()
    logging.basicConfig(handlers = [fileHandler, streamHandler],
        level=logging.INFO, 
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    sess = requests.Session()
    base_url = 'https://dblp.uni-trier.de/pers'
    i = 1

    if os.path.exists('result.txt'):
        with open('result.txt', 'r', encoding = 'utf-8') as fin:
            i = len(fin.readlines()) + 1

    logging.info('Existing result {0}'.format(i))

    newAuthor = 1
    while newAuthor > 0:
        url = updateQuery(base_url, i)
        r = sess.get(url, timeout = 20)
        if r.ok:
            newAuthor = getAuthorName(r.content, 'a')
            i += newAuthor
        else:
            logging.error('http request error with {0} at i: {1}'.format(r.status_code, i))
            sess = requests.Session()
            time.sleep(10)