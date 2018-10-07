# -*- coding:utf-8 -*-
# --------------------
# Author:       SDN
# Description:	员工管理
# --------------------


import tornado.web

from base_handler import BaseHandler
from config import paging
from config import config
from config.config import H_SECRETE_COOKIE
from module.generation.model.user_model import user_model
from utils import InputUtils
from utils import md5util


class LoginHandler(BaseHandler):
    def get(self):
        if self.get_current_user():  # 在其它窗口已经登陆了，就根据角色进入相应的界面
            self.redirect('/user')
        else:
            if user_model.is_user_table_empty():
                self.render('login.html', title_login='网站管理系统登录（设置超级管理员）')
            else:
                self.render('login.html', title_login='网站管理系统登录')

    def post(self):
        """
            前端采用 ajax 方式
        """
        name_login = self.get_argument('name_login', strip=True)
        ps_login = self.get_argument('ps_login', strip=True)
        if self.verify_input(name_input=name_login, ps_input=ps_login):
            # 如果用户表是空，这儿是创建超级用户
            if user_model.is_user_table_empty():
                result = user_model.create_super_admin(name_login, ps_login)
                if result == 1:
                    # 将角色保存到secure cookie中，get_current_user 得到 role
                    self.set_secure_cookie(config.H_SECRETE_COOKIE, name_login + '_' + '0',
                                           expires_days=None)  # 浏览器关闭，cookie失效
                    self.write('success')
                else:
                    self.write('false')
            else:
                role = user_model.verify(name_login, ps_login)
                if role == '0' or role == '1':
                    # 将角色保存到secure cookie中，get_current_user 得到 role
                    self.set_secure_cookie(config.H_SECRETE_COOKIE, name_login + '_' + role,
                                           expires_days=None)  # 浏览器关闭，cookie失效
                    self.write('success')
                else:  # 登陆失败
                    self.write('false')
        else:  # 登陆失败
            self.write('false')

    def verify_input(self, name_input, ps_input):
        """
        检查输入是否合法
        :param name_input:
        :param ps_input:    密码为六位
        :return:
        """
        if InputUtils.verify_name(name_input) and InputUtils.verify_ps(ps_input):
            return True
        else:
            return False


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie(H_SECRETE_COOKIE)  # 清除登陆cookie
        self.redirect('/login')


