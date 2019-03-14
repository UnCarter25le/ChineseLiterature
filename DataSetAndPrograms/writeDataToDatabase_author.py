#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# -*- coding: utf-8 -*-

#(1)
# https://stackoverflow.com/questions/11146190/python-typeerror-not-enough-arguments-for-format-string
#(2)
# InternalError: (1241, 'Operand should contain 1 column(s)')   --> 陣列的資料要json.dumps
#(3)
# https://stackoverflow.com/questions/606191/convert-bytes-to-a-string  -->bytes2string
#(4)
#InternalError: (1366, "Incorrect string value: '\\xF0\\xA4\\xA7\\xA3\\xE3\\x80...' for column  -->4bytes一個漢字 ，發生在1152筆時。
# https://stackoverflow.com/questions/10957238/incorrect-string-value-when-trying-to-insert-utf-8-into-mysql-via-jdbc
# https://blog.csdn.net/boycycyzero/article/details/42879911
# https://www.chenshaowen.com/blog/using-utf8mb4-in-django-to-support-emoji-expression.html
# https://stackoverflow.com/questions/26532722/how-to-encode-utf8mb4-in-python -->*best!


import pymysql
import base64
import json,time,os,re
from langconv import *
from zh_wiki import *
# import codecs
# codecs.register(lambda name: codecs.lookup('utf-8') if name == 'utf8mb4' else None)

def SimChtoTradiCh(sentence):
    sentence = Converter('zh-hant').convert(sentence)
    return sentence

def searchNums(bookurl):
    searchNum = re.compile('\d+')
    number = searchNum.search(bookurl).group()
    return number

def initialFile():
    author = os.listdir('./作者的照片/')
    author.sort(key=lambda x: int(x.split('_')[0]))
    return author

def loadAuthorPhoto(key):
    global author,authorPhotoPoolNums
    if key in authorPhotoPoolNums:
        index = authorPhotoPoolNums.index(key)
        authorPhotoFile = author[index]
        with open('./作者的照片/{0}'.format(authorPhotoFile),'rb')as image_file:
            encoded_string = base64.b64encode(image_file.read())  #bytes String
        return str(encoded_string,encoding='utf-8') # 即使強制用utf-8編碼，仍可以用base64.b64decode解碼印出圖片。
    else:
        return 'None'
    
def loadAuthorInfo():
    with open('./authorInfoSETDetail_5.json')as f:
        inn2 = json.load(f)
    return inn2

def transNoneToNumber(none):
    if none == 'None':
        return '0'
    else:
        return none #如果設pass，就會回傳NoneType。錯誤發生在處理一連串None創作後的有創作的作者。
    

def replaceSymbol(context):
    context = context.replace('・','_')    .replace('·','_')    .replace('○','@')    .replace('—','-')    .replace('－','-')    .replace('◎','@')    .replace('\n\u3000\u3000','')    .replace('\n','')    .replace('\u3000\u3000','')    .replace(' ','')    .replace("'",'')    .replace('!','！')    .replace('.','。')    .replace(':','：')    .replace('?','？')    .replace(';','；')    .replace('\\xa0','')
    return context #何得‘有巢'无主’之说。幸硬骨头朕，若他人则必不免。”  解決1626作者介紹的問題


def connectAndInsert():
    global inn2
    
    conn = pymysql.connect('localhost',port=3306,user='root',passwd='1234',charset='utf8', db='literature')  #連結資料庫

    cursor = conn.cursor()
    # 確保資料庫接受utf8mb4格式的資料！
    cursor.execute('SET NAMES utf8mb4')
    cursor.execute("SET CHARACTER SET utf8mb4")
    cursor.execute("SET character_set_connection=utf8mb4")
    #----------------------------
    cursor.close()
    print('開始進行insert！資料一共有：'+str(len(inn2.keys())))
    total = 0
    
    try:
        for key in list(inn2.keys())[0:]:
            print('進行第 '+key+'筆資料：')
            with conn.cursor() as cursor: #這種寫法讓cursor每執行完SQL後，就會休息(cursor.close())。
                
                begin = time.time()
                SQL = "insert into literature_author (author_id,                authorName_SimCh,                authorIntro_SimCh,                dynasty_SimCh,                authorName_TradiCh,                authorIntro_TradiCh,                dynasty_TradiCh,                worksNum,                authorImg,                authorImg_Uri,                authorCodeName,                domain_Url,                author_Urn,                works_Urn) values ({0})".format(','.join(
                    ["'" +key+"'" \
                    ,"'" +inn2[key]['authorName']+"'" \
                    ,"'" +replaceSymbol(inn2[key]['authorIntro'])+"'" \
                    ,"'" +inn2[key]['dynasty']+"'" \
                    ,"'" +SimChtoTradiCh(inn2[key]['authorName'])+"'" \
                    ,"'" +SimChtoTradiCh(replaceSymbol(inn2[key]['authorIntro']))+"'" \
                    ,"'" +SimChtoTradiCh(inn2[key]['dynasty'])+"'" \
                    ,"'" +transNoneToNumber(inn2[key]['worksNum'])+"'" \
                    ,"'" +loadAuthorPhoto(key)+"'" \
                    ,"'" +inn2[key]['authorImg']+"'" \
                    ,"'" +inn2[key]['authorCodeName']+"'" \
                    ,"'" +inn2[key]['domainUrl']+"'" \
                    ,"'" +inn2[key]['authorUrn']+"'" \
                    ,"'" +json.dumps(inn2[key]['worksUrn'])+"'" ]
                )
                                               )
                cursor.execute(SQL)

            conn.commit()

            end = time.time()
            timeSpend = end - begin
            total += timeSpend
            print('每筆耗時：'+ str(timeSpend))
    except Exception as e:
        print('key='+key+'時，發生錯誤：' + str(e))
        conn.rollback()
        conn.close()
        
    finally:
        conn.close()

    print('done '+key)
    return '平均每筆耗時：'+str(total/len(inn2.keys()))+' 秒'

if __name__ == '__main__':
    # 只呼叫loadAuthorInfo()，並不能讓inn2變成global variable。
    author = initialFile()
    authorPhotoPoolNums = [auPhoto.split('_')[0] for auPhoto in initialFile()]
    inn2 = loadAuthorInfo()
    averageTime = connectAndInsert()
    print(averageTime)

