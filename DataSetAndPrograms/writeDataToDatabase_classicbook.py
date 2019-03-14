#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pymysql
import base64
import json,time,os
from langconv import *
from zh_wiki import *
# https://stackoverflow.com/questions/21659691/error-1452-cannot-add-or-update-a-child-row-a-foreign-key-constraint-fails

def SimChtoTradiCh(sentence):
    sentence = Converter('zh-hant').convert(sentence)
    return sentence

def initialFile():
    bookPhoto = os.listdir('./古籍的照片/')
    bookPhoto.sort(key=lambda x: int(x.split('_')[0]))
    return bookPhoto

def loadBookPhoto(key):
    global bookPhoto,bookPhotoPoolNums
    if key in bookPhotoPoolNums:
        index = bookPhotoPoolNums.index(key)
        bookPhotoFile = bookPhoto[index]
        with open('./古籍的照片/{0}'.format(bookPhotoFile),'rb')as image_file:
            encoded_string = base64.b64encode(image_file.read())  #bytes String
        return str(encoded_string,encoding='utf-8') # 即使強制用utf-8編碼，仍可以用base64.b64decode解碼印出圖片。
    else:
        return 'None'
    
def loadBookInfo():
    with open('./bookInfoDetail_6_withGuanzhi.json')as f:
        inn1 = json.load(f)
    return inn1

def replaceSymbol(context):
    context = context.replace('・','_')    .replace('·','_')    .replace('○','@')    .replace('—','-')    .replace('－','-')    .replace('◎','@')    .replace('\n\u3000\u3000','')    .replace('\n','')    .replace('\u3000\u3000','')    .replace(' ','')    .replace("'",'')    .replace('!','！')    .replace('.','。')    .replace(':','：')    .replace('?','？')    .replace(';','；')    .replace('\\xa0','')
    return context    


def connectAndInsert():
    global inn1
    conn = pymysql.connect('localhost',port=3306,user='root',passwd='1234',charset='utf8', db='literature')  #連結資料庫
      
    cursor = conn.cursor()
    # 確保資料庫接受utf8mb4格式的資料！
    cursor.execute('SET NAMES utf8mb4')
    cursor.execute("SET CHARACTER SET utf8mb4")
    cursor.execute("SET character_set_connection=utf8mb4")
    #----------------------------
    cursor.close()
    print('開始進行insert！資料一共有：'+str(len(inn1.keys())))
    total = 0
    
    try:
        for key in list(inn1.keys())[0:]:
            print('進行第 '+key+'筆資料：')
            with conn.cursor() as cursor: #這種寫法讓cursor每執行完SQL後，就會休息(cursor.close())。
                
                begin = time.time()
                
                SQL = "insert into literature_classicbook (book_id,                bookName_SimCh,                bookIntro_SimCh,                bookName_TradiCh,                bookIntro_TradiCh,                bookImg,                bookImg_Uri,                quotation,                domain_Url,                book_Urn,                author_id_id) values ({0})".format(','.join(
                    ["'" +key+ "'"\
                    ,"'" +inn1[key]['bookName']+ "'"\
                    ,"'" +replaceSymbol(inn1[key]['bookIntro'])+ "'"\
                    ,"'" +SimChtoTradiCh(inn1[key]['bookName'])+ "'"\
                    ,"'" +SimChtoTradiCh(replaceSymbol(inn1[key]['bookIntro']))+ "'"\
                    ,"'" +loadBookPhoto(key)+ "'"\
                    ,"'" +inn1[key]['bookImg']+ "'"\
                    ,"'" +json.dumps(inn1[key]['quotation'])+ "'"\
                    ,"'" +inn1[key]['domainUrl']+ "'"\
                    ,"'" +inn1[key]['bookUrn']+ "'"\
                    ,"'" +inn1[key]['author_id']+ "'"]
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
    return '平均每筆耗時：'+str(total/len(inn1.keys()))+' 秒'

if __name__ == '__main__':
    # 只呼叫initialFile()，並不能讓inn2變成global variable。
    bookPhoto = initialFile()
    inn1 = loadBookInfo()
    bookPhotoPoolNums = [boPhoto.split('_')[0] for boPhoto in bookPhoto]
    averageTime = connectAndInsert()
    print(averageTime)

