#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json,re,os
import requests
from bs4 import BeautifulSoup

def mkdir():
    if not os.path.isdir('./古籍innerChapterHtml/'):
        os.mkdir('./古籍innerChapterHtml/')
    else:
        print('已經存在_古籍innerChapterHtml 資料夾')
        pass
def replaceSymbol(context):
    context = context.replace('・','_')    .replace('·','_')    .replace('○','@')    .replace('—','-')    .replace('－','-')    .replace('◎','@')    .replace('\n\u3000\u3000','')    .replace('\n','')    .replace('\u3000\u3000','')    .replace(' ','')    .replace("'",'')    .replace('!','！')    .replace(',','，')    .replace('.','。')    .replace(':','：')    .replace('?','？')    .replace(';','；')    .replace('\\xa0','')
    return context

def searchNums(bookurl):
    searchNum = re.compile('\d+')
    number = searchNum.search(bookurl).group()
    return number

with open('./bookInfo.json') as f:
    inn = f.read()
    outt = json.loads(inn)

    
mkdir()
    
keys = list(outt.keys())
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'}

# 檔名 'book_1' _ 'bookv_1' _ 'innerChapter'  _  'html'

for key in keys[0:]: #slice可以调整从哪本书开始爬 
    for row in [link for link in outt[key]['innerChapter'] if link != 'None']:
#         接續爬蟲     244'19162 ~244'19264
#         if int(searchNums(row)) in range(19162,19265):
#             pass
#             print('第 '+key+' 本，第 '+ searchNums(row)+' 個已經爬過。')
#         else:
        try: #https://so.gushiwen.org/guwen/bookv_16530.aspx 有連結沒有內容
            res = requests.get(row,headers = headers)
            soup = BeautifulSoup(res.text,'html.parser')
            print('正在處理第 '+key+' 本，第 '+ searchNums(row)+' 個innerChapter_id。。。' )
            #https://so.gushiwen.org/guwen/bookv_3190.aspx  名稱有/線＠＠
            with open('./古籍innerChapterHtml/{0}.txt'.format(key+'_'+searchNums(row)+'_'+replaceSymbol(soup.select_one('span').text).replace('/','_')+'_html'),'w',encoding='utf-8')as f:
                f.write(str(soup))
            print('完成第 '+key+' 本，第 '+ searchNums(row)+' 個id！' )
            time.sleep(4)
        except Exception as e:
            print(e)
            print('第 '+key+' 本，第 '+ searchNums(row)+' 個innerChapter_id 沒有內容！' )
            errorMessage = str(e)+'  '+searchNums(row)
            with open('./古籍innerChapterHtmlError.txt','a')as f:
                f.write(errorMessage)
                f.write('\n')

