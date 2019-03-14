from django.shortcuts import render,redirect
from django.http import HttpResponse

from django.contrib.auth import authenticate
from django.contrib import auth

from datetime import datetime
from django.utils import timezone

# from ChineseLiterature.settings import SSLFILES_FOLDER #呼叫SSL認證檔

import pymysql
import json,time,os
from literature import function

# Create your views here.

def getSearchResult(request,keyword=None,s=None):
    # 本地
    conn = pymysql.connect('localhost',port=3306,user='root',passwd='1234',charset='utf8',db='literature')
    #Azure
    #conn = pymysql.connect(user="...", \
    #                   password='...', \
    #                   host="XXX.database.azure.com",\
    #                   port=3306, database='literature', \
    #                   ssl = {'ssl': {'ca': SSLFILES_FOLDER+'BaltimoreCyberTrustRoot.crt.pem'}})

    with conn.cursor() as cursor:
        # 確保資料庫接受utf8mb4格式的資料！
        cursor.execute('SET NAMES utf8mb4')
        cursor.execute("SET CHARACTER SET utf8mb4")
        cursor.execute("SET character_set_connection=utf8mb4")
        cursor.execute("SET sql_mode = 'PIPES_AS_CONCAT'")
        #----------------------------
    if keyword is None:
        note = "僅針對「作者名稱」、「古籍名稱」作搜尋。不支持「空白」or「%20」。"
        language1 = "簡體搜尋："
        input1 = "請在網址列 「/search/」 後面，輸入關鍵字。例如：/search/古文观止 。"
        language2 = "繁體搜尋："
        input2 = "請在網址列 「/search/關鍵字」 後面，加上 「/s」。例如：/search/李白/s 。"
    elif not keyword is None and s is 's': #繁體搜尋
        try:
            urlcode = function.urlencodeForCh(keyword)
            with conn.cursor() as cursor:
                SQL = "select author_id,\
                authorName_TradiCh,\
                dynasty_TradiCh,\
                authorIntro_TradiCh,\
                domain_Url || author_Urn\
                from literature_author where authorName_TradiCh like '%{0}%'".format(keyword)
                cursor.execute(SQL)
                authorData = cursor.fetchall()
            authorDataArray, authorNums = function.checkAuthorResultS(authorData)

            with conn.cursor() as cursor:
                SQL = "select book_id,\
                bookName_TradiCh,\
                author.author_id,\
                bookIntro_TradiCh,\
                book.domain_Url || book.book_Urn\
                from literature_classicbook AS book join literature_author AS author \
                on book.author_id_id = author.author_id where bookName_TradiCh like '%{0}%'".format(keyword)
                cursor.execute(SQL)
                bookData = cursor.fetchall()
            bookDataArray, bookNums = function.checkBookResultS(bookData)
        except Exception as e:
            error = str(e)
            print("connection error!" + error)
            conn.close()
        finally:
            conn.close()
    
    elif not keyword is None and s is None : #簡體搜尋
        try:
            urlcode = function.urlencodeForCh(keyword)
            with conn.cursor() as cursor:
                SQL = "select author_id,\
                authorName_SimCh,\
                dynasty_SimCh,\
                authorIntro_SimCh,\
                domain_Url || author_Urn\
                from literature_author where authorName_SimCh like '%{0}%'".format(keyword)
                cursor.execute(SQL)
                authorData = cursor.fetchall()
            authorDataArray, authorNums = function.checkAuthorResult(authorData)

            with conn.cursor() as cursor:
                SQL = "select book_id,\
                bookName_SimCh,\
                author.author_id,\
                bookIntro_SimCh,\
                book.domain_Url || book.book_Urn\
                from literature_classicbook AS book join literature_author AS author \
                on book.author_id_id = author.author_id where bookName_SimCh like '%{0}%'".format(keyword)
                cursor.execute(SQL)
                bookData = cursor.fetchall()
            bookDataArray, bookNums = function.checkBookResult(bookData)
        except Exception as e:
            error = str(e)
            print("connection error!" + error)
            conn.close()
        finally:
            conn.close()

    return render(request,'literature/showSearchResult.html',locals())



