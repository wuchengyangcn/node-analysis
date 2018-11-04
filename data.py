import requests
from time import sleep
from random import *
from lxml import html

def data(file):
    try:
        finished = int(open(file+'data.txt', 'r').readlines()[-1].split(' ')[0])
    except:
        finished = 0
    count = finished
    for line in open(file+'.txt', 'r').readlines()[finished:]:
        count += 1
        print(count)
        sleep(6+random()*4)
        agents = ['scholar.90h6.cn:1668']
        url = 'https://'+sample(agents,1)[0]+'/citations?user='+line.strip()+'&hl=zh-CN'
        fail = 0
        while fail < 10:
            try:
                page = requests.get(url, timeout=30)
            except:
                continue
            if page.status_code == 200:
                break
            print(page.status_code)
            fail += 1
            sleep(60+random())
        if fail == 10:
            continue
        tree = html.fromstring(page.text)
        name_label = tree.xpath('//*[@id="gsc_prf_in"]')
        name = name_label[0].text
        print(name)
        first_ten = []
        for i in range(1, 11):
            try:
                cite_label = tree.xpath('//*[@id="gsc_a_b"]/tr['+str(i)+']/td[2]/a')
                first_ten.append(cite_label[0].text)
            except:
                break
        if len(first_ten) < 10:
            continue
        for i in range(len(first_ten)):
            if not first_ten[i]:
                first_ten[i] = '0'
        total_label = tree.xpath('//*[@id="gsc_rsb_st"]/tbody/tr[1]/td[2]')
        total = total_label[0].text
        h_label = tree.xpath('//*[@id="gsc_rsb_st"]/tbody/tr[2]/td[2]')
        h_index = h_label[0].text
        open(file+'data.txt', 'a').write(str(count)+' '+name+' '+h_index+' '+total+' '+' '.join(first_ten[:5])+'\n')


filename = ['cityuniversityofhongkong']
for file in filename:
    data(file)
