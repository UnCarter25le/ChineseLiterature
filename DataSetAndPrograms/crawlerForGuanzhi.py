#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from bs4 import BeautifulSoup
import requests,json
from datetime import datetime
from pytz import timezone
import pytz
import time

def getTime():
    CN = pytz.timezone('Asia/Taipei')
    CN.zone
    CN_time =CN.localize(datetime.now())#+ timedelta(hours=8))
    fmt = "%Y年_%m月_%d日_%H時_%M分"
    now = CN_time.strftime(fmt)
    return now

def getPageAndFile(url):
     #古文觀止
    global headers
    
    res = requests.get(url,headers=headers)
    soup = BeautifulSoup(res.text,'html.parser')
    
    with open('./{0}.txt'.format(getFileName(res.url,soup)),'w',encoding = 'utf-8')as f:
        f.write(str(soup))
    return res,soup

def getPage(url):
    global headers
    res = requests.get(url,headers=headers)
    soup = BeautifulSoup(res.text,'html.parser')
    return res,soup

def getFileName(resurl,soup): #專門是古文觀止適用而已喔
    fileName = resurl.split('/')[-1].split('.')[0]+'_'+soup.select_one('.title').text.strip()+'_html'
    return fileName

def dynastySimComparison(value):
    with open('./dynastyComparison.json') as f:
        inn = f.read()
        outt = json.loads(inn)
    if value in list(outt[0].values()):
        return list(outt[0].values()).index(value)+1
    else:
        return '14'

def replaceSymbol(context):
    context = context.replace('・','_')    .replace('·','_')    .replace('○','@')    .replace('—','-')    .replace('－','-')    .replace('◎','@')    .replace('\n\u3000\u3000','')    .replace('\n','')    .replace('\u3000\u3000','')    .replace(' ','')
    return context


def timeSleepOne():
    time.sleep(3)

def innerChapterAuthorIdReference(authorName):
    global innn,authorNamePool
    if authorName in authorNamePool:
        return authorNamePool.index(authorName)+1
    else:
        return authorName #看看哪個作者不在authorInfo裡

def getShiwenId(url):
    shiwenId = url.split('_')[1].split('.aspx')[0]
    return shiwenId

#省略翻譯
# def getShiwenTraslation(shiwenId):
#     apiUrl = 'https://so.gushiwen.org/shiwen2017/ajaxshiwencont.aspx?id='+shiwenId+'&value=yi'
#     resInner,soupInner = getPage(apiUrl)
#     timeSleepOne()
#     if not resInner.text is '':
#         translation = ""
#         for row in soupInner.select('p > span'):
#             translation += replaceSymbol(row.text)
#         print('translation get!')
#         return translation
#     else:
#         print('translation None!')
#         return 'None'

def generateContent(textSoup):
    #不保留\u3000空格、\n\u3000\u3000。一個文章成為由多個段落元素組成的陣列。
    innerChapterContent = []
    for row in textSoup.select_one('.contson').stripped_strings:
        innerChapterContent.append(replaceSymbol(row).strip())
    return innerChapterContent

def getEntireStructure(res,soup): #專門爬古文觀止
    start = datetime.now()
    with open('./{0}.txt'.format(getFileName(res.url,soup)), encoding = 'utf-8')as f:
        inn = f.read()
    textSoup = BeautifulSoup(inn,'html.parser')

    title = textSoup.select_one('.title').text.strip() #書名
    tmpUpperAndInner = textSoup.select('.typecont') #詩文當中，每個upperChapter and innerChapter區塊。有些詩文沒有upperChapter，因此只有一個typecont區塊。

    contentArray = []
    print('現在時刻:'+getTime()+'，開始處理：')
    done = 1
    innerChapter_id = 20342 #古籍的innerChapter_id到20341，所以從20342開始計算古文觀止的文章。
    for rowOutside in tmpUpperAndInner:
        innerContentArray = []
        upperInnerDict = {} 
        for rowInside in rowOutside.select('a'):
            print('處理第'+str(done)+'筆innerChapter中...')
            innerChapterDict = {}
            innerChapterDict['innerChapter_id'] = str(innerChapter_id)
            innerChapterDict['innerChapter'] = replaceSymbol(rowInside.text) #
            innerChapterDict['innerChapterUrn'] = rowInside.attrs.get('href').replace('https://so.gushiwen.org','')
            innerChapterDict['chapterContentCodeName'] = getShiwenId(rowInside.attrs.get('href')) #詩文專屬id
            
            timeSleepOne() #取得chapterContent內容頁
            soupFromPage = getPage(rowInside.attrs.get('href'))
            authorName = soupFromPage[1].select_one('.source').text.split('：')[1].split(' ')[0].strip() #避免『劉向 撰』的情況
            innerChapterDict['author_id'] = innerChapterAuthorIdReference(authorName)
            innerChapterDict['authorName'] = authorName
            innerChapterDict['dynasty_id'] = dynastySimComparison(soupFromPage[1].select_one('.source').text.split('：')[0].strip() )
            innerChapterDict['dynasty'] = soupFromPage[1].select_one('.source').text.split('：')[0].strip() 
            #不保留\u3000空格、\n\u3000\u3000，一個文章成為由多個段落元素組成的陣列。
            innerChapterDict['chapterContent'] = generateContent(soupFromPage[1])
            print('成功捕捉文章成陣列！以下是其中的部份內容：')
            print(generateContent(soupFromPage[1])[:1])
            
            
            #省略翻譯
#             timeSleepOne() ##取得chapterContent內容頁翻譯
#             translation = getShiwenTraslation(getShiwenId(rowInside.attrs.get('href')))
#             innerChapterDict['translation'] = translation
            
            print('完成第'+str(done)+'筆。')
            innerContentArray.append(innerChapterDict)
            done += 1
            innerChapter_id += 1
            
        upperInnerDict['upperChapter'] = replaceSymbol(rowOutside.select_one('.bookMl').text)
        upperInnerDict['innerContent'] = innerContentArray
        contentArray.append(upperInnerDict)

    bookDict = {}  #整本詩文選集的內容
    bookDict['book_id'] = '295'
    bookDict['bookName'] = title    
    bookDict['bookIntro'] = 'None' 
    bookDict['bookImg'] = 'None'
    bookDict['authorName'] = '佚名'
    bookDict['author_id'] = '15791'
    bookDict['quotation'] = ['None','None']
    bookDict['domainUrl'] = 'https://so.gushiwen.org'
    bookDict['bookUrn'] = '/wenyan/guanzhi.aspx'
    bookDict['content'] = contentArray
    end = datetime.now()
    print('現在時刻:'+getTime()+'，完成！')
    print('共耗時 '+str((end-start)))
    return bookDict
    

if __name__ == '__main__':
    with open('./authorInfoSETDetail_5.json')as f:
        innn = json.load(f)
    authorNamePool = [row for row in [innn[i]['authorName'] for i in innn.keys()]]
        
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'}
    res,soup = getPageAndFile('https://so.gushiwen.org/wenyan/guanzhi.aspx')
    bookDict = getEntireStructure(res,soup)
    
    
    with open('./{0}.json'.format(getFileName(res.url,soup).replace('_html','')),'w',encoding='utf-8') as f:
        json.dump(bookDict,f,indent=2,ensure_ascii=False)

