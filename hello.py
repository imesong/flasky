#! usr/bin/python
# -*-encoding:utf-8 -*-


from flask import Flask,render_template,session,redirect,url_for,make_response,flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment

from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = 'woshiqiangge'

# flask_script 扩展程序，管理第三方扩展
manager = Manager(app)
# UI渲染
bootstrip = Bootstrap(app)
# 客户端时间本地化
moment = Moment(app)

#静态根路由
@app.route('/',methods=['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash("looks like you have change your name")
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html',form=form,name=session.get('name'))

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


class NameForm(Form):
    name = StringField("what's your name ?",validators=[DataRequired()])
    submit = SubmitField('Submit')


if  __name__ == '__main__':
    # app.run(debug=True)
    manager.run()