class UserHandler(BaseHandler):
    """
    1、超级管理员不能通过后台修改，只能在数据库中改
    2、超级管理员可以增删改查所有员工、普通管理员
    3、普通管理员只能增加员工，不能删除管理员
    """

    @tornado.web.authenticated
    def get(self):
        """
        显示超级管理员
        :return:
        """
        render_params = self.render_params
        render_params['page_current'] = self.get_int('page_current', 1)
        render_params['role_admin'] = self.get_current_user_role()
        render_params['name_admin'] = self.get_current_user_name()
        render_params['navi_main'] = 'user'
        render_params['navi_sub'] = 'user_sub'
        render_params['title_page'] = '员工管理'
        render_params['title_content'] = '员工管理'
        render_params['category'] = 'user'

        if render_params['role_admin'] == '0':
            render_params['page_total'], render_params['items'] = user_model.get_user_list_with_super(
                page_current=render_params['page_current'],
                items_per_page=paging.manage_user
            )
        else:
            render_params['page_total'], render_params['items'] = user_model.get_user_list_without_super(
                page_current=render_params['page_current'],
                items_per_page=paging.manage_user
            )
        self.render('user.html', **render_params)

    @tornado.web.authenticated
    def post(self):
        """
        添加员工:
        1、name 用户名（字母）
        2、pass 密码
        3、role 账户类型
        4、page 添加员工时，前端显示的页面（不需要，通过判断添加成功后员工在数据表中的位置，可以得到要显示的是第几页）
        :return:
        """
        name_add = self.get_argument('name_add', strip=True)
        ps_add = self.get_argument('ps_add', strip=True)
        role_add = self.get_argument('role_add', strip=True)
        # print __name__, 'name_add:', name_add, '/ ps_add:', ps_add, '/ role_add:', role_add
        if InputUtils.verify_name(name_add) and InputUtils.verify_ps(ps_add):  # 验证输入
            if user_model.name_not_exist(name_add):
                kwargs = dict(
                    name=name_add,
                    password=md5util.md5(ps_add.encode('utf-8')),
                )
                role_admin = self.get_current_user_role()
                if role_admin == '0':  # 当前用户为超级管理员
                    if role_add == 'admin':
                        kwargs['role'] = '1'  # 添加普通管理员
                    else:
                        kwargs['role'] = '2'  # 添加普通员工
                else:
                    kwargs['role'] = '2'  # 添加普通员工(普通管理员只能添加一般员工)
                result = user_model.add_user(**kwargs)
                if result == 1:  # 添加成功
                    # 添加成功后回到添加显示的页
                    if role_admin == '0':
                        name_all = user_model.get_all_name_with_super()
                    else:
                        name_all = user_model.get_all_name_without_super()
                    index_add = name_all.index(name_add) + 1
                    items = paging.manage_user
                    if index_add % items != 0:
                        page_temp = index_add / items + 1
                    else:
                        page_temp = index_add / items
                    self.write(str(page_temp))
                else:  # 数据库操作异常
                    self.write('false')
            else:  # 用户存在
                self.write('false')
        else:  # 输入不对
            self.write('false')

    @tornado.web.authenticated
    def put(self):
        """
        只能改密码，账户类型, 前端传来的参数：
        1、name_edit 用户名
        2、ps_new 新密码
        3、ps_old 旧密码
        4、role_edit 要修改的员工类型
        5、page 页面当前显示的页数（修改员工后要显示新员工所在页， 不需要）
        :return:
        """
        role_admin = self.get_current_user_role()  # 当前用户的角色
        name_edit = self.get_argument('name_edit', strip=True)
        ps_new = self.get_argument('ps_new', strip=True)
        ps_old = self.get_argument('ps_old', strip=True)
        role_user_old = self.get_argument('role_user_old', strip=True)
        role_user_new = self.get_argument('role_user_new', strip=True)

        result = 0
        if role_admin == '1':  # 普通管理员(要判断旧密码是否输入正确)
            # 判断新旧密码
            ps_old_db = user_model.get_password(name_edit)
            if ps_old_db == md5util.md5(ps_old):
                temp = user_model.modify_password(name=name_edit, new_password=md5util.md5(ps_new))
                if temp == -1:
                    result = -1
                else:
                    result = 1
            else:
                result = -1
        elif role_admin == '0':  # 超级管理员（不判断旧密码）
            if role_user_old == 'super':  # 超级管理员修改密码
                if InputUtils.verify_ps(ps_new):
                    temp = user_model.modify_role_password(
                        name=name_edit,
                        new_password=md5util.md5(ps_new),
                        role='0'
                    )
                    if temp == -1:
                        result = -1
                    else:
                        result = 1
            else:  # 超级管理员修改其他员工信息，或者一般管理员修改密码
                if role_user_new == 'admin':
                    role_code = '1'
                else:
                    role_code = '2'
                if ps_new == u'':  # 修改权限
                    temp = user_model.modify_role(
                        name=name_edit,
                        role=role_code
                    )
                    if temp == -1:
                        result = -1
                    else:
                        result = 1
                else:  # 修改密码及权限
                    if InputUtils.verify_ps(ps_new):  # 更改密码，权限
                        temp = user_model.modify_role_password(
                            name=name_edit,
                            new_password=md5util.md5(ps_new),
                            role=role_code
                        )
                        if temp == -1:
                            result = -1
                        else:
                            result = 1
                    else:
                        result = -1
        if result == 1:
            # 编辑成功后回到修改条目所在页显示的页（更改权限后，排序要改变）
            if role_admin == '0':
                name_all = user_model.get_all_name_with_super()
            else:
                name_all = user_model.get_all_name_without_super()
            index_add = name_all.index(name_edit) + 1
            items = paging.manage_user
            if index_add % items != 0:
                page_temp = index_add / items + 1
            else:
                page_temp = index_add / items
            self.write(str(page_temp))
        else:
            self.write('false')

    @tornado.web.authenticated
    def delete(self):
        """
            根据名字删除员工（登陆名是唯一的）：
            1、name 员工名
            2、page 当前显示的页数（删除后，前端回到删除时的页面）
            3、删除条目后总页数可能回发生变化，为了保证前端依旧显示删除的页面，需讨论
        """
        name_del = self.get_argument('name_del')
        page_current = self.get_int('page_current', 1)
        result = user_model.delete_one_user(name_del)
        role_admin = self.get_current_user_role()
        if result != -1:  # 删除成功
            # 重新获得总页数
            if role_admin == '0':
                current_total_page = user_model.get_user_total_page_with_super(
                    items_per_page=paging.manage_user
                )
            else:
                current_total_page = user_model.get_user_total_page_without_super(
                    items_per_page=paging.manage_user
                )
            # 判断current_page与total_page关系
            if page_current < current_total_page:
                self.write(str(page_current))
            else:
                self.write(str(current_total_page))
        else:
            self.write('false')


