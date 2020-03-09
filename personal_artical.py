
# -*- coding: utf -8 -*-
from flask import Blueprint, redirect, render_template, request, g, url_for, flash
from auth import conn, cursor
from artical import select_artical
from templates.personal import *
from auth import login_required
"""
根据用户名,筛选出,属于该用户的所有文章

"""
person_bp = Blueprint('personal_artical', __name__)


@person_bp.route('/<int:id>/personal', methods=['GET', 'POST'])
def personal_artical_list(id):
    result = result = cursor.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM article p JOIN userinfo u ON p.author_id = u.id'
        ' WHERE p.author_id  = ?', (id,)
    ).fetchall()
    if result:
        return render_template('personal/personal_list.html', datas=result)
    else:
        return """目前作者没有写过文章"""



@person_bp.route('/personal/create', methods=['GET', 'POST'])
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
            return redirect(url_for('artical.articel_list', id=g.user['id']))
    return render_template('personal/create_persona_artical.html')



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





@person_bp.route('/<int:id>/personal/update', methods=['GET', 'POST'])
@login_required
def update_artical(id):
    result = select_artical(id)
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
            return redirect(url_for('personal_artical.personal_artical_list', id=result['author_id']))
    return render_template('personal/update_personal_artical.html', result=result)


@person_bp.route('/<int:id>/personal/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
    result = select_artical(id)
    cursor.execute('DELETE FROM article WHERE id = ?', (id, ))
    conn.commit()
    return redirect(url_for('personal_artical.personal_artical_list', id=result['author_id']))

