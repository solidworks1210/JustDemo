# -*- coding:utf-8 -*- 
# --------------------
# Author:       SDN
# Description:	公示管理
# Time:         2017/3/2
# --------------------
import re

import datetime
import tornado.web

from BaseHandler import BaseHandler
from module.generation.model import FWBModel
from utils import StringUtils
from utils import TimeUtils


class FWBHandler(BaseHandler):
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
        render_params['page_total'], render_params['items'] = FWBModel.get_item_list(
            table=info_category['table_item'],
            category=info_category['category'],
            page_current=render_params['page_current'],
            items=info_category['items_per_page']
        )
        if category in ['solution', 'standard']:
            render_params['url_preview'] = StringUtils.connect('/private/', category)
        elif category in ['news', 'work']:
            render_params['url_preview'] = StringUtils.connect('/news/', category)
        elif category in ['price', 'hire']:
            render_params['url_preview'] = StringUtils.connect('/publicity/', category)
        elif category in 'case':
            render_params['url_preview'] = '/case'
        else:
            render_params['url_preview'] = ''
        self.render('manage_new/fwb.html', **self.render_params)


class FWBMakeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, category):
        def get_simple_date(old_date):
            try:
                if old_date:
                    return old_date.split(' ')[0]
                else:
                    return str(datetime.datetime.now().strftime('%Y-%m-%d'))
            except:
                return str(datetime.datetime.now().strftime('%Y-%m-%d'))
        info_category = self.category.get(category, 'default')
        if info_category == 'default':
            self.redirect('/manage')
            return
        render_params = self.render_params
        render_params['role_admin'] = self.get_current_user_role()
        render_params['name_admin'] = self.get_current_user_name()
        render_params['page_current'] = self.get_argument('page_current', '1')
        render_params['category'] = info_category['category']
        render_params['father_category'] = info_category['father_category']
        render_params['navi_main'] = info_category['father_category']
        render_params['navi_sub'] = info_category['navi_sub']
        render_params['title_page'] = info_category['title_page']
        render_params['title_navi1'] = info_category['title_navi1']
        render_params['url_navi1'] = info_category['url_navi1']

        action_type = self.get_argument('action_type')
        # 添加
        if action_type == 'add':
            render_params['action_type'] = 'add'
            render_params['title_content'] = info_category['title_content_add']
            render_params['title_navi2'] = info_category['title_navi2_add']
            render_params['url_navi2'] = info_category['url_navi2_add']
            render_params['item'] = {'id': TimeUtils.time_id(), }
        # 编辑
        else:
            render_params['action_type'] = 'edit'
            render_params['title_content'] = info_category['title_content_edit']
            render_params['title_navi2'] = info_category['title_navi2_edit']
            render_params['url_navi2'] = info_category['url_navi2_edit']
            id_item = self.get_argument('id')
            item = FWBModel.get_one_item_by_id(id_item=id_item, table_item='item')
            if len(item) > 0:
                item['m_modified'] = get_simple_date(item['modified'])
                render_params['item'] = item
            else:
                render_params['item'] = {'id': TimeUtils.time_id(), }

        self.render('manage_new/fwb_maker.html', **self.render_params)

    @tornado.web.authenticated
    def post(self, category):
        info_category = self.category.get(category, 'default')
        if info_category == 'default':
            self.redirect('/manage')
            return
        args = {
            'id': self.get_argument('id'),
            'title': self.get_argument('title'),
            'summary': self.get_argument('summary'),
            'content': FWBModel.remove_image_height_attr(self.get_argument('content', strip=True)),
            'category': info_category['category'],
            'attachment_list': self.get_argument('attachment_list')
        }
        action_type = self.get_argument('action_type')
        # 清理附件
        FWBModel.clean_attachment(
            attachment_new=args['attachment_list'],  # 字符串化的 list
            table_file=info_category['table_file'],
            id_user=args['id']
        )
        # 清理符文本内容
        args['path_thumb'] = FWBModel.clean_fwb_content(
            id_user=args['id'],
            category=info_category['category'],
            table_file='file',
            content_page=args['content'],
            create_thumb=True,      # 编辑时删除文件会删附件，因此要生成缩略图
            thumb_with=info_category['thumb_width'],
            thumb_height=info_category['thumb_height']
        )

        customer_time = self.get_argument('customer_time', None)
        if customer_time:
            temp_time = TimeUtils.datetime_date_full()
            time_detail = temp_time.split(' ')[1]
            time_time = StringUtils.connect(customer_time, ' ', time_detail)
            print time_time
        else:
            time_time = TimeUtils.datetime_date_full()

        if action_type == 'add':
            args['created'] = TimeUtils.datetime_date_full()
            args['modified'] = time_time
        else:
            args['modified'] = time_time

        result = FWBModel.insert_one_item(info_category['table_item'], **args)
        if result != -1:
            self.write('success')
        else:
            self.write('false')


class FWBDiscardHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, category):
        info_category = self.category.get(category, 'default')
        if info_category == 'default':
            self.redirect('/manage')
            return
        id_discard = self.get_argument('id_discard')
        current_page = self.get_int('page_current', 1)
        action_type = self.get_argument('action_type')
        if action_type == 'del':
            result = FWBModel.delete_one_item_by_item_id(
                id_discard,
                table_item=info_category['table_item'],
                table_file=info_category['table_file'],
            )
            if result == 1:  # 删除成功
                current_total_page = FWBModel.total_pages(
                    table=info_category['table_item'],
                    category=info_category['category'],
                    items=info_category['items_per_page'])
                # 判断current_page与total_page关系
                if current_page < current_total_page:
                    self.write(str(current_page))
                else:
                    self.write(str(current_total_page))
            else:
                self.write('false')
        elif action_type == 'add':
            FWBModel.clean_fwb_content_add_discard(id_user=id_discard, table_file=info_category['table_file'])
            self.write(str(current_page))
        elif action_type == 'edit':
            item = FWBModel.get_one_item_by_id(id_item=id_discard, table_item=info_category['table_item'])
            if len(item) > 0:
                # 清理附件
                FWBModel.clean_attachment(
                    attachment_new=item['attachment_list'],
                    table_file=info_category['table_file'],
                    id_user=id_discard
                )
                # 清理富文本内容
                FWBModel.clean_fwb_content_edit_discard(
                    id_user=id_discard,
                    table_file=info_category['table_file'],
                    content=item['content'],
                )
            self.write(str(current_page))
