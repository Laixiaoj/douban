import urllib
import urllib.request as ur
import time
from bs4 import BeautifulSoup      # 网页分析，获取网页信息
import re                          # 正则表达式。进行文字匹配
import urllib.request,urllib.error # 制定URL,获取网页数据
from conn import conn              # 导入conn.py

# 创建正则模式对象规则
# 获取超链接
findLink=re.compile(r'<a href="(.*?)">')
# 获取图片
findImgSrc=re.compile(r'<img.*src="(.*?)"',re.S) # re.S让换行符包含在其中
# 获取片名
findTitle=re.compile(r'<span class="title">(.*?)</span>')
# 获取评分
findRate=re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# 获取评价人数
findJudge=re.compile(r'<span>(\d*)人评价</span>') # (\d*)
# 获取概括
findInq=re.compile(r'<span class="inq">(.*?)</span>')

def main(): # main主函数
    # 获取网页IP
    baseUrl='https://movie.douban.com/top250?start='
    # 1.爬取IP
    dataList=getDate(baseUrl)

    # 2.保存爬取数据到Mysql数据库
    saveDate_DB(dataList)
    pass

# 爬取IP
def getDate(baseurl):

    dateList=[]

    for i in range(0,10):
        url=baseurl+str(25*i) # 调节页数，记得转类型
        html=askUrl(url) # return html，保存获取url信息
        # print(html)
        # 解析数据
        bs=BeautifulSoup(html,'html.parser')
        for item in bs.find_all('div',class_='item'):  # 匹配符合的字符串并且形成列表,class加_因为class是关键字
            # print(item)
            date=[] # 保存一部电影的全部信息
            item=str(item) # 转化类型
            # 根据正则模式匹配
            link=re.findall(findLink,item)[0] # 正则查找指定字符串,（[0]将列表转化掉）
            date.append(link)

            imgSrc=re.findall(findImgSrc,item)[0]
            date.append(imgSrc)

            Title=re.findall(findTitle,item) # 这里需要去掉[0]，保留列表形式
            if len(Title)==2: # 可能存在两个标题
                fTitle=Title[0]
                date.append(fTitle)
                tTitle=Title[1].replace(r'/','') # 替代掉无关字符，r避免转义字符
                tTitle=re.sub(r'\xa0','',tTitle) # 替代掉\xa0
                date.append(tTitle)
            else:
                date.append(Title[0])
                date.append(" ") # 空格留位即使不存在也要留空

            rate=re.findall(findRate,item)[0]
            date.append(rate)

            judge=re.findall(findJudge,item)[0]
            date.append(judge)

            inq=re.findall(findInq,item) # 可能不存在inq
            if len(inq)!=0:
                nInq=inq[0].replace('。','')
                date.append(nInq)
            else:
                date.append(" ")          # 留空
            # print(link)

            dateList.append(date)         # 列表里面存入子列表

    # print(dateList)

    return dateList

# 访问Url
def askUrl(url):

    headers={  # 注意User-Agent格式，之间没有空格
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    req=urllib.request.Request(url=url,headers=headers) # 封装url
    html=''

# 异常处理
    try:
        response=ur.urlopen(req)
        html=response.read().decode('utf-8')
        time.sleep(2)
       # print(html)

    except urllib.error.URLError as result:
        if hasattr(result,'code'): # hasattr() 函数用于判断对象是否包含对应的属性,有则True，否则False
            print(result.code)  # 输出result类中的成员属性
        if hasattr(result,'reason'):
            print(result.reason)
    return html

# 保存方式：数据库Mysql
def saveDate_DB(dataList):

    init_DB() # 这里先创建表，运行一次即可
    con = conn() # 数据库连接配置
    cur=con.cursor()

    for data in dataList:
        for index in range(len(data)):
            if(index==4 or index==5):
                continue # 排除数字转化字符
            data[index]='"'+data[index]+'"'
        # print(data)
        sql='''
            insert into doubantop250(
            info_link,pic_link,cname,ename,score,rated,introduction)
            values(%s)''' %(",".join(data))
        #print(sql)
        cur.execute(sql)
        con.commit()
    cur.close()
    con.close()

# 初始化database，运行一次即可
def init_DB():
    # 连接数据库
    con = conn()
    # 创建游标对象
    cur = con.cursor()
    # 编写创建表的sql
    sql = """
        create table doubanTop250(
        id int primary key auto_increment,
        info_link varchar(100),
        pic_link varchar(100),
        cname varchar(100),
        ename varchar(100),
        score varchar(100),
        rated varchar(100),
        introduction varchar(100)
        )
    """
    try:
        # 执行创建表的sql
        cur.execute(sql)
        print("创建表成功")
    except Exception as e:
        print(e)
        print("创建表失败")
    finally:
    # 关闭游标连接
        cur.close()
    # 关闭数据库连接
        con.close()

# 启动主函数
if __name__=='__main__':
    # init_db('textDouban.db')
    main()
    print("导入完毕！")