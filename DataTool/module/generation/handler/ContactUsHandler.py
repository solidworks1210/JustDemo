# -*- coding:utf-8 -*- 
# --------------------
# Author:       SDN
# Description:	留言管理
# Time:         2017/3/2
# --------------------

import tornado.web

from BaseHandler import BaseHandler
from config import paging
from ..model import ContactUsModel


class ContactUsHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        render_params = self.render_params
        render_params['page_current'] = self.get_int('page_current', 1)
        render_params['role_admin'] = self.get_current_user_role()
        render_params['name_admin'] = self.get_current_user_name()
        render_params['navi_main'] = 'contact'
        render_params['navi_sub'] = 'contact-contact'
        render_params['title_content'] = '留言管理'
        render_params['title_page'] = '客户留言管理'

        render_params['page_total'], render_params['items'] = ContactUsModel.get_comment(
            page=render_params['page_current'],
            items=paging.manage_contact_us
        )
        self.render('manage_new/contact_us.html', **render_params)


class ContactUsDelHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        # 删除时传递参数：id、当前页码
        # 根据id从数据库删除条目
        # 删除条目后总页数可能回发生变化，为了保证前端依旧显示删除的页面，需讨论
        id_del = self.get_argument('id')
        page_current = self.get_argument('page_current', strip=True)
        result = ContactUsModel.delete_one_comment(id_del)
        if result == 1:  # 删除成功
            # 重新获得总页数
            current_total_page = ContactUsModel.get_comment_total_pages(items=paging.manage_contact_us)
            # 判断current_page与total_page关系
            if int(page_current) < current_total_page:
                self.write(str(page_current))
            else:
                self.write(str(current_total_page))
        else:
            self.write('false')


class ContactUsDetailHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        id_item = self.get_argument('id', strip=True)
        data_dict = ContactUsModel.get_one_comment(id_item)
        self.write(str(data_dict))