def getBookInfo(request,s=None):
    # 本地
    conn = pymysql.connect('localhost',port=3306,user='root',passwd='1234',charset='utf8',db='literature')
    #Azure
    #conn = pymysql.connect(user="...", \
    #                   password='...', \
    #                   host="XXX.database.azure.com",\
    #                   port=3306, database='literature', \
    #                   ssl = {'ssl': {'ca': SSLFILES_FOLDER+'BaltimoreCyberTrustRoot.crt.pem'}})
    with conn.cursor() as cursor:
        # 確保資料庫接受utf8mb4格式的資料！
        cursor.execute('SET NAMES utf8mb4')
        cursor.execute("SET CHARACTER SET utf8mb4")
        cursor.execute("SET character_set_connection=utf8mb4")
        cursor.execute("SET sql_mode = 'PIPES_AS_CONCAT'")
        #----------------------------
    if s is None:
        language = "簡體"
        book_id = "book_id"
        bookName_SimCh = "bookName_SimCh"
        bookIntro_SimCh = "bookIntro_SimCh"
        bookImg_Uri = "bookImg_Uri"
        book_Uri = "book_Uri"
        try:
            with conn.cursor() as cursor:
                SQL = "select book_id,\
                bookName_SimCh,\
                bookIntro_SimCh,\
                bookImg_Uri,\
                domain_Url || book_Urn \
                from literature_classicbook"
                cursor.execute(SQL)
                data = cursor.fetchall()
        except Exception as e:
            error = str(e)
            print("connection error!" + error)
            conn.close()
        finally:
            conn.close()

    elif s is "s":
        language = "繁體"
        book_id = "book_id"
        bookName_SimCh = "bookName_TradiCh" 
        bookIntro_SimCh = "bookIntro_TradiCh"
        bookImg_Uri = "bookImg_Uri"
        book_Uri = "book_Uri"
        try:
            with conn.cursor() as cursor:
                SQL = "select book_id,\
                bookName_TradiCh,\
                bookIntro_TradiCh,\
                bookImg_Uri,\
                domain_Url || book_Urn \
                from literature_classicbook"
                cursor.execute(SQL)
                data = cursor.fetchall()
            
        except Exception as e:
            error = str(e)
            print("connection error!" + error)
            conn.close()
        finally:
            conn.close()

    elif not s is None or s != 's':
        error = " /bookInfo/ 後面，輸入 s 可以繁體檢視～"
    return render(request,'literature/showBookInfo.html',locals())
    



