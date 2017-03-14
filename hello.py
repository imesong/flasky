#! usr/bin/python
# -*-encoding:utf-8 -*-


from flask import Flask, render_template, session, redirect, url_for, make_response, flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
import os
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail, Message

basedir = os.path.abspath(os.path.dirname(__file__))
print('basedir == ', basedir)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'woshiqiangge'
# 数据库相关
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

#Mail 服务器
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")


# flask_script 扩展程序，管理第三方扩展
manager = Manager(app)
# UI渲染
bootstrip = Bootstrap(app)
# 客户端时间本地化
moment = Moment(app)
# 数据库对象
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

mail = Mail(app)

#静态根路由
@app.route('/', methods=['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if user is None:
            user = User(name=form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True

        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash("looks like you have change your name")
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html',
                           form=form,
                           name=session.get('name'),
                           known=session.get('known', False))


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
def page_not_found():
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_fault():
    return render_template('500.html'), 500


# 动态路由 使用 Jinjia2 接收变量 name
@app.route('/<name>')
def user(name):
    return render_template('user.html', name=name)


# Jinjia2 中渲染 集合，验证了集合中内容是无序存储的
@app.route('/comments')
def comment():
    args = {'a', 'b', 'c', 'd', 'e', 'f', 'g'}
    return render_template("comments.html", comments=args)


class NameForm(Form):
    name = StringField("what's your name ?", validators=[DataRequired()])
    submit = SubmitField('Submit')


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    user = db.relationship('User', backref='Role')

    def __repr__(self):
        return "<Role> %r=" % self.name


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

if __name__ == '__main__':
    # app.run(debug=True)
    manager.run()
