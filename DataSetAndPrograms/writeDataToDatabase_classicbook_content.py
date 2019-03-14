#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pymysql
import json,time,os
from langconv import *
from zh_wiki import *
# (3 此方法有效！) https://pypi.org/project/django-jsonfield/     pip install django-jsonfield 
# 不過此套件不支持中文unicode存入（u前面的斜線會被捨去，變成沒有意義的資料）。
# 因此為了存進資料庫的資料確定是中文，且又是json array，
# 存進去前要使用匹配的bulkinsert字符，
# bulkinsert使用字符:"'" or  '"' ，能夠匹配的字串陣列如下：
# a. '"' ----"['哈哈','頁耶']"   這是python讀取list時，陣列元素若是字串時的樣子。建議使用此bulkinsert的字符。陣列須轉成str。
# b. "'"-----'["哈哈","頁耶"]'
# 因此不使用json序列化str: json.dumps(contentInner['chapterContent'])json.dumps(SimChtoTradiCh(contentInner['chapterContent']))
#___發現：若使用a，則字串裡面不可以包含『"』，必須取代掉；若使用b，則字串裡面不可以包含『'』，必須取代掉。

def SimChtoTradiCh(sentence):
    sentence = Converter('zh-hant').convert(sentence)
    return sentence

def initialFile():
    bookContent = os.listdir('./古籍/')
    bookContent.sort(key=lambda x: int(x.split('_')[0]))
    noindentArray = [noindentFile for noindentFile in bookContent if 'noindent' in noindentFile]
    return noindentArray

def loadBookfile(file):
    with open('./古籍/{0}'.format(file))as f:
        inn3 = json.load(f)
    return inn3

def loadInnerChapterComparison():
    with open('./innerChapterComparison.json')as f:
        inn = json.load(f)
    return len(inn['SimCh'].keys())

def replaceSymbol(context):
    context = context.replace('・','_')    .replace('·','_')    .replace('○','@')    .replace('—','-')    .replace('－','-')    .replace('◎','@')    .replace('\n\u3000\u3000','')    .replace('\n','')    .replace('\u3000\u3000','')    .replace(' ','')    .replace("'",'')    .replace('!','！')    .replace('.','。')    .replace(':','：')    .replace('?','？')    .replace(';','；')    .replace('\\xa0','')    .replace('"','*')    .replace('ue2a9','')
    return context # 解決第16本書，id2392的：(嫡妻第二子以下及妾子皆称为"支子")，裡面的「"」號； 還有\\xa0 空格的符號。
    #這裡不能把 「,」 取代成「，」，否則無法split(',')！

def connectAndInsert():
    global noindentArray
    conn = pymysql.connect('localhost',port=3306,user='root',passwd='1234',charset='utf8', db='literature')  #連結資料庫

    cursor = conn.cursor()
    # 確保資料庫接受utf8mb4格式的資料！
    cursor.execute('SET NAMES utf8mb4')
    cursor.execute("SET CHARACTER SET utf8mb4")
    cursor.execute("SET character_set_connection=utf8mb4")
    #----------------------------
    cursor.close()

    print('開始進行insert！資料一共有：'+str(loadInnerChapterComparison()))
    total = 0
                   
    try:
        for file in noindentArray[0:]:
            inn3 = loadBookfile(file)
            print('---------------進行資料是 ：'+ file)
                                  
            for content in inn3['content']:#有幾個upperChapter，就有幾個元素。
                for contentInner in content['innerContent']:
                    print('正在寫入id是 ：'+ contentInner['innerChapter_id']+'...')
                    with conn.cursor() as cursor: #這種寫法讓cursor每執行完SQL後，就會休息(cursor.close())。
                        begin = time.time() #每筆開始
                        
                        SQL = u"insert into literature_classicbook_content (innerChapter_id,                        upperChapter_SimCh,                        innerChapter_SimCh,                        chapterContent_SimCh,                        upperChapter_TradiCh,                        innerChapter_TradiCh,                        chapterContent_TradiCh,                        innerChapter_Urn,                        book_id_id,                        domain_Url) values ({0})".format(','.join(
                            ['"' + contentInner['innerChapter_id'] + '"'\
                            ,'"' + content['upperChapter'] + '"'\
                            ,'"' + contentInner['innerChapter'] + '"'\
                            ,'"' + replaceSymbol(str(contentInner['chapterContent'])) + '"'\
                            ,'"' + SimChtoTradiCh(content['upperChapter']) + '"'\
                            ,'"' + SimChtoTradiCh(contentInner['innerChapter']) + '"'\
                            ,'"' + SimChtoTradiCh(replaceSymbol(str(contentInner['chapterContent']))) + '"'\
                            ,'"' + contentInner['innerChapterUrn'] + '"'\
                            ,'"' + inn3['book_id']+ '"'\
                            ,'"' + inn3['domainUrl'] + '"']
                                                                )
                                                       )
                        cursor.execute(SQL)

                    conn.commit() #每完成一筆就commit

                    end = time.time()
                    timeSpend = end - begin
                    total += timeSpend
                    print('每筆耗時：'+ str(timeSpend))
    except Exception as e:
        print(file +'的innerChapter_id '+contentInner['innerChapter_id']+'，發生錯誤：' + str(e))
        conn.rollback()
        conn.close()
        
    finally:
        conn.close()

    print('done！')
    return '平均每筆耗時：'+str(total/loadInnerChapterComparison())+' 秒'

if __name__ == '__main__':
    
    noindentArray = initialFile()
    averageTime = connectAndInsert()
    print(averageTime)