def getBookDetail(request,nums=None,s=None):
    # 本地
    conn = pymysql.connect('localhost',port=3306,user='root',passwd='1234',charset='utf8',db='literature')
    #Azure
    #conn = pymysql.connect(user="...", \
    #                   password='...', \
    #                   host="XXX.database.azure.com",\
    #                   port=3306, database='literature', \
    #                   ssl = {'ssl': {'ca': SSLFILES_FOLDER+'BaltimoreCyberTrustRoot.crt.pem'}})
    cursor = conn.cursor()
     # 確保資料庫接受utf8mb4格式的資料！
    cursor.execute('SET NAMES utf8mb4')
    cursor.execute("SET CHARACTER SET utf8mb4")
    cursor.execute("SET character_set_connection=utf8mb4")
    cursor.execute("SET sql_mode = 'PIPES_AS_CONCAT'")
    #----------------------------
    if not nums in [str(num) for num in range(1,296)]:
        error = "請在 /bookInfo/ 後面，輸入介於1～295的數字。"

    elif  s == 's' and nums in [str(num) for num in range(1,296)]:
        language = "繁體"
        upperChapter_SimCh = "upperChapter_TradiCh"
        innerChapter_id = "innerChapter_id"
        innerChapter_Uri = "innerChapter_Uri"
        chapterContent_SimCh = "chapterContent_TradiCh"
        innerChapter_SimCh = "innerChapter_TradiCh"
        try:
            with conn.cursor() as cursor:
                SQL = "select upperChapter_TradiCh,\
                innerChapter_id,\
                book.domain_Url || innerChapter_Urn,\
                chapterContent_TradiCh,\
                book.bookName_TradiCh,\
                book.bookImg,\
                book.bookIntro_TradiCh,\
                innerChapter_TradiCh,\
                author.authorName_TradiCh\
                from literature_classicbook AS book ,literature_classicbook_content AS content, literature_author AS author\
                where  book.book_id = content.book_id_id and book.author_id_id = author.author_id\
                and book_id = {0} limit 5".format(nums)
                cursor.execute(SQL)
                data = cursor.fetchall()
            bookName_SimCh = data[0][4]
            bookIntro_SimCh = data[0][6]
            bookAuthorName = data[0][8]
            function.checkPhoto(data[0][5])
            
            
        except Exception as e:
            error = str(e)
            print("connection error!" + error)
            conn.close()
        finally:
            conn.close()

    elif s is None and nums in [str(num) for num in range(1,296)]:
        language = "簡體"
        upperChapter_SimCh = "upperChapter_SimCh"
        innerChapter_id = "innerChapter_id"
        innerChapter_Uri = "innerChapter_Uri"
        chapterContent_SimCh = "chapterContent_SimCh"
        innerChapter_SimCh = "innerChapter_SimiCh"
        try:
            with conn.cursor() as cursor:
                SQL = "select upperChapter_SimCh,\
                innerChapter_id,\
                book.domain_Url || innerChapter_Urn,\
                chapterContent_SimCh,\
                book.bookName_SimCh,\
                book.bookImg,\
                book.bookIntro_SimCh,\
                innerChapter_SimCh,\
                author.authorName_SimCh\
                from literature_classicbook AS book ,literature_classicbook_content AS content, literature_author AS author\
                where  book.book_id = content.book_id_id  and book.author_id_id = author.author_id\
                and book_id = {0} limit 5".format(nums)
                cursor.execute(SQL)
                data = cursor.fetchall()
            bookName_SimCh = data[0][4]
            bookIntro_SimCh = data[0][6]
            bookAuthorName = data[0][8]
            function.checkPhoto(data[0][5])
        except Exception as e:
            error = str(e)
            print("connection error!" + error)
            conn.close()
        finally:
            conn.close()
    return render(request,'literature/showBookDetail.html',locals())



def getAuthorInfo(request,s=None):
    # 本地
    conn = pymysql.connect('localhost',port=3306,user='root',passwd='1234',charset='utf8',db='literature')
    #Azure
    #conn = pymysql.connect(user="...", \
    #                   password='...', \
    #                   host="XXX.database.azure.com",\
    #                   port=3306, database='literature', \
    #                   ssl = {'ssl': {'ca': SSLFILES_FOLDER+'BaltimoreCyberTrustRoot.crt.pem'}})
    with conn.cursor() as cursor:
         # 確保資料庫接受utf8mb4格式的資料！
        cursor.execute('SET NAMES utf8mb4')
        cursor.execute("SET CHARACTER SET utf8mb4")
        cursor.execute("SET character_set_connection=utf8mb4")
        cursor.execute("SET sql_mode = 'PIPES_AS_CONCAT'")
        #----------------------------
    if s is None:
        language = "簡體"

        author_id = "author_id"
        authorName_SimCh = "authorName_SimCh"
        dynasty_SimCh = "dynasty_SimCh"
        authorIntro_SimCh = "authorIntro_SimCh"
        authorImg_Uri = "authorImg_Uri"
        author_Uri = "author_Uri"
        works_Uri = "works_Uri"

        try:
            with conn.cursor() as cursor:
                SQL = "select author_id,\
                authorName_SimCh,\
                dynasty_SimCh,\
                authorIntro_SimCh,\
                authorImg_Uri,\
                domain_Url || author_Urn,\
                works_Urn\
                from literature_author limit 100"
                cursor.execute(SQL)
                data = cursor.fetchall()
        except Exception as e:
            error = str(e)
            print("connection error!" + error)
            conn.close()
        finally:
            conn.close()
    elif s is 's':
        language = "繁體"

        author_id = "author_id"
        authorName_SimCh = "authorName_TradiCh"
        dynasty_SimCh = "dynasty_TradiCh"
        authorIntro_SimCh = "authorIntro_TradiCh"
        authorImg_Uri = "authorImg_Uri"
        author_Uri = "author_Uri"
        works_Uri = "works_Uri"

        try:
            with conn.cursor() as cursor:
                SQL = "select author_id,\
                authorName_TradiCh,\
                dynasty_TradiCh,\
                authorIntro_TradiCh,\
                authorImg_Uri,\
                domain_Url || author_Urn,\
                works_Urn\
                from literature_author limit 100"
                cursor.execute(SQL)
                data = cursor.fetchall()
        except Exception as e:
            error = str(e)
            print("connection error!" + error)
            conn.close()
        finally:
            conn.close()

    elif not s is None or s != 's':
        error = " /authorInfo/ 後面，輸入 s 可以繁體檢視～"
    return render(request,'literature/showAuthorInfo.html',locals())
    



