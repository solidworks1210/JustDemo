# -*- coding:utf-8 -*- 
# --------------------
# Author:       SDN
# Description:  
# --------------------

from flask import Flask

app = Flask(__name__)


# 默认情况下，路由只回应 GET 请求，但是通过 route() 装饰器传递 methods 参数可以改变这个行为。
@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username


@app.route('/user/<username>/')
def show_user_profile2(username):
    # show the user profile for that user
    return 'User2: %s' % username


# @app.route('/post/<float:post_id>')
@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


if __name__ == '__main__':
    app.debug = False

    # 这会让操作系统监听所有公网IP
    app.run(host='0.0.0.0')
