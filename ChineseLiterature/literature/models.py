from django.db import models

from django.utils import timezone

import jsonfield  #JSONField()，透過ORM在mysql創建的型態是longtext表示。

# from compositefk.fields import CompositeForeignKey
# import codecs
# codecs.register(lambda name: codecs.lookup('utf8') if name == 'utf8mb4' else None)


# Create your models here.
 
# 不加會員的話，共7張表

# (1)建立好表格，第一次migrate後，在既有表格內增減欄位，更改欄位屬性是ok的，第二次migrate沒問題。
# (2)建立好表格，第一次migrate後，自行在mysql裡更改表格內的欄位或屬性，甚至操作表格本身，無法透過migrate再同步回來。(非常不建議不透過models.py來修改資料庫)
# (3)建立好表格，第一次migrate後，透過models.py裡註解掉某一class同時取消admin.py的註冊，再migrate後，可達到刪除資料庫特定表格。
# (4) 不建議未刪除table A的情況下，直接更改table A名稱接著migrate，似乎會影響表跟表之間的FK關係。即使migrate --fake後，也無法解決問題。
# (5) 如果table A table B之間有FK的關聯，是無法直接透過註解table A達到刪除表格。
# (6)重置migrations紀錄 # https://simpleisbetterthancomplex.com/tutorial/2016/07/26/how-to-reset-migrations.html

##(table 1)
class ClassicBook(models.Model):
    book_id = models.PositiveSmallIntegerField(primary_key=True) # 數字約 0 to 32767 
    author_id = models.ForeignKey('Author',on_delete=models.CASCADE)
    bookName_SimCh = models.CharField(max_length=30,null=False,default="None") #CharField's max_length=255 ；一個漢字3的byte；CharField在mysql裡是char，加了max_length變成varchar。
    bookIntro_SimCh = models.TextField(null=False,default="None") #TextField usually give up max_length
    bookName_TradiCh = models.CharField(max_length=30,null=False,default="None")
    bookIntro_TradiCh = models.TextField(null=False,default="None") 
    bookImg = models.TextField(null=False,default="None") #不考慮BinaryField，用TextField儲存base64位元字串
    bookImg_Uri = models.URLField(max_length=100,null=False,blank=True,default="None")
    quotation = jsonfield.JSONField(null=False,default=["None","None"]) #陣列
    domain_Url = models.URLField(max_length=30,null=False,default="None")
    book_Urn = models.URLField(max_length=60,null=False,default="None")
    
    def __str__(self):
        return self.bookName_SimCh


##(table 2)
class ClassicBook_Content(models.Model):
    innerChapter_id = models.PositiveIntegerField(primary_key = True) # 0 to 2147483647
    book_id = models.ForeignKey('ClassicBook',on_delete=models.CASCADE)
    upperChapter_SimCh = models.CharField(max_length=30,null=False,default="None")
    innerChapter_SimCh = models.CharField(max_length=120,null=False,default="None")
    chapterContent_SimCh = jsonfield.JSONField(null=False,default=["None"])#陣列
    upperChapter_TradiCh = models.CharField(max_length=30,null=False,default="None")
    innerChapter_TradiCh = models.CharField(max_length=120,null=False,default="None")
    chapterContent_TradiCh = jsonfield.JSONField(null=False,default=["None"])#陣列
    domain_Url = models.URLField(max_length=30,null=False,default="None")
    innerChapter_Urn = models.URLField(max_length=60,null=False,default="None")
    
    def __str__(self):
        return self.innerChapter_SimCh

#(table 3)
class Quotation_From_ClassicBook(models.Model):
    quotation_id = models.AutoField(primary_key=True)
    innerChapter_id = models.ForeignKey('ClassicBook_Content',on_delete=models.CASCADE)
    quotation_SimCh = models.CharField(max_length=255,null=False,default="None")
    quotaTranslation_SimCh = models.TextField(null=False,default="None") #考慮改成text
    quotaFrom_SimCh = models.CharField(max_length=100,null=False,default="None")
    quotation_TradiCh = models.CharField(max_length=255,null=False,default="None")
    quotaTranslation_TradiCh = models.TextField(null=False,default="None") #考慮改成text
    quotaFrom_TradiCh = models.CharField(max_length=100,null=False,default="None")

    def __str__(self):
        return self.quotation_SimCh