def getAuthorDetail(request,nums=None,s=None):
    # 本地
    conn = pymysql.connect('localhost',port=3306,user='root',passwd='1234',charset='utf8',db='literature')
    #Azure
    #conn = pymysql.connect(user="...", \
    #                   password='...', \
    #                   host="XXX.database.azure.com",\
    #                   port=3306, database='literature', \
    #                   ssl = {'ssl': {'ca': SSLFILES_FOLDER+'BaltimoreCyberTrustRoot.crt.pem'}})
    with conn.cursor() as cursor:
         # 確保資料庫接受utf8mb4格式的資料！
        cursor.execute('SET NAMES utf8mb4')
        cursor.execute("SET CHARACTER SET utf8mb4")
        cursor.execute("SET character_set_connection=utf8mb4")
        cursor.execute("SET sql_mode = 'PIPES_AS_CONCAT'")
        #----------------------------
    if not nums in [str(num) for num in range(1,15920)]:
        error = "請在 /authorInfo/ 後面，輸入介於1～15919的數字。"

    elif s is None and nums in [str(num) for num in range(1,15920)] :
        language = "簡體"

        author_id = "author_id"
        authorName_SimCh = "authorName_SimCh"
        dynasty_SimCh = "dynasty_SimCh"
        authorIntro_SimCh = "authorIntro_SimCh"
        authorImg_Uri = "authorImg_Uri"
        author_Uri = "author_Uri"
        works_Uri = "works_Uri"

        try:
            with conn.cursor() as cursor:
                SQL = "select author_id,\
                authorName_SimCh,\
                dynasty_SimCh,\
                authorIntro_SimCh,\
                authorImg_Uri,\
                domain_Url || author_Urn,\
                works_Urn,\
                authorImg\
                from literature_author\
                where  author_id  = {0} ".format(nums)
                cursor.execute(SQL)
                data = cursor.fetchall()
            authorName_SimCh = data[0][1]
            authorIntro_SimCh= data[0][3]
            function.checkPhoto(data[0][7])

            # try:  使用template 的 for loop empty機制，就不需要加上try catch了。
            with conn.cursor() as cursor:
                SQL2 = "select book.book_id,\
                book.bookName_SimCh,\
                book.bookIntro_SimCh\
                from literature_author AS author , literature_classicbook AS book\
                where  author.author_id = book.author_id_id and author_id  = {0} ".format(nums)
                cursor.execute(SQL2)
                data2 = cursor.fetchall()
            # except:
            #     bookid = "此作者沒有古籍著作。"
            #     bookname = "--"
            #     bookintro = "--"
            #     tip = "295本書  對到 15919位作者的機率是。。。。0.018531315...."
        except Exception as e:
            error = str(e)
            print("connection error!" + error)
            conn.close()
        finally:
            conn.close()

    elif s is 's' and nums in [str(num) for num in range(1,15920)] :
        language = "繁體"

        author_id = "author_id"
        authorName_SimCh = "authorName_TradiCh"
        dynasty_SimCh = "dynasty_TradiCh"
        authorIntro_SimCh = "authorIntro_TradiCh"
        authorImg_Uri = "authorImg_Uri"
        author_Uri = "author_Uri"
        works_Uri = "works_Uri"

        try:
            with conn.cursor() as cursor:
                SQL = "select author_id,\
                authorName_TradiCh,\
                dynasty_TradiCh,\
                authorIntro_TradiCh,\
                authorImg_Uri,\
                domain_Url || author_Urn,\
                works_Urn,\
                authorImg\
                from literature_author\
                where  author_id  = {0} ".format(nums)
                cursor.execute(SQL)
                data = cursor.fetchall()
            authorName_SimCh = data[0][1]
            authorIntro_SimCh= data[0][3]
            function.checkPhoto(data[0][7])

            # try:
            with conn.cursor() as cursor:
                SQL2 = "select book.book_id,\
                book.bookName_TradiCh,\
                book.bookIntro_TradiCh\
                from literature_author AS author , literature_classicbook AS book\
                where  author.author_id = book.author_id_id and author_id  = {0} ".format(nums)
                cursor.execute(SQL2)
                data2 = cursor.fetchall()
            # except:
            #     bookid = "此作者沒有古籍著作。"
            #     bookname = "--"
            #     bookintro = "--"
            #     tip = "295本書  對到 15919位作者的機率是。。。。0.018531315...."
        except Exception as e:
            error = str(e)
            print("connection error!" + error)
            conn.close()
        finally:
            conn.close()
    return render(request,'literature/showAuthorDetail.html',locals())

