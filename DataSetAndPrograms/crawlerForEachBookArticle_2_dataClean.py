#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from bs4 import BeautifulSoup
import requests,json,os
from datetime import datetime
import time
import re

def searchNums(bookurl):
    searchNum = re.compile('\d+')
    number = searchNum.search(bookurl).group()
    return number

def mkdir():
    if not os.path.isdir('./古籍/'):
        os.mkdir('./古籍/')
    else:
        print('已經存在_古籍 資料夾')
        pass

def replaceSymbol(context):
    context = context.replace('・','_')    .replace('·','_')    .replace('○','@')    .replace('—','-')    .replace('－','-')    .replace('◎','@')    .replace('\n\u3000\u3000','')    .replace('\n','')    .replace('\u3000\u3000','')    .replace(' ','')    .replace("'",'')    .replace('!','！')    .replace(',','，')    .replace('.','。')    .replace(':','：')    .replace('?','？')    .replace(';','；')    .replace('\\xa0','')
    return context

def initialFile():
    classicc = os.listdir('./古籍innerChapterHtml/')
    classicc.sort(key=lambda x: int(x.split('_')[0])) #列舉檔案排序
    classicc.sort(key=lambda x: int(x.split('_')[1])) 
    return classicc

def generateContent(textSoup):
    #不保留\u3000空格、\n\u3000\u3000。一個文章成為由多個段落元素組成的陣列。
    innerChapterContent = []
    for row in textSoup.select_one('.contson').stripped_strings:
        innerChapterContent.append(replaceSymbol(row).strip())
    return innerChapterContent

def innerChapterAuthorIdReference(authorName):
    global inn4,authorNamePool
    if authorName in authorNamePool:
        return authorNamePool.index(authorName)+1
    else:
        return 'None'

def innerChapterComparison(innerChapter_id):
    global inn2
    try:
        index = list(inn2['SimCh'].keys()).index(innerChapter_id)
        return list(inn2['SimCh'].values())[index]
    except:
        return False

def generateInnerChapterName(fileName):
    tmpInnerChapter = fileName.replace('_html.txt','').split('_')[2:]
    innerChapterName = '_'.join(tmpInnerChapter)
    return innerChapterName

def searchRealFile(innerChapter_id):
    for readyFile in filePoolwithInnerChapter_id:
        if innerChapter_id == readyFile.split('_')[0]:
            return readyFile
        else:
            pass

with open('./bookInfoDetail_5.json')as f: #不能用6，innerchapterhtml沒有古文觀止的。
    inn = json.load(f)

# with open('./guanzhi_古文观止.json')as f:
#     inn1 = json.load(f)
    
with open('./innerChapterComparison.json')as f:
    inn2 = json.load(f)

with open('./authorComparisonId.json')as f:
    inn4 = json.load(f)

mkdir()    

authorNamePool = [row for row in [inn4['SimCh'][i] for i in inn4['SimCh'].keys()]]
filePoolwithInnerChapter_id = ['_'.join(file.split('_')[1:]) for file in initialFile()]

start = datetime.now()

for key in list(inn.keys())[0:]: #迭代進入每本書
    bookDict = {}
    contentArray = [] #仿古文觀止
    
    for keyInside in inn[key]['upperChapter']:# 山海經的山經、海經
        upperInnerDict = {}  #處理完山經與其文章後，清空後，在處理海經與其文章
        innerContentArray = [] #仿古文觀止
        upperInnerDict['upperChapter'] = keyInside['upperChapterName'] 
        for chapterInside in keyInside['innerChapterInside']: #該upperChapter的所有innerChapter(/guwen/bookv_1.aspx)
            innerChapterDict = {} #裝每個innerChapter的資訊。
            #有些innerChapterUrn是None(<class 'NoneType'>)，如27鬼谷子的。
            #bookv_16529 雖然有連結，但该文章不存在或已被删除，点击返回古诗文网首页。https://so.gushiwen.org//guwen/bookv_16529.aspx
            if chapterInside != None and innerChapterComparison(searchNums(chapterInside)):
                innerChapterDict['innerChapter_id'] = searchNums(chapterInside)
                innerChapterDict['innerChapter'] = innerChapterComparison(searchNums(chapterInside))
                innerChapterDict['innerChapterUrn'] = chapterInside

                fileReady = searchRealFile(searchNums(chapterInside))
                with open('./古籍innerChapterHtml/{0}_{1}'.format(key,fileReady))as f:
                    inn5 = f.read()
                textSoup = BeautifulSoup(inn5,'html.parser')
                innerChapterDict['chapterContent'] = generateContent(textSoup)

                authorName = textSoup.select_one('.source').text.split('：')[1].split(' ')[0].strip()
                innerChapterDict['authorName'] = authorName
                innerChapterDict['author_id'] = innerChapterAuthorIdReference(authorName)
                innerContentArray.append(innerChapterDict)
            else:
                print('book_id: '+key+'有連結失效。書名是'+inn[key]['bookName'])
                pass
        upperInnerDict['innerContent'] = innerContentArray
        contentArray.append(upperInnerDict)
    bookDict['book_id'] = key
    bookDict['bookName'] = inn[key]['bookName']
    bookDict['bookIntro'] = inn[key]['bookIntro']
    bookDict['bookImg'] = inn[key]['bookImg']
    bookDict['author_id'] = inn[key]['author_id']
    bookDict['quotation'] = inn[key]['quotation']
    bookDict['domainUrl'] = inn[key]['domainUrl']
    bookDict['bookUrn'] = inn[key]['bookUrn']
    bookDict['content'] = contentArray
    
    with open('./古籍/{0}_{1}.json'.format(bookDict['book_id'],bookDict['bookName']),'w',encoding='utf-8')as f:
        json.dump(bookDict,f,indent=2,ensure_ascii=False)
    with open('./古籍/{0}_{1}_noindent.json'.format(bookDict['book_id'],bookDict['bookName']),'w',encoding='utf-8')as f:
        json.dump(bookDict,f,ensure_ascii=False)
    
    print("完成第 "+key+"本書。")

end = datetime.now()

print('歷時： '+str(end-start))

