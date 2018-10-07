# -*- coding:utf-8 -*- 
# --------------------
# Author:       SDN
# Description:	私有信息管理
# Time:         2017/3/2
# --------------------

import tornado.web

from BaseHandler import BaseHandler
from module.generation.model import SelectorModel
from utils import StringUtils
from utils import TimeUtils


class SelectorHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, category):
        info_category = self.category.get(category, 'default')
        if info_category == 'default':
            self.redirect('/manage')
            return
        render_params = self.render_params
        render_params['role_admin'] = self.get_current_user_role()
        render_params['name_admin'] = self.get_current_user_name()
        render_params['page_current'] = self.get_int('page_current', 1)
        render_params['category'] = info_category['category']
        render_params['father_category'] = info_category['father_category']
        render_params['navi_main'] = info_category['father_category']
        render_params['title_page'] = info_category['title_page']
        render_params['title_navi1'] = info_category['title_navi1']
        render_params['url_navi1'] = info_category['url_navi1']
        render_params['navi_sub'] = info_category['navi_sub']
        render_params['title_content'] = info_category['title_content']
        render_params['title_navi2'] = info_category['title_navi2']
        render_params['url_navi2'] = info_category['url_navi2']
        render_params['dimension_limit'] = StringUtils.connect(
            "最佳图片尺寸：", info_category['width_limit'], "px*",
            info_category['height_limit'], 'px'
        )
        render_params['url_preview2'] = ''
        if category in ['bar', 'service']:
            render_params['url_preview'] = '/'
        elif category == 'certificate':
            render_params['url_preview'] = '/private/certificate'
            render_params['url_preview2'] = '/'
        else:
            render_params['url_preview'] = ''

        render_params['page_total'], render_params['items'] = SelectorModel.get_item_list(
            table=info_category['table_item'],
            category=info_category['category'],
            page_current=render_params['page_current'],
            items=info_category['items_per_page']
        )
        self.render('manage_new/selector.html', **self.render_params)


class SelectorMakeHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, category):
        info_category = self.category.get(category, 'default')
        if info_category == 'default':
            self.redirect('/manage')
            return
        # 共有
        page_current = self.get_argument('page_current', '1')
        args = dict(
            category=info_category['category'],
            title=self.get_argument('title', strip=True),
            summary=self.get_argument('summary', strip=True),
            sequence=self.get_int('sequence', 1),
            status=self.get_argument('status', strip=True),
            url=self.get_str_default('url', default='')
        )
        try:
            args['status'] = str(int(args['status']))
        except:
            args['status'] = '1'  # 默认显示

        # 私有
        action_type = self.get_argument('action_type')
        if action_type == 'add':
            args['id'] = TimeUtils.time_id()
            args['created'] = TimeUtils.datetime_date_full()
            args['modified'] = TimeUtils.datetime_date_full()
        elif action_type == 'edit':
            args['id'] = self.get_argument('id')
            args['modified'] = TimeUtils.datetime_date_full()
        else:
            self.write('false')
            return
        # 保存图片
        try:
            if action_type == 'add':
                result = SelectorModel.save_selector(
                    file_save=self.request.files['photo'][0],
                    table_file='file',
                    category=args['category'],
                    id_user=args['id'],
                    size_limit=info_category['size_limit'],
                    width_limit=info_category['width_limit'],
                    height_limit=info_category['height_limit'],
                    width_thumb=info_category['width_thumb'],
                    height_thumb=info_category['height_thumb'],
                    quality_limit=info_category['quality_limit'],
                    compress_type=info_category['compress_type']
                )
            else:
                result = SelectorModel.change_selector(
                    file_save=self.request.files['photo'][0],
                    table_file='file',
                    category=args['category'],
                    id_user=args['id'],
                    size_limit=info_category['size_limit'],
                    width_limit=info_category['width_limit'],
                    height_limit=info_category['height_limit'],
                    width_thumb=info_category['width_thumb'],
                    height_thumb=info_category['height_thumb'],
                    quality_limit=info_category['quality_limit'],
                    compress_type=info_category['compress_type']
                )
            if len(result) > 1:
                args['path_origin'] = result['path_origin']
                args['path_file'] = result['path_file']
                args['path_thumb'] = result['path_thumb']
        except Exception as e:
            print __name__, '添加服务图片保存异常: ', e
            if action_type == 'add':
                self.redirect(
                    StringUtils.connect('/selector/', info_category['category'], '?page_current=', page_current))
                return
        # 保存条目
        result = SelectorModel.insert_one_item(info_category['table_item'], **args)

        if result != -1:
            # 添加成功返回第一页
            if action_type == 'add':
                self.redirect(StringUtils.connect('/selector/', info_category['category']))
            # 编辑成功返回当前页
            else:
                self.redirect(StringUtils.connect('/selector/', info_category['category'], '?page_current=', page_current))
        else:
            # 操作失败返回当前页
            self.redirect(StringUtils.connect('/selector/', info_category['category']))


class SelectorDelHandler(BaseHandler):
    """
    删除
    """

    def post(self, category):
        info_category = self.category.get(category, 'default')
        if info_category == 'default':
            self.write('false')
            return
        id_del = self.get_argument('id_del', strip=True)
        current_page = self.get_int('page_current', 1)

        result = SelectorModel.delete_one_item_by_id(
            id_del=id_del,
            table_item=info_category['table_item'],
            table_file=info_category['table_file']
        )
        if result != -1:  # 删除成功
            # 重新获得总页数
            current_total_page = SelectorModel.total_pages(
                table=info_category['table_item'],
                category=info_category['category'],
                items=info_category['items_per_page']
            )
            # 判断current_page与total_page关系
            if current_page < current_total_page:
                self.write(str(current_page))
            else:
                self.write(str(current_total_page))
        else:
            self.write('false')
