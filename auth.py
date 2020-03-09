# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_template, redirect, url_for, session, g
from excute_sql import *
from werkzeug.security import check_password_hash, generate_password_hash
from templates.auth import *
import functools

conn, cursor = get_db()

auth_bp = Blueprint('auth', __name__ )


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None
        if not username or not password:
            error = '用户名或密码错误'
        else:
            select_result = cursor.execute('select * from userinfo where username = ?', (username, )).fetchone()

            if select_result:
                if check_password_hash(select_result['password'], password):
                    session.clear()
                    session['user_id'] = select_result['id']
                    session['user_name'] = username
                    return redirect(url_for('artical.articel_list'))
                else:
                    error = '密码错误'
            else:
                return render_template('auth/register.html')
    else:
        return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None
        if not username:
            error = '请输入用户名或密码'
        elif not password:
            error = '请输入用户名或密码'
        else:
            select_result = cursor.execute('select * from userinfo where username = ?', (username,)).fetchone()
            if select_result:
                error = '用户存在'
            else:
                cursor.execute('INSERT INTO userinfo (username, password) VALUES (?, ?)',
                           (username, generate_password_hash(password)))
                conn.commit()
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html')


@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = cursor.execute(
            'SELECT * FROM userinfo WHERE id = ?', (user_id,)
        ).fetchone()


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('artical.articel_list'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view