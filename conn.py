import pymysql # 引入mysql
# 数据库连接配置
def conn():
    # 创建连接
    return  pymysql.connect(host="localhost", user="root", password="123456", database="douban", port=3306)