#(table 4)
class Author(models.Model):
    author_id = models.PositiveIntegerField(primary_key=True)# 0 to 2147483647
    authorName_SimCh = models.CharField(max_length=30,null=False,default="None")
    authorIntro_SimCh = models.TextField(null=False,default="None")
    dynasty_SimCh = models.CharField(max_length=20,null=False,default="None")
    authorName_TradiCh = models.CharField(max_length=30,null=False,default="None")
    authorIntro_TradiCh = models.TextField(null=False,default="None")
    dynasty_TradiCh = models.CharField(max_length=20,null=False,default="None")
    worksNum = models.PositiveSmallIntegerField(null=False,default=0) #約 0 to 32767 
    authorImg = models.TextField(null=False,blank=True,default="None")#不考慮BinaryField，用TextField儲存base64位元字串
    authorImg_Uri = models.URLField(max_length=100,null=False,blank=True,default="None")
    authorCodeName = models.CharField(max_length=20,null=False,default="None")
    domain_Url = models.URLField(max_length=30,null=False,default="None")
    author_Urn = models.URLField(max_length=60,null=False,default="None")
    works_Urn = jsonfield.JSONField(null=False,default=["None"]) #陣列

    def __str__(self):
        return self.authorName_SimCh

#(table 5) 得第二階段再做了。
# class Poem_And_Article(models.Model):
#     content_id = models.PositiveIntegerField(primary_key=True)# 0 to 2147483647
#     author_id = models.ForeignKey('Author',on_delete=models.CASCADE)
#     theme_SimCh =  models.CharField(max_length=60,null=False,default="None")
#     content_SimCh = models.TextField(null=False,default="None")
#     theme_TradiCh =  models.CharField(max_length=60,null=False,default="None")
#     content_TradiCh = models.TextField(null=False,default="None")
#     domain_Url = models.URLField(max_length=30,null=False,default="None")
#     content_Urn = models.URLField(max_length=60,null=False,default="None")
#     contentCodeName =  models.CharField(max_length=20,null=False,default="None")

#     def __str__(self):
#         return self.theme_SimCh

#(table 6)   得第三階段再做了。
# class Quotation_From_Poem_And_Article(models.Model):
#     quotation_id = models.AutoField(primary_key=True)
#     author_id = models.ForeignKey('Author',on_delete=models.CASCADE)
#     content_id = models.ForeignKey('Poem_And_Article',on_delete=models.CASCADE)
#     quotation_SimCh =models.CharField(max_length=255,null=False,default="None")  #考慮改成text
#     quotation_TradiCh =models.CharField(max_length=255,null=False,default="None")  #考慮改成text

#     def __str__(self):
#         return self.quotation_SimCh

#(合併進作者)
# class Dynasty_SimCh(models.Model):
#     dynasty_id = models.PositiveSmallIntegerField(primary_key=True)#約 0 to 32767 
#     dynastySimCh = models.CharField(max_length=20,null=False,default="None")

#     def __str__(self):
#         return self.dynastySimCh

# class Member(models.Model):
#     member_id = models.AutoField(primary_key=True)
#     account = models.CharField(max_length=20,null=False,default="None",blank=True)
#     authAccount = models.CharField(max_length=100,null=False,default="None")
#     salt = models.CharField(max_length=100,null=False,default="None")
#     is_active = models.NullBooleanField(null=False,default=True)

#     def __str__(self):
#         return self.account

# class AddPoemAndArticleTo:
#     Member_id = models.ForeignKey('Member',on_delete=models.CASCADE)
#     Content_id = models.ForeignKey('PoemAndArticle',on_delete=models.CASCADE)
#     class Meta:
#         AddCompositePK = [('Member_id','Content_id'),]
    
#     def __str__(self):
#         return self.AddCompositePK

# class AddBookTo:
#     Member_id = models.ForeignKey('Member',on_delete=models.CASCADE)
#     Book_id = models.ForeignKey('ClassicBook',on_delete=models.CASCADE)
#     class Meta:
#         AddCompositePK = [('Member_id','Book_id'),]
#     def __str__(self):
#         return self.AddCompositePK



#https://stackoverflow.com/questions/26719088/django-1-7-blank-charfield-textfield-convention
# 對表格新增新的FK時，可以注意的事項。

#https://stackoverflow.com/questions/25924858/django-1-7-migrate-gets-error-table-already-exists

# Under the circumstance where several tables in DB don't be used in models.py, 
# we can use command:'python manage.py migrate --fake <appname>'  to have a choice to delete those.