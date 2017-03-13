#! usr/bin/python
# -*-encoding:utf-8 -*-


from flask import Flask
from flask import request
from flask import make_response
from flask import redirect
from flask import abort
from flask_script import Manager

app = Flask(__name__)
# flask_script 扩展程序，管理第三方扩展
manager = Manager(app)

#静态根路由
@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    return '''<h1>hello flask with qiangge,
    User-Agent is
    %s </h1>''' %user_agent

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


@app.route('/404')
def errorhandle():
    return '<h1>this is about error handler </h1>'

# 动态路由
@app.route('/user/<name>')
def user(name):
    return '<h1>hello , %s,welcom to user flask !</h1>' %name




if  __name__ == '__main__':
    # app.run(debug=True)
    manager.run()
