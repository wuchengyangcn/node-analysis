import seaborn as sb
import matplotlib.pyplot as plt
name = 'zhejianguniversitydata'
cite_ratio = []
h_index = []
for line in open(name+'.txt', 'r', encoding='utf-8').readlines():
    items = line.strip().split()
    c1 = int(items[-1])
    c2 = int(items[-2])
    c3 = int(items[-3])
    c4 = int(items[-4])
    c5 = int(items[-5])
    total = int(items[-6])
    if c1+c2+c3+c4+c5 > total:
        continue
    cite_ratio.append((c1+c2+c3+c4+c5)/total)
    h_index.append(int(items[-7]))
sb.kdeplot(cite_ratio, h_index)
plt.xlabel('cite_ratio')
plt.ylabel('h_index')
plt.title(name[:-4])
plt.xlim(0, 1)
plt.ylim(0, 40)
plt.savefig(name[:-4]+'_cite.png', dpi=300)
plt.close()

sb.distplot(cite_ratio, bins=100)
plt.xlabel('cite_ratio')
plt.title(name[:-4])
plt.xlim(0, 1)
plt.ylim(0, 2.25)
plt.savefig(name[:-4]+'_h.png', dpi=300)
plt.close()
