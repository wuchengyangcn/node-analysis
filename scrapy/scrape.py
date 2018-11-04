#!/usr/bin/env python3
import gevent.monkey
import os
import sys
import requests
import urllib.parse
import logging
import time
import pyquery
import random
import gevent.pool
import gevent.lock
import functools
gevent.monkey.patch_all()
proxies_list = [
    # '101.37.79.125	3128'
    None]
host_url = 'https://scholar.google.com'


def getSession(pool_size=10, retry=3):
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(pool_size, pool_size, retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def request(url, session, refer_url=None, proxies=None):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'en-US,en;q=0.9,zh;q=0.8,zh-TW;q=0.7,zh-CN;q=0.6,ja;q=0.5',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
    }
    if refer_url:
        headers.update({'referer': refer_url})

    for i in range(3):
        try:
            r = session.get(url, headers=headers, timeout=20, proxies=proxies)
        except:
            time.sleep(300)
            continue

        if r.ok:
            response = r.content
            if not response:
                logging.error('Request nothing with proxy: {0}'.format(proxies['https']))
                sys.exit(1)
            return response
        else:
            logging.error('{0} {1} with url: {2}'.format(r.status_code, r.reason, url))
            time.sleep(random.random() * 10)

    sys.exit(1)


def scrapOnePerson(name, session, proxies=None):
    params = {'q': name}
    global host_url
    base_url = host_url + '/scholar'

    url_parts = list(urllib.parse.urlparse(base_url))
    query = urllib.parse.parse_qs(url_parts[4])
    query.update(params)
    url_parts[4] = urllib.parse.urlencode(query)
    url = urllib.parse.urlunparse(url_parts)

    response = request(url, session, host_url, proxies)

    d = pyquery.PyQuery(response)
    next_url_element = d('div.gs_r table a')
    if len(next_url_element) < 1:
        logging.info('scrap no person with name: {0}'.format(name))
        return name
    elif len(next_url_element) > 1:
        logging.info('scrap more than one person with name: {0}'.format(name))
    
    next_url = next_url_element.attr('href')
    next_url = urllib.parse.urljoin(url, next_url)
    time.sleep(random.random() * 10)
    response = request(next_url, session, url, proxies)

    # if not os.path.exists('res'):
    #     os.makedirs('res')
    # with open(os.path.join('res', name + '.html'), 'wb') as fout:
    #     fout.write(response)

    d = pyquery.PyQuery(response)
    total_citation = d('div#gsc_bdy #gsc_rsb_cit table tr:first td:eq(1)').text()
    h_index = d('div#gsc_bdy #gsc_rsb_cit table tr:eq(1) td:eq(1)').text()

    citations = []
    citations_elements = d('div#gsc_bdy #gsc_art table tr td:eq(1) > a:not([class*=gsc_a_acm])')
    citations_elements.each(lambda i, element: citations.append(pyquery.PyQuery(this).text()))

    return '{0}\th_index: {1}\t{2}\t{3}'.format(name, h_index, total_citation, '\t'.join(citations))


def getRequestName():
    all_authors = open('all_author.txt', 'r', encoding='utf-8').readlines()
    if not os.path.exists('result.txt'):
        all_results = []
    else:
        all_results = open('result.txt', 'r', encoding='utf-8').readlines()
        while all_results and all_results[-1].strip() == '':
            all_results = all_results[:-1]

    logging.info('existing result {0}'.format(len(all_results)))

    authors = set()

    for author in all_authors:
        authors.add(author.strip().split('\t')[0])
    for author in all_results:
        authors.discard(author.strip().split('\t')[0])
    return authors


def getProxies():
    global proxies_list
    for i, proxy in enumerate(proxies_list):
        if proxy:
            proxy = 'http://' + ':'.join(proxy.split('\t'))
        proxies_list[i] = {'http': proxy, 'https': proxy}

    return proxies_list


def multiprocess(lock, session, proxies_list, fout, author):
    idx, name = author
    lock.acquire()
    proxies = proxies_list.pop()
    lock.release()

    info = scrapOnePerson(name, session, proxies)

    lock.acquire()
    print(info, file=fout, flush=True)
    proxies_list.append(proxies)
    lock.release()

    logging.info('finish scraping: {0}'.format(name))
    time.sleep(1 + random.random() * 10)

    if idx % 100 == 99:
        time.sleep(random.random() + 30)


def main():
    authors = getRequestName()
    proxies_list = getProxies()
    session = getSession(len(proxies_list) + 5)
    fout = open('result.txt', 'a+', encoding='utf-8')
    pool = gevent.pool.Pool(len(proxies_list))
    lock = gevent.lock.Semaphore()
    func = functools.partial(multiprocess, lock, session, proxies_list, fout)
    pool.map(func, enumerate(authors))


if __name__ == '__main__':
    fileHandler = logging.FileHandler('scrape.log')
    streamHandler = logging.StreamHandler()
    logging.basicConfig(handlers=[fileHandler, streamHandler],
        level=logging.INFO, 
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
    main()
