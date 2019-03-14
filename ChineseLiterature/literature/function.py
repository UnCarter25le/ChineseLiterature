import re
from PIL import Image
import PIL.Image
import base64
import sys,io
import urllib.parse


# 中文字轉成url:
# https://meyerweb.com/eric/tools/dencoder/     urlencode、decode
#
# (1)urlencode in python3
# https://stackoverflow.com/questions/5607551/how-to-urlencode-a-querystring-in-python
#   import urllib.parse
#   urllib.parse.quote_plus(論語)
# (2)urldecode in python 3
# https://stackoverflow.com/questions/16566069/url-decode-utf-8-in-python
#   from urllib.parse import unquote
#   url = unquote(%E8%AB%96%E8%AA%9E)
# (3)urlencode, querystring
# https://stackoverflow.com/questions/5607551/how-to-urlencode-a-querystring-in-python
# import urllib.parse
# f = {"yes":123}
# urllib.parse.urlencode(f)


def searchNums(bookurl):
    searchNum = re.compile('\d+')
    number = searchNum.search(bookurl).group()
    return number


def checkPhoto(image):
    try:
        img=base64.b64decode(image)   
        file_like=io.BytesIO(img)
        image=PIL.Image.open(file_like)
        image.show()
        return image
    except Exception as e:
        pass
        return e

def checkAuthorResultS(authorData):
    if authorData:
        authorDataArray = []
        for dataInside in authorData:
            authorDataDict = {}
            authorDataDict = {
                "author_id": dataInside[0],
                "authorName_TradiCh": dataInside[1],
                "dynasty_TradiCh": dataInside[2],
                "authorIntro_TradiCh":dataInside[3],
                "author_Uri":dataInside[4]
            }
            authorDataArray.append(authorDataDict)
        authorNums = len(authorDataArray)
        return authorDataArray,authorNums
    else:
        authorDataArray = "搜查不到，請換關鍵字繼續～"
        authorNums = 0
        return authorDataArray,authorNums

def checkAuthorResult(authorData):
    if authorData:
        authorDataArray = []
        for dataInside in authorData:
            authorDataDict = {}
            authorDataDict = {
                "author_id": dataInside[0],
                "authorName_SimCh": dataInside[1],
                "dynasty_SimCh": dataInside[2],
                "authorIntro_SimCh":dataInside[3],
                "author_Uri":dataInside[4]
            }
            authorDataArray.append(authorDataDict)
        authorNums = len(authorDataArray)
        return authorDataArray,authorNums
    else:
        authorDataArray = "搜查不到，請換關鍵字繼續～"
        authorNums = 0
        return authorDataArray,authorNums

def checkBookResultS(bookData):
    if bookData:
        bookDataArray = []
        for dataInside in bookData:
            bookDataDict = {}
            bookDataDict = {
                "book_id": dataInside[0],
                "bookName_TradiCh": dataInside[1],
                "author_id": dataInside[2],
                "bookIntro_TradiCh":dataInside[3],
                "book_Uri":dataInside[4]
            }
            bookDataArray.append(bookDataDict)
        bookNums = len(bookDataArray)
        return bookDataArray,bookNums
    else:
        bookDataArray = "搜查不到，請換關鍵字繼續～"
        bookNums = 0
        return bookDataArray,bookNums

def checkBookResult(bookData):
    if bookData:
        bookDataArray = []
        for dataInside in bookData:
            bookDataDict = {}
            bookDataDict = {
                "book_id": dataInside[0],
                "bookName_SimCh": dataInside[1],
                "author_id": dataInside[2],
                "bookIntro_SimCh":dataInside[3],
                "book_Uri":dataInside[4]
            }
            bookDataArray.append(bookDataDict)
        bookNums = len(bookDataArray)
        return bookDataArray,bookNums
    else:
        bookDataArray = "搜查不到，請換關鍵字繼續～"
        bookNums = 0
        return bookDataArray,bookNums


def urlencodeForCh(keyword):
    urlcode = urllib.parse.quote_plus(keyword)
    return urlcode