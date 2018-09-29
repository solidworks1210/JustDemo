# -*- coding:utf-8 -*-


from modules.common.handler import error
from modules.auth.handler import login
from modules.auth.handler import user
from modules.index.handler import index
from modules.share.handler import share

HANDLERS = [

    (r'/', index.IndexHandler),
    (r'/error', error.AuthErrorHandler),
    (r'/login', login.LoginHandler),
    (r'/logout', login.LogoutHandler),
    (r'/user', user.UserHandler),
    (r'/user/(.*)', user.UserProfileHandler),
    (r'/share', share.IndexHandler),
    (r'/download', share.DownloadHandler),


    (r'/(.*)', error.NotFoundHandler),  # 未定义路由（需放在最后）
]
