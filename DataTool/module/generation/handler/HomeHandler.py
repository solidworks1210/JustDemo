# -*- coding:utf-8 -*-
# --------------------
# Author:       SDN
# Description:	后台管理首页，员工管理
# Time:         2017/3/1
# --------------------

import tornado.web

from BaseHandler import BaseHandler
from utils import TimeUtils
from ..model import HomeModel


class HomeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, role):
        try:
            result = self.get_argument('result', '100')
            page_current = self.get_argument('page_current', '1')
            args = self.render_params
            args['navi_main'] = 'home'
            args['navi_sub'] = ''
            args['title_page'] = '首页管理'
            args['title_content'] = ''
            args['role_page'] = ''
            args['role_admin'] = self.get_current_user_role()
            args['name_admin'] = self.get_current_user_name()
            args['page_current'] = page_current
            args['result'] = result

            if role == 'description':    # 公司介绍
                result = HomeModel.get_desc()
                args['navi_sub'] = 'home-description'
                args['id'] = result['id']
                args['title_content'] = '公司介绍'
                args['role_page'] = 'description'
                args['content'] = result['content']
                self.render('manage_new/home_desc.html', **args)
            else:
                self.write('false')
        except Exception as e:
            print __name__, 'get出错：', e
            self.redirect('/manage')


    @tornado.web.authenticated
    def post(self, role):
        try:
            if role == 'description':   # 保存修改（描述）
                id_item = self.get_argument('id', strip=True)
                content = self.get_argument('content', strip=True)
                # 将数据写入数据库
                result = HomeModel.save_descr(id_item=id_item, content=content)
                if result != -1:
                    self.write('success')
                else:
                    self.write('false')
            else:
                self.write('false')
        except Exception as e:
            print __name__, 'post，失败：', e
            self.redirect('/manage')



