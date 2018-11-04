import os
import sys
import random

field = ''
if len(sys.argv) > 1:
    field = sys.argv[1] + '_'

with open(field + 'result.txt', 'r', encoding = 'utf-8') as fin:
    lines = fin.readlines()

skip = 0
num = 0
percentage = dict()

for i, line in enumerate(lines):
    line = line.strip().split('\t')
    author = line[0]
    if len(line) < 2:
        skip += 1
        continue
    num += 1
    h_index = 0
    if line[1].startswith('h_index'):
        h_index_num = line[1].split(':')[-1]
        h_index = int(h_index_num if h_index_num else 0)
        line = line[0:1] + line[2:]
    new_line = []
    for l in line[1:]:
        if l[-1] == '*':
            l = l[:-1]
        new_line.append(int(l))
    line = new_line
    if not line:
        continue
    if len(line) > 10:
        per = 0
        for p in line[1:6]:
            per += p
        percentage[author] = (per / line[0], h_index)

print(len(percentage))

# import pickle

# try:
#     with open('first.pkl', 'rb') as fin:
#         percentage.update(pickle.load(fin))
# except:
#     pass

# with open('first.pkl', 'wb') as fout:
#     pickle.dump(percentage, fout)
#     sys.exit(0)


import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn.neighbors
import pandas as pd
import scipy as sp

X = list(percentage.values())
# X = random.sample(X, 200)
x = []
y = []
xx= []

for a in X[:]:
    x.append(a[0])
    y.append(a[1])
    xx.append(1 / a[0])

data = pd.DataFrame(data = {'1 / cite ratio': xx, 'h index': y})



# sns.lmplot('1 / cite ratio', 'h index', data, ci = None, robust = False, lowess=True, scatter_kws={"s": 1}, line_kws={'color': 'black'})

# ax = sns.kdeplot(x, y)
# # ax = plt.gca()
# ax.set_ylim(0, 60)
# ax.set_xlim(0, 1)
# ax.set_xlabel('cite ratio')
# ax.set_ylabel('h index')
# plt.title(field[:-1])

# plt.savefig(field + 'h_index.png', dpi = 300)
# plt.show()
# plt.clf()



# for den in [50, 100]:
#     ax = sns.distplot(x, bins = den)
#     ax.set_xlabel('cite ratio')

#     plt.title(field[:-1])

#     plt.savefig(field + 'cite_{0}.png'.format(den), dpi = 300)
#     plt.show()
#     plt.clf()



# x = pd.Series(x)
# print('均值\t方差\t偏度\t峰度')
# print('{:.4f}\t{:.4f}\t{:.4f}\t{:.4f}'.format(x.mean(), x.var(), x.skew(), x.kurt()))
# print(data.corr())