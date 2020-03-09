# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_template, redirect, url_for, g, flash
from excute_sql import *
from templates.auth import *
from auth import conn, cursor
from templates.article import *

from auth import login_required
"""
文章列表的展示
文章的修改
文章的编辑
文章的删除
"""

artical_bp = Blueprint('artical', __name__)


@artical_bp.route('/')
def articel_list():
    data_list = cursor.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM article p JOIN userinfo u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('article/article_list.html', result=data_list)



@artical_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_artical():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('body')
        error = None
        if not title:
            error = 'TITLE IS REQUIRED '
        if error is not None:
            flash(error)
        else:
            print(g.user)
            cursor.execute('INSERT INTO article (title, body, author_id)'
                       ' VALUES (?, ?, ?)',
                       (title, content, g.user['id']))
            conn.commit()
            return redirect(url_for('artical.articel_list'))
    return render_template('article/create.html')



def select_artical(artical_id, check_author=True):
    result = cursor.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM article p JOIN userinfo u ON p.author_id = u.id'
        ' WHERE p.id = ?', (artical_id,)
    ).fetchone()
    if result is None:
        return render_template('404error.html')
    if check_author and result['author_id'] != g.user['id']:
        return render_template('404error.html')
    return  result





@artical_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_artical(id):
    result = select_artical(id)
    print('select artical id', result)
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('body')
        error = None
        if not title:
            error = 'Title is required.'
        if error is not None:
            flash(error)
        else:
            cursor.execute('UPDATE article SET title = ?, body = ?  WHERE id = ?', (title, content, int(id)))
            conn.commit()
            return redirect(url_for('artical.articel_list'))
    return render_template('article/update.html', result=result)


@artical_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
    select_artical(id)
    cursor.execute('DELETE FROM article WHERE id = ?', (id, ))
    conn.commit()
    return redirect(url_for('artical.articel_list'))





