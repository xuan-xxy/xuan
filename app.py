# -*- coding: utf-8 -*-
"""
创建一个博客园区: 主要功能:登录, 注册, 编辑, 展示, 删除,修改, 上传图片,

"""
from flask import Flask
import auth
import os
import artical
import personal_artical

app = Flask(__name__)
app.secret_key = os.urandom(16)


@app.route('/hello')
def hello():
    return 'hello world'

app.register_blueprint(auth.auth_bp)
app.register_blueprint(artical.artical_bp)
app.register_blueprint(personal_artical.person_bp)

if __name__ == '__main__':
    app.run(debug=True)
