import requests
from lxml import html
from time import sleep
from random import random


def crawl(oid):
    first = 'https://scholar.uulucky.com/citations?view_op=view_org&hl=zh-CN&org='+oid
    while True:
        try:
            page = requests.get(first, timeout=30)
        except:
            continue
        if page.status_code == 200:
            break
        print(page.status_code)
        sleep(60+random())
    tree = html.fromstring(page.text)
    org = tree.xpath('//*[@id="gsc_sa_ccl"]/h2')
    name = org[0].text
    file = ''.join(name.split(' ')).lower()
    after, start = parse(page, file)
    while True:
        if after == -1 and start == -1:
            break
        sleep(6+random()*4)
        url = first+'&after_author='+after+'&astart='+start
        while True:
            try:
                page = requests.get(url, timeout=30)
            except:
                continue
            if page.status_code == 200:
                break
            print(page.status_code)
            sleep(60 + random())
        after, start = parse(page, file)

def parse(page,file):
    tree = html.fromstring(page.text)
    outfile = open(file+'.txt', 'a')
    end = 0
    for i in range(2, 12):
        try:
            label = tree.xpath('//*[@id="gsc_sa_ccl"]/div['+str(i)+']/div/h3/a')
            link = label[0].attrib['href']
            uid = link.split('&')[0].split('=')[1]
            print(uid)
            outfile.write(uid+'\n')
        except:
            end = 1
            break
    outfile.close()
    try:
        button = tree.xpath('//*[@id="gsc_authors_bottom_pag"]/div/button[2]')
        click = button[0].attrib['onclick']
        click = click[click.find('after_author')+len('after_author')+4:-1]
        after = click[:click.find("\\")]
        start = click[click.find("\\x3d")+4:]
    except:
        end = 1
    if end:
        return -1, -1
    return after, start


oids = ['1234567890']
for oid in oids:
    crawl(oid)