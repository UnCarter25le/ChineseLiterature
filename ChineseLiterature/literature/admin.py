from django.contrib import admin
from literature import models
import jsonfield

# Register your models here.


class ClassicBookAdmin(admin.ModelAdmin):
    list_display = ('book_id','bookName_SimCh','bookIntro_SimCh','bookName_TradiCh','bookIntro_TradiCh','bookImg_Uri','quotation','domain_Url','book_Urn','author_id_id')
    ordering=('book_id',)
admin.site.register(models.ClassicBook,ClassicBookAdmin)


# class ClassicBook_ContentAdmin(admin.ModelAdmin):
#     list_display = ('upperChapter_SimCh','domain_Url')
    # ordering=('domain_Url',)
# admin.site.register(models.ClassicBook_Content,ClassicBook_ContentAdmin)
admin.site.register(models.ClassicBook_Content)


class Quotation_From_ClassicBookAdmin(admin.ModelAdmin):
    list_display =  ('quotation_id','quotation_SimCh','quotaFrom_SimCh','quotation_TradiCh','quotaFrom_TradiCh')#,'innerChapter_id_id')
    ordering=('quotation_id',)
admin.site.register(models.Quotation_From_ClassicBook,Quotation_From_ClassicBookAdmin)
# admin.site.register(models.Quotation_From_ClassicBook)


class AuthorAdmin(admin.ModelAdmin):
    list_display =  ('author_id','authorName_SimCh','authorIntro_SimCh','dynasty_SimCh','authorName_TradiCh','authorIntro_TradiCh','dynasty_TradiCh','worksNum','authorImg_Uri','authorCodeName','domain_Url','author_Urn','works_Urn')
    ordering=('author_id',)
admin.site.register(models.Author,AuthorAdmin)

# admin.site.register(models.Poem_And_Article_SimCh)

# admin.site.register(models.Quotation_From_Poem_And_Article_SimCh)

# admin.site.register(models.Dynasty_SimCh)

# admin.site.register(models.Member)

# admin.site.register(models.AddBookTo)

# admin.site.register(models.AddPoemAndArticleTo)

