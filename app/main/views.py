from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import User
from . import main
from .forms import NameForm


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True

        # old_name = session.get('name')
        # if old_name is not None and old_name != form.name.data:
            # flash("looks like you have change your name")
        session['name'] = form.name.data
        return redirect(url_for('main.index'))
    return render_template('index.html',
                           form=form,
                           name=session.get('name'),
                           known=session.get('known', False))