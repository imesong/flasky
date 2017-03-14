#! usr/bin/python
# -*-encoding:utf-8 -*-


from flask import Flask,render_template
from flask import make_response
from flask import redirect
from flask_script import Manager
from flask_bootstrap import Bootstrap

app = Flask(__name__)
# flask_script 扩展程序，管理第三方扩展
manager = Manager(app)
bootstrip = Bootstrap(app)

#静态根路由
@app.route('/')
def index():
    return render_template('index.html')

# 响应测试
@app.route("/response")
def response():
    response = make_response('<h1>This document with cookies</h1>')
    response.set_cookie('name','imesong')
    response.set_cookie('password','imesong')
    # 客户端如何获取 cookie 中的数据呢
    return response

#重定向
@app.route('/redirect')
def redir():
    return redirect('http://www.baidu.com')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html') ,404

@app.errorhandler(500)
def server_fault(e):
    return render_template('500.html'),500

# 动态路由 使用 Jinjia2 接收变量 name
@app.route('/<name>')
def user(name):
    return render_template('user.html', name = name)


# Jinjia2 中渲染 集合，验证了集合中内容是无序存储的
@app.route('/comments')
def comment():
    args = {'a','b','c','d','e','f','g'}
    return  render_template("comments.html",comments = args)



def about():
    return render_template("about.html")

if  __name__ == '__main__':
    # app.run(debug=True)
    manager.run()
