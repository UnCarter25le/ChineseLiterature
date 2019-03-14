#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pymysql
import json,time,os
from langconv import *
from zh_wiki import *
# https://stackoverflow.com/questions/21659691/error-1452-cannot-add-or-update-a-child-row-a-foreign-key-constraint-fails

def SimChtoTradiCh(sentence):
    sentence = Converter('zh-hant').convert(sentence)
    return sentence
    
def loadQuotationInfo():
    with open('./quotationFromClassicBook_SET.json')as f:
        inn4 = json.load(f)
    return inn4

def replaceSymbol(context):
    context = context.replace('・','_')    .replace('·','_')    .replace('○','@')    .replace('—','-')    .replace('－','-')    .replace('◎','@')    .replace('\n\u3000\u3000','')    .replace('\n','')    .replace('\u3000\u3000','')    .replace(' ','')    .replace("'",'')    .replace('!','！')    .replace('.','。')    .replace(':','：')    .replace('?','？')    .replace(';','；')    .replace('\\xa0','')
    return context    
#id517 發生錯誤：解释：习惯了亲密，亲密到了一定程度就更为'斤斤计较'。說明單引號包裹的insert，元素不能有『'』


def connectAndInsert():
    global inn4
    conn = pymysql.connect('localhost',port=3306,user='root',passwd='1234',charset='utf8', db='literature')  #連結資料庫
    
    cursor = conn.cursor()
    # 確保資料庫接受utf8mb4格式的資料！
    cursor.execute('SET NAMES utf8mb4')
    cursor.execute("SET CHARACTER SET utf8mb4")
    cursor.execute("SET character_set_connection=utf8mb4")
    #----------------------------
    cursor.close()
    print('開始進行insert！資料一共有：'+str(len(inn4.keys())))
    total = 0
    
    try:
        for key in list(inn4.keys())[0:]:
            print('進行第 '+key+'筆資料：')
            with conn.cursor() as cursor: #這種寫法讓cursor每執行完SQL後，就會休息(cursor.close())。
                
                begin = time.time()
                
                SQL = "insert into literature_quotation_from_classicbook (quotation_SimCh,                quotaTranslation_SimCh,                quotaFrom_SimCh,                quotation_TradiCh,                quotaTranslation_TradiCh,                quotaFrom_TradiCh,                innerChapter_id_id) values ({0})".format(','.join(
                    ["'" + replaceSymbol(inn4[key]['quotation']) + "'"\
                    ,"'" + replaceSymbol(inn4[key]['quotaTranslation']) + "'"\
                    ,"'" + inn4[key]['quotaFrom'] + "'"\
                    ,"'" + SimChtoTradiCh(replaceSymbol(inn4[key]['quotation'])) + "'"\
                    ,"'" + SimChtoTradiCh(replaceSymbol(inn4[key]['quotaTranslation'])) + "'"\
                    ,"'" + SimChtoTradiCh(replaceSymbol(inn4[key]['quotaFrom'])) + "'"\
                    ,"'" + inn4[key]['innerChapter_id'] + "'"]
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
    return '平均每筆耗時：'+str(total/len(inn4.keys()))+' 秒'

if __name__ == '__main__':

    
    inn4 = loadQuotationInfo()
    averageTime = connectAndInsert()
    print(averageTime)