def getQuotaInfo(request,s=None):
    # 本地
    conn = pymysql.connect('localhost',port=3306,user='root',passwd='1234',charset='utf8',db='literature')
    #Azure
    #conn = pymysql.connect(user="...", \
    #                   password='...', \
    #                   host="XXX.database.azure.com",\
    #                   port=3306, database='literature', \
    #                   ssl = {'ssl': {'ca': SSLFILES_FOLDER+'BaltimoreCyberTrustRoot.crt.pem'}})
    with conn.cursor() as cursor:
         # 確保資料庫接受utf8mb4格式的資料！
        cursor.execute('SET NAMES utf8mb4')
        cursor.execute("SET CHARACTER SET utf8mb4")
        cursor.execute("SET character_set_connection=utf8mb4")
        cursor.execute("SET sql_mode = 'PIPES_AS_CONCAT'")
        #----------------------------
    if s is None:
        language = "簡體"

        quotation_id = "quotation_id"
        quotation_SimCh = "quotation_SimCh"
        quotaTranslation_SimCh = "quotaTranslation_SimCh"
        quotaFrom_SimCh = "quotaFrom_SimCh"
        
        try:
            with conn.cursor() as cursor:
                SQL = "select quotation_id,\
                quotation_SimCh,\
                quotaTranslation_SimCh,\
                quotaFrom_SimCh\
                from literature_quotation_from_classicbook limit 100"
                cursor.execute(SQL)
                data = cursor.fetchall()
        except Exception as e:
            error = str(e)
            print("connection error!" + error)
            conn.close()
        finally:
            conn.close()
    elif s is 's':
        language = "繁體"

        quotation_id = "quotation_id"
        quotation_SimCh = "quotation_TradiCh"
        quotaTranslation_SimCh = "quotaTranslation_TradiCh"
        quotaFrom_SimCh = "quotaFrom_TradiCh"

        try:
            with conn.cursor() as cursor:
                SQL = "select quotation_id,\
                quotation_TradiCh,\
                quotaTranslation_TradiCh,\
                quotaFrom_TradiCh\
                from literature_quotation_from_classicbook limit 100"
                cursor.execute(SQL)
                data = cursor.fetchall()
        except Exception as e:
            error = str(e)
            print("connection error!" + error)
            conn.close()
        finally:
            conn.close()

    elif not s is None or s != 's':
        error = " /quotaInfo/ 後面，輸入 s 可以繁體檢視～"
    return render(request,'literature/showQuotaInfo.html',locals())


