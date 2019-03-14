
# Chinese Literature
------
## Intention of this project:

- Because craving for reading the Chinese literature called __"古文觀止guanzhi"__ online for free one day in 
Bejing, I search that material on the internet through google or baidu. Expectedly, it's farely more difficult 
to search that one in traditional Chinese edtion than simplified Chinese edition. What sort of edition I want 
to read is traditional one! At the meantime, I had found a 
[website](https://www.gushiwen.org/wenyan/guanzhi.aspx "古文观止") equipped with wonderful and diversified literature 
resource, and caming up that why not crawlering literature material from that website and then Extract-Load-
Transform to build __one software service with two editions for myself!__

- Therefore,this project had taken place on 2/15,2019 and has been completed recently. I'm so delighted to have 
this service switching between simplified and traditional Chinese,which meets my origial expectation to see Chinese literature called "古文觀止guanzhi" in two ways! Moreover, I also crawl many other material from that website to enrich my service,such as __295 classic book,15919 authors,20500 aritcle from book, and 1999 quotation from book.__

- When deploying on to the MicroSoft Azure web service and MySQL successfully in the final stage, I have been awared that whatever torture or difficulties I faced during the stage of developing __do not mean something!__


---
# Next, there are two ways for those who is normal user or coder:
> ##  Normal user: 

### - Typing web site on the browser, and enjoying the service.

> ## Coder: 

### - In addition to examining web service, I would farely like to introduce my project step by step in a organized way to you, and expect it would be beneficial to get you envolved in my project.


---

# For Normal user!!
> ### Typing https://chineseliterature.azurewebsites.net/   on the browser will get message of __"get Page not found (404)" expectedly__, so you may reference the instructions as below:
### 1. /bookInfo/    --> inspect information of classic books
- Browsing information for classic books in __simplified Chinese__, try this way:

    - https://chineseliterature.azurewebsites.net/bookInfo/

- Browsing specific information of the classic book in __simplified Chinese__, try this way:

    - https://chineseliterature.azurewebsites.net/bookInfo/numbers/    numbers between 1~295
    
- Browsing information for classic books in __traditional Chinese__, try this way:

    - https://chineseliterature.azurewebsites.net/bookInfo/s/
    
- Browsing specific information of the classic book in __traditional Chinese__, try this way:

    - https://chineseliterature.azurewebsites.net/bookInfo/numbers/s/    numbers between 1~295

### 2.  /authorInfo/    --> inspect information of authors
- Browsing information for authors in __simplified Chinese__, try this way:

    - https://chineseliterature.azurewebsites.net/authorInfo/

- Browsing specific information of the author in __simplified Chinese__, try this way:

    - https://chineseliterature.azurewebsites.net/authorInfo/numbers/    numbers between 1~15919
    
- Browsing information for authors in __traditional Chinese__, try this way:

    - https://chineseliterature.azurewebsites.net/authorInfo/s/
    
- Browsing specific information of the author in __traditional Chinese__, try this way:

    - https://chineseliterature.azurewebsites.net/authorInfo/numbers/s/    numbers between 1~15919

### 3.  /quotaInfo/    --> inspect information of quotations from classic books
- Browsing information for quotations in __simplified Chinese__, try this way:

    - https://chineseliterature.azurewebsites.net/quotaInfo/

- Browsing specific information of the author in __simplified Chinese__, try this way:

    - https://chineseliterature.azurewebsites.net/quotaInfo/numbers/    numbers between 1~1999
    
- Browsing information for author in __traditional Chinese__, try this way:

    - https://chineseliterature.azurewebsites.net/quotaInfo/s/
    
- Browsing specific information of the author in __traditional Chinese__, try this way:

    - https://chineseliterature.azurewebsites.net/quotaInfo/numbers/s/    numbers between 1~1999


### 4.  /search/    --> searching information about authors or classic books via keywords
- Browsing information for classic books or authors in __simplified Chinese__, try this way:

```
- https://chineseliterature.azurewebsites.net/search/keywords 
ex: replace "keywords" with 古文观止 or 孙武
https://chineseliterature.azurewebsites.net/search/古文观止/
https://chineseliterature.azurewebsites.net/search/孙武/
```

    
- Browsing information for classic books or authors in __traditional Chinese__, try this way:

```
- https://chineseliterature.azurewebsites.net/search/keywords 
ex: replace "keywords" with 古文觀止 or 李白
https://chineseliterature.azurewebsites.net/search/古文觀止/s
https://chineseliterature.azurewebsites.net/search/李白/s
```


---

# For Coder!!
![Alt text](https://github.com/UnCarter25le/ChineseLiterature/blob/fourth-without-heavy-files/overview_1.png)

# First of all, take a overview:
> # There are four folders here, and..
> ### 1. ChineseLiterature: 
This is __django project__. If you wanna try local service, I sincerely suggest you to modiy conncetion parametors with mysql server locally in two files, __settings.py and views.py__. Moreover, you are albe to use __models.py__ to manipulate and create tables in database named __literature__, __but remenber to create that database first__. You can take a closer look at the Database folder to see what sorts of choices you can reference.
> ### 2. Database:
Here is full of information  about database, such as ERmodel of MySQL, packages needed to import , overview for database via phpmyadmin, etc. Most importantly, I supply two folders, __"YouAlreadyHaveLocalMySQL"__ and __"YouWannaTryDocker"__, to test the ways of "mysqldump" or "writing data to mysql server locally(whatever docker mysql or local mysql)."
> ### 3. PhotoSet:
Here is full of photos about packages needed when crawling and __data structure__ very crucial to this project.
>### 4. DataSetAndPrograms:
Here is abundant in data set in json format and programs for crawling from website or write data into database. You can try __"crawlerForGuanzhi.py" to get entire content of book in approximately 20 minutes!__ Make sure to have these data set before taking "writeDataToDatabase_*.py" a shot, __especially folders named "作者的照片","古籍","古籍的照片"__.


# Secondly,
> ### 1. Do not trying to writing data? Just pull branch: fourth-without-heavy-files.
> ### 2. Wanna try to inserting data, please pull branch: fourth-with-heavy-files(1.2GB or so).

# Thirdly, importand package edition.
> ### python-3.6.6
> ### django-1.9.10
> ### mysql_server-5.7.25


# Fourth, detailed info for first part.
> ### 1. ChineseLiterature: 

- #####  Make sure the connection parametors in these files when you trying to connect mysql server locally.

```
settings.py:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'literature',
        'USER':'root',     #here u should notice!
        'PASSWORD':'1234', #here u should notice!
        'HOST':'127.0.0.1',
        'PORT':'3306',
        'OPTIONS': {'charset':'utf8mb4'},
    }
}
```


```
views.py                                    user and passwd u should notice!
conn = pymysql.connect('localhost',port=3306,user='root',passwd='1234',charset='utf8',db='literature')
```

- ##### Because I make decision to __create tables via django ORM__ instead of executing SQL command via pymysql, you had better __create a database named "literature" in utf8mb4 format first__, and follow commands as bellow:


    cd ChineseLiterature/

    find . -path "*/migrations/*.py" -not -name "__init__.py" -delete

    find . -path "*/migrations/*.pyc"  -delete

    python manage.py makemigrations

    python manage.py migrate



- ##### More detailed info about utf8mb4 and how many processes in completing migraing tables in database via models.py, you can reference...

```
1. https://blog.csdn.net/boycycyzero/article/details/42879911
2. cd Database/YouAlreadyHaveLocalMySQL/      
3. vim Instruction
```

> ### 2. Database:

<b>   <b>


> ### 3. PhotoSet:


> ### 4. DataSetAndPrograms:
>
>
>

    code(sddsfdsfsdf)
