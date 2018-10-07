# -*- coding:utf-8 -*-
# --------------------
# Author:       SDN
# Description:	路由器
# --------------------

from module.generation.handler import user_handler

HANDLERS = [
    # 后台
    (r'/', user_handler.LoginHandler),  # 登陆
    (r'/login', user_handler.LoginHandler),  # 登陆
    (r'/logout', user_handler.LogoutHandler),  # 登出
    (r'/user', user_handler.UserHandler),  # 员工管理

    (r'/xxx', user_handler.UserHandler0),  # 员工管理


    # # 基本信息
    # (r'/basic/(\w+)', module.generation.handler.BasicHandler.BasicHandler),  # 公司基本信息设置
    # (r'/basic-edit/(\w+)', module.generation.handler.BasicHandler.BasicEditHandler),  # 编辑
    #
    # # 公司概况
    # (r'/manage-about/(\w+)', module.generation.handler.AboutHandler.AboutHandler),  # 公司概况
    # (r'/manage-about-discard/(\w+)', module.generation.handler.AboutHandler.AboutDiscardHandler),  # 公司概况
    #
    # # 文件接收
    # (r'/manage/file/image', module.generation.handler.FileHandler.ImageHandler),  # 富文本图片
    # (r'/file/ajax', module.generation.handler.FileHandler.FileUploadAjaxHandler),   # 附件上传
    #
    #
    # (r'/selector/(.*)', module.generation.handler.SelectorHandler.SelectorHandler),
    # (r'/selector-make/(.*)', module.generation.handler.SelectorHandler.SelectorMakeHandler),
    # (r'/selector-delete/(.*)', module.generation.handler.SelectorHandler.SelectorDelHandler),


]