def getQuotaDetail(request,nums=None,s=None):
    # 本地
    conn = pymysql.connect('localhost',port=3306,user='root',passwd='1234',charset='utf8',db='literature')
    #Azure
    #conn = pymysql.connect(user="...", \
    #                   password='...', \
    #                   host="XXX.database.azure.com",\
    #                   port=3306, database='literature', \
    #                   ssl = {'ssl': {'ca': SSLFILES_FOLDER+'BaltimoreCyberTrustRoot.crt.pem'}})
    with conn.cursor() as cursor:
         # 確保資料庫接受utf8mb4格式的資料！
        cursor.execute('SET NAMES utf8mb4')
        cursor.execute("SET CHARACTER SET utf8mb4")
        cursor.execute("SET character_set_connection=utf8mb4")
        cursor.execute("SET sql_mode = 'PIPES_AS_CONCAT'")
        #----------------------------
    if not nums in [str(num) for num in range(1,2000)]:
        error = "請在 /quotaInfo/ 後面，輸入介於1～1999的數字。"

    elif s is None and nums in [str(num) for num in range(1,2000)]:
        language = "簡體"

        quotation_id = "quotation_id"
        quotaTranslation_SimCh = "quotaTranslation_SimCh"
        innerChapter_id = "innerChapter_id"
        book_id = "book_id"
        bookName_SimCh = "bookName_SimCh"

        try:
            with conn.cursor() as cursor:
                SQL = "select quotation_id,\
                quotation_SimCh,\
                quotaTranslation_SimCh,\
                quotaFrom_SimCh,\
                quota.innerChapter_id_id,\
                content.book_id_id,\
                book.bookName_SimCh,\
                author.author_id\
                from ((literature_quotation_from_classicbook AS quota join literature_classicbook_content AS content \
                on quota.innerChapter_id_id = content.innerChapter_id) join literature_classicbook AS book \
                on content.book_id_id = book.book_id) join literature_author AS author \
                on book.author_id_id = author.author_id\
                where quotation_id = {0} ".format(nums)
                cursor.execute(SQL)
                data = cursor.fetchall()
            quotation = data[0][1]
            quotaFrom = data[0][3]
            bookid = data[0][5]
            authorid = data[0][7]
            innerchapterid = data[0][4]
        except Exception as e:
            error = str(e)
            print("connection error!" + error)
            conn.close()
        finally:
            conn.close()
    elif s is 's' and nums in [str(num) for num in range(1,15920)] :
        language = "繁體"

        quotation_id = "quotation_id"
        quotaTranslation_SimCh = "quotaTranslation_TradiCh"
        innerChapter_id = "innerChapter_id"
        book_id = "book_id"
        bookName_SimCh = "bookName_TradiCh"

        try:
            with conn.cursor() as cursor:
                SQL = "select quotation_id,\
                quotation_TradiCh,\
                quotaTranslation_TradiCh,\
                quotaFrom_TradiCh,\
                quota.innerChapter_id_id,\
                content.book_id_id,\
                book.bookName_TradiCh,\
                author.author_id\
                from ((literature_quotation_from_classicbook AS quota join literature_classicbook_content AS content \
                on quota.innerChapter_id_id = content.innerChapter_id) join literature_classicbook AS book \
                on content.book_id_id = book.book_id) join literature_author AS author \
                on book.author_id_id = author.author_id\
                where quotation_id = {0} ".format(nums)
                cursor.execute(SQL)
                data = cursor.fetchall()
            quotation = data[0][1]
            quotaFrom = data[0][3]
            bookid = data[0][5]
            authorid = data[0][7]
            innerchapterid = data[0][4]
        except Exception as e:
            error = str(e)
            print("connection error!" + error)
            conn.close()
        finally:
            conn.close()
    return render(request,'literature/showQuotaDetail.html',locals())