class UserHandler0(BaseHandler):
    """
    1、超级管理员不能通过后台修改，只能在数据库中改
    2、超级管理员可以增删改查所有员工、普通管理员
    3、普通管理员只能增加员工，不能删除管理员
    """

    @tornado.web.authenticated
    def get(self):
        """
        显示超级管理员
        :return:
        """
        render_params = self.render_params
        render_params['page_current'] = self.get_int('page_current', 1)
        render_params['role_admin'] = self.get_current_user_role()
        render_params['name_admin'] = self.get_current_user_name()
        render_params['navi_main'] = 'user'
        render_params['navi_sub'] = 'user_sub'
        render_params['title_page'] = '员工管理'
        render_params['title_content'] = '员工管理'
        render_params['category'] = 'user'

        if render_params['role_admin'] == '0':
            render_params['page_total'], render_params['items'] = user_model.get_user_list_with_super(
                page_current=render_params['page_current'],
                items_per_page=paging.manage_user
            )
        else:
            render_params['page_total'], render_params['items'] = user_model.get_user_list_without_super(
                page_current=render_params['page_current'],
                items_per_page=paging.manage_user
            )
        self.render('xxx.html', **render_params)

    @tornado.web.authenticated
    def post(self):
        """
        添加员工:
        1、name 用户名（字母）
        2、pass 密码
        3、role 账户类型
        4、page 添加员工时，前端显示的页面（不需要，通过判断添加成功后员工在数据表中的位置，可以得到要显示的是第几页）
        :return:
        """
        name_add = self.get_argument('name_add', strip=True)
        ps_add = self.get_argument('ps_add', strip=True)
        role_add = self.get_argument('role_add', strip=True)
        # print __name__, 'name_add:', name_add, '/ ps_add:', ps_add, '/ role_add:', role_add
        if InputUtils.verify_name(name_add) and InputUtils.verify_ps(ps_add):  # 验证输入
            if user_model.name_not_exist(name_add):
                kwargs = dict(
                    name=name_add,
                    password=md5util.md5(ps_add.encode('utf-8')),
                )
                role_admin = self.get_current_user_role()
                if role_admin == '0':  # 当前用户为超级管理员
                    if role_add == 'admin':
                        kwargs['role'] = '1'  # 添加普通管理员
                    else:
                        kwargs['role'] = '2'  # 添加普通员工
                else:
                    kwargs['role'] = '2'  # 添加普通员工(普通管理员只能添加一般员工)
                result = user_model.add_user(**kwargs)
                if result == 1:  # 添加成功
                    # 添加成功后回到添加显示的页
                    if role_admin == '0':
                        name_all = user_model.get_all_name_with_super()
                    else:
                        name_all = user_model.get_all_name_without_super()
                    index_add = name_all.index(name_add) + 1
                    items = paging.manage_user
                    if index_add % items != 0:
                        page_temp = index_add / items + 1
                    else:
                        page_temp = index_add / items
                    self.write(str(page_temp))
                else:  # 数据库操作异常
                    self.write('false')
            else:  # 用户存在
                self.write('false')
        else:  # 输入不对
            self.write('false')

    @tornado.web.authenticated
    def put(self):
        """
        只能改密码，账户类型, 前端传来的参数：
        1、name_edit 用户名
        2、ps_new 新密码
        3、ps_old 旧密码
        4、role_edit 要修改的员工类型
        5、page 页面当前显示的页数（修改员工后要显示新员工所在页， 不需要）
        :return:
        """
        role_admin = self.get_current_user_role()  # 当前用户的角色
        name_edit = self.get_argument('name_edit', strip=True)
        ps_new = self.get_argument('ps_new', strip=True)
        ps_old = self.get_argument('ps_old', strip=True)
        role_user_old = self.get_argument('role_user_old', strip=True)
        role_user_new = self.get_argument('role_user_new', strip=True)

        result = 0
        if role_admin == '1':  # 普通管理员(要判断旧密码是否输入正确)
            # 判断新旧密码
            ps_old_db = user_model.get_password(name_edit)
            if ps_old_db == md5util.md5(ps_old):
                temp = user_model.modify_password(name=name_edit, new_password=md5util.md5(ps_new))
                if temp == -1:
                    result = -1
                else:
                    result = 1
            else:
                result = -1
        elif role_admin == '0':  # 超级管理员（不判断旧密码）
            if role_user_old == 'super':  # 超级管理员修改密码
                if InputUtils.verify_ps(ps_new):
                    temp = user_model.modify_role_password(
                        name=name_edit,
                        new_password=md5util.md5(ps_new),
                        role='0'
                    )
                    if temp == -1:
                        result = -1
                    else:
                        result = 1
            else:  # 超级管理员修改其他员工信息，或者一般管理员修改密码
                if role_user_new == 'admin':
                    role_code = '1'
                else:
                    role_code = '2'
                if ps_new == u'':  # 修改权限
                    temp = user_model.modify_role(
                        name=name_edit,
                        role=role_code
                    )
                    if temp == -1:
                        result = -1
                    else:
                        result = 1
                else:  # 修改密码及权限
                    if InputUtils.verify_ps(ps_new):  # 更改密码，权限
                        temp = user_model.modify_role_password(
                            name=name_edit,
                            new_password=md5util.md5(ps_new),
                            role=role_code
                        )
                        if temp == -1:
                            result = -1
                        else:
                            result = 1
                    else:
                        result = -1
        if result == 1:
            # 编辑成功后回到修改条目所在页显示的页（更改权限后，排序要改变）
            if role_admin == '0':
                name_all = user_model.get_all_name_with_super()
            else:
                name_all = user_model.get_all_name_without_super()
            index_add = name_all.index(name_edit) + 1
            items = paging.manage_user
            if index_add % items != 0:
                page_temp = index_add / items + 1
            else:
                page_temp = index_add / items
            self.write(str(page_temp))
        else:
            self.write('false')

    @tornado.web.authenticated
    def delete(self):
        """
            根据名字删除员工（登陆名是唯一的）：
            1、name 员工名
            2、page 当前显示的页数（删除后，前端回到删除时的页面）
            3、删除条目后总页数可能回发生变化，为了保证前端依旧显示删除的页面，需讨论
        """
        name_del = self.get_argument('name_del')
        page_current = self.get_int('page_current', 1)
        result = user_model.delete_one_user(name_del)
        role_admin = self.get_current_user_role()
        if result != -1:  # 删除成功
            # 重新获得总页数
            if role_admin == '0':
                current_total_page = user_model.get_user_total_page_with_super(
                    items_per_page=paging.manage_user
                )
            else:
                current_total_page = user_model.get_user_total_page_without_super(
                    items_per_page=paging.manage_user
                )
            # 判断current_page与total_page关系
            if page_current < current_total_page:
                self.write(str(page_current))
            else:
                self.write(str(current_total_page))
        else:
            self.write('false')



