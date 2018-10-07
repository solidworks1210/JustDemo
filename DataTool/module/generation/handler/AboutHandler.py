# -*- coding:utf-8 -*- 
# --------------------
# Author:       SDN
# Description:	关于公司
# Time:         2017/3/7
# --------------------
import re
import tornado.web

from BaseHandler import BaseHandler
from module.generation.model import FWBModel
from utils import TimeUtils
from ..model import AboutModel


class AboutHandler(BaseHandler):
    """
    关于公司
    """

    @tornado.web.authenticated
    def get(self, role):
        try:
            args = self.render_params
            args['navi_main'] = 'about'
            args['navi_sub'] = ''
            args['title_page'] = '公司概况管理'
            args['title_content'] = ''
            args['role_page'] = ''
            args['role_admin'] = self.get_current_user_role()
            args['name_admin'] = self.get_current_user_name()
            if role == 'speech0':  # 总经理致辞
                args['navi_sub'] = 'about-speech'
                args['role_page'] = 'speech'
                args['title_content'] = '总经理致辞'
                result = AboutModel.get('speech')
                args['id'] = result['id']
                args['content'] = result['content']
            elif role == 'institution':  # 组织机构
                args['navi_sub'] = 'about-institution'
                args['role_page'] = 'institution'
                args['title_content'] = '组织机构'
                result = AboutModel.get('institution')
                args['id'] = result['id']
                args['content'] = result['content']
            elif role == 'qualification':  # 公司资质
                args['navi_sub'] = 'about-qualification'
                args['role_page'] = 'qualification'
                args['title_content'] = '公司资质'
                result = AboutModel.get('qualification')
                args['id'] = result['id']
                args['content'] = result['content']
            elif role == 'concept':  # 服务理念
                args['navi_sub'] = 'about-concept'
                args['role_page'] = 'concept'
                args['title_content'] = '服务理念'
                result = AboutModel.get('concept')
                args['id'] = result['id']
                args['content'] = result['content']
            elif role == 'business':  # 业务范围
                args['navi_sub'] = 'about-business'
                args['role_page'] = 'business'
                args['title_content'] = '业务范围'
                result = AboutModel.get('business')
                args['id'] = result['id']
                args['content'] = result['content']
            self.render('manage_new/about.html', **args)
        except Exception as e:
            print __name__, 'AboutHandler_get exception: ', e
            self.write('false')

    @tornado.web.authenticated
    def post(self, category):
        try:
            args = {
                'content': AboutModel.remove_image_height_attr(self.get_argument('content', strip=True)),
                'id': self.get_argument('id', strip=True),
                'category': category,
                'created': TimeUtils.datetime_date_simple(),
                'modified': TimeUtils.datetime_date_simple()
            }
            FWBModel.clean_fwb_content(
                id_user=args['id'],
                category=category,
                table_file='file',
                content_page=args['content'],
                create_thumb=False
            )
            result = AboutModel.save(**args)
            if result != -1:
                self.write('success')
            else:
                self.write('false')
        except Exception as e:
            print __name__, 'AboutHandler_post exception: ', e
            self.write('false')


class AboutDiscardHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, category):
        try:
            id_dis = self.get_argument('id')
            result = AboutModel.get(category)
            if len(result) > 0:
                FWBModel.clean_fwb_content_edit_discard(
                    id_user=id_dis,
                    table_file='file',
                    content=result['content']
                )

            self.write('success')
        except Exception as e:
            print __name__, 'AboutDiscardHandler_post exception: ', e
            self.write('false')
