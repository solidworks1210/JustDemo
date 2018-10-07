# -*- coding:utf-8 -*- 
# --------------------
# Author:       SDN
# Description:	后台的基础Handler
# --------------------

import tornado.web

from config import category
from config import config


class BaseHandler(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        # 渲染页面时，要传入的参数表
        self.category = category.category_manage
        self.render_params = dict(
            navi_main='',  # 一级标题标签(导航栏, 左侧导航栏)
            navi_sub='',  # 二级标题标签(导航栏，左侧导航栏)
            title_page='',  # 浏览器标签栏显示的标题
            title_content='',  # 内容区显示的标题
            url_navi1='',  # 右侧内容区导航栏
            url_navi2='',  # 右侧内容区导航栏
            title_navi1='',  # 右侧内容区导航栏
            title_navi2='',  # 右侧内容区导航栏

            role_page='',  # 当前页面的角色（根据需要赋值）
            role_admin='',  # 用户角色：超级管理员 or 普通管理员
            role_user='',  # 文件使用者的角色，由于文件的分类保存

            name_admin='',  # 用户名
            page_current=0,  # 当前要显示的页数，这儿给个默认值，后面修改
            page_total=100,  # 总共的页数，这儿给个默认值，后面修改
            items=[],  # 给个默认值，避免没添加，模板渲染异常（根据需要赋值）
            content='',  # 内容（根据需要赋值）
            id='',  # （根据需要赋值）
        )
        super(BaseHandler, self).__init__(application, request, **kwargs)

    def get_int(self, name_args, default_value=None):
        """
        将前端传来的数据转为整数
        :param name_args: 前端传递参数的名字
        :param default_value: 参数不存在，返回的默认值
        :return:
        """
        try:
            result_temp = self.get_argument(name_args, strip=True)
            return int(result_temp)
        except:
            if default_value:
                return default_value
            else:
                raise __name__ + '出错'

    def get_current_user(self):
        """
        登陆成功后，添加安全cookie时，值为name和角色的组合：name_role
        :return:
        """
        return self.get_secure_cookie(config.H_SECRETE_COOKIE)

    def get_current_user_name(self):
        """
        登陆成功后，添加安全cookie时，值为name和角色的组合：name_role
        :return:
        """
        name_role = self.get_current_user()
        if name_role:
            return name_role.split('_')[0]

    def get_current_user_role(self):
        """
        登陆成功后，添加安全cookie时，值为name和角色的组合：name_role
        :return:
        """
        name_role = self.get_current_user()
        if name_role:
            return name_role.split('_')[1]

    def get_str_default(self, keyy, default, exception=False):
        if not exception:
            result = self.get_argument(keyy, strip=True)
            if len(result) > 0:
                return result
            else:
                return default
        else:
            result = self.get_argument(keyy, strip=True, default=default)
            if len(result) > 0:
                return result
            else:
                return default
