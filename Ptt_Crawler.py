
# coding: utf-8

# In[52]:

import requests
from bs4 import BeautifulSoup
from datetime import date,datetime
import re


# In[53]:

def pageDetail(detailurl):
    res = requests.get(detailurl)
    soup = BeautifulSoup(res.text, 'html.parser')
    i = 1
    push = ""
    
    if len(soup.select('#main-content')[0].contents) > 4:
        # 抓取內文
        summary = soup.select('#main-content')[0].contents[4]
        # 抓取時間
        time = soup.select('.article-meta-value')[3].text
        dt =datetime.strptime(time, '%a %b %d %H:%M:%S %Y')
        
        if (len(soup.select('#main-content')[0].select('.push')) > 0):
            for push_text in soup.select('#main-content')[0].select('.push'):
                push = push + str(i) + push_text.text
                i = i + 1
        # 以字典回傳資料
        return {'summary': summary, 'dt': dt, 'push': push}

#d = pageDetail('https://www.ptt.cc/bbs/creditcard/M.1469180146.A.1D0.html')


# In[54]:

home_page = 'https://www.ptt.cc/bbs/Salary/index.html'
home_section = requests.get(home_page)
home_soup = BeautifulSoup(home_section.text, 'html.parser')

controls = home_soup.find('div', 'btn-group-paging').find_all('a', 'btn')

link = controls[1].get('href')
max_page = int(re.findall('\d+', link)[0]) + 1
min_page = 2375
#min_page = 1


# In[55]:

domain = 'https://www.ptt.cc'
#建立空 List
pttary = []
for page in range(max_page,min_page,-1):
    #紀錄一下跑到哪
    print(page)
    
    ptturl = 'https://www.ptt.cc/bbs/Salary/index{}.html'.format(page)
    #使用format 更新頁數
    section = requests.get(ptturl.format(page))
    #將資料讀取至BeautifulSoup
    soup = BeautifulSoup(section.text, 'html.parser')
    #分別抓取各標籤元素
    for ent in soup.select('.r-ent'): 
        if len(ent.select('a')) >0:
            dic = {}
            dic['title'] = ent.select('.title')[0].text
            dic['link'] = domain + ent.select('a')[0]['href']
            #更新內容頁抓取到的資料
            dic.update(pageDetail(dic['link']))
            pttary.append(dic)


# In[48]:

import pandas
df = pandas.DataFrame(pttary)
df.head()


# In[58]:

#print(pttary[5]['push'])
len(pttary)
with open('df.json', 'w', encoding='utf-8') as file:
    df.to_json(file, force_ascii=False)
df.to_excel('df.xlsx')


# In[ ]:



