from flask import Flask,render_template
from conn import conn # 导入conn.py
app=Flask(__name__)

# 数据库连接配置
conn()


@app.route('/')
def index():
    return render_template('test.html')

@app.route('/index')
def home():
    return render_template('test.html')

@app.route('/movie')
def movie():
    dataList=[] # 存取数据库数据
    con = conn()
    cur=con.cursor() # 获取游标
    sql = 'select * from doubantop250'
    cur.execute(sql)
    dats = cur.fetchall()
    for item in dats:
        dataList.append(item)

    cur.close()
    con.close()
    return render_template('movie.html',movies=dataList)

@app.route('/score')
def score():
    score = []  # 存取评分数据
    num=[]      # 存取各个评分的数量
    con = conn()
    cur = con.cursor()  # 获取游标
    sql = 'select score,count(score) from doubantop250 group by score'  # group by score实现数据分段
    cur.execute(sql)
    dats = cur.fetchall()

    for item in dats:
        score.append(item[0])
        num.append(item[1])

    cur.close()
    con.close()
    return render_template('score.html',score=score,num=num)

@app.route('/word')
def word():
    return render_template('word.html')

@app.route('/term')
def term():
    return render_template('term.html')

if __name__=='__main__':
    app.run(debug=True)