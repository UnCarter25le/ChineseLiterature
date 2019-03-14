"""ChineseLiterature URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from literature import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^bookInfo/$',views.getBookInfo),
    url(r'^bookInfo/([a-z]+)/$',views.getBookInfo),
    url(r'^bookInfo/(\d+)/$',views.getBookDetail),
    url(r'^bookInfo/(\d+)/([s])/$',views.getBookDetail),
    url(r'^authorInfo/$',views.getAuthorInfo),
    url(r'^authorInfo/([a-z]+)/$',views.getAuthorInfo),
    url(r'^authorInfo/(\d+)/$',views.getAuthorDetail),
    url(r'^authorInfo/(\d+)/([s])/$',views.getAuthorDetail),
    url(r'^quotaInfo/$',views.getQuotaInfo),
    url(r'^quotaInfo/([a-z]+)/$',views.getQuotaInfo),
    url(r'^quotaInfo/(\d+)/$',views.getQuotaDetail),
    url(r'^quotaInfo/(\d+)/([s])/$',views.getQuotaDetail),
    url(r'^search/$',views.getSearchResult),
    url(r'^search/(\s*\w+\s*\w*)/$',views.getSearchResult),
    url(r'^search/(\s*\w+\s*\w*)/([s])$',views.getSearchResult),
]
