import pymysql
pymysql.install_as_MySQLdb()

# django使用docker 的mysql發生錯誤！
#django.core.exceptions.ImproperlyConfigured: Error loading MySQLdb module: No module named 'MySQLdb'
# 解法：upperProjectFolder/__init__.py 增添使用pymysql! 參考下列連結。
#https://www.jianshu.com/p/82781add8449  https://blog.51cto.com/10250691/1918629 #解決docker run mysql 了，django卻還不能連進去的問題
# 結論：python2 用'MySQLdb'，和python3的pymysql不兼容了