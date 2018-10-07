# -*- coding:utf-8 -*- 
# --------------------
# Author:       SDN
# Description:  公司基本信息设置
# Time:         2017/3/2
# --------------------

import tornado.web

from BaseHandler import BaseHandler
from module.generation.model import SelectorModel
from utils import TimeUtils
from ..model import BasicModel


class BasicHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, role):
        args = self.render_params
        args['navi_main'] = 'basic'
        args['navi_sub'] = ''
        args['title_page'] = '公司基本信息设置'
        args['title_content'] = ''
        args['role_page'] = ''
        args['role_admin'] = self.get_current_user_role()
        args['name_admin'] = self.get_current_user_name()
        if role == 'basic':
            args['navi_sub'] = 'basic-basic'
            args['title_content'] = '基本信息管理'
            self.render('manage_new/basic.html', **args)
        else:
            self.write('false')


class BasicEditHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, role):
        if role == 'basic':
            """
            不管更新是否成功，刷新当前页(只更新文字，logo单独)
            """
            info = dict(
                id=self.get_argument('id'),
                name_full=self.get_argument('name_full', strip=True),
                address=self.get_argument('address', strip=True),
                name_short=self.get_argument('name_short', strip=True),
                phone=self.get_argument('phone', strip=True),
                seo=self.get_argument('seo', strip=True),
                icp=self.get_argument('icp', strip=True),
                copyright=self.get_argument('copyright', strip=True),
                qq=self.get_argument('qq', strip=True),
                modified=TimeUtils.datetime_date_simple(),
            )
            # 将数据写入数据
            result = BasicModel.update_basic_info(**info)
            if result != -1:
                self.write('success')
            else:
                self.write('false')
        elif role == 'logo':
            """
            更新公司Logo
            """
            try:
                args = dict(
                    id=self.get_argument('id', strip=True),
                )
                # 更新图片
                result = BasicModel.change_selector(
                    file_save=self.request.files['photo'][0],  # 要保存的文件
                    table_file='file',  # 文件保存的表
                    category='logo',  # 文件分类
                    id_user=args['id'],  # 使用者 id
                    size_limit=100,
                    quality_limit=90,
                    width_limit=200,
                    height_limit=200,
                    width_thumb=200,
                    height_thumb=200,
                    compress_type=2
                )
                # 保存logo信息
                if len(result) > 1:
                    args['logo'] = result['path_file']
                    BasicModel.update_basic_info(**args)
                self.redirect('/basic/basic')
            except Exception as e:
                print __name__, 'change logo exception: no image file ', e
                self.redirect('/basic/basic')
        else:
            self.write('false')
