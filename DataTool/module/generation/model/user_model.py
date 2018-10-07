# -*- coding:utf-8 -*- 
# --------------------
# Author:       SDN
# Description:
# Time:         2017/3/1
# --------------------
from module.generation.model.base_model import BaseModel
from utils import md5util


class UserModel(BaseModel):

    def get_user_list_with_super(self, page_current, items_per_page=10):
        """
    
        :param page_current:
        :param items_per_page:
        :return:
        """
        try:
            if page_current == 0:
                page_current = 1
            offset = items_per_page * (page_current - 1)
            total_page = self.get_user_total_page_with_super(items_per_page=items_per_page)
            list_dict = self.db.query("select * from user order by role asc, name asc limit %s offset %s",
                                      items_per_page, offset)
            return total_page, list_dict
        except Exception as e:
            print __name__, 'get_user_list_with_super exception: ', e
            return 0, []

    def get_user_total_page_with_super(self, items_per_page=10):
        try:
            all_items = self.db.row_count("select count(*) from user")
            if all_items % items_per_page != 0:
                page_total = all_items / items_per_page + 1
            else:
                page_total = all_items / items_per_page
            return page_total
        except Exception as e:
            print __name__, 'get_user_total_page_with_super exception: ', e
            return 0

    def get_user_list_without_super(self, page_current, items_per_page=10):
        """
    
        :param page_current:
        :param items_per_page:
        :return:
        """
        try:
            if page_current == 0:
                page_current = 1
            offset = items_per_page * (page_current - 1)
            total_page = self.get_user_total_page_without_super(items_per_page=items_per_page)
            list_dict = self.db.query(
                "select * from user where role!= '0' order by role asc, name asc limit %s offset %s",
                items_per_page, offset)
            return total_page, list_dict
        except Exception as e:
            print __name__, 'get_user_list_without_super exception: ', e
            return 0, []

    def get_user_total_page_without_super(self, items_per_page=10):
        try:
            all_items = self.db.row_count("select count(*) from user where role!='0'")
            if all_items % items_per_page != 0:
                page_total = all_items / items_per_page + 1
            else:
                page_total = all_items / items_per_page
            return page_total
        except Exception as e:
            print __name__, 'get_user_total_page_without_super exception: ', e
            return 0

    def get_all_name_with_super(self):
        """
        获得所有用户名
        :return:
        """
        list_dict = self.db.query("select name from user order by role asc, name asc")
        user_name = []
        for item in list_dict:
            user_name.append(item['name'])
        return user_name

    def get_all_name_without_super(self):
        """
        获得所有用户名
        :return:
        """
        list_dict = self.db.query("select name from user where role!='0' order by role asc, name asc")
        user_name = []
        for item in list_dict:
            user_name.append(item['name'])
        return user_name

    def add_user(self, **kwargs):
        try:
            result = self.db.insert('insert into user (name, password, role) values (%s, %s, %s)',
                                    *(kwargs['name'], kwargs['password'], kwargs['role']))
            self.db.commit()
            return result
        except Exception as e:
            print 'EmployeeModel:', e
            self.db.rollback()
            return -1

    def name_not_exist(self, name):
        """
        判断用户名是否已经存在
        :param name:
        :return:
        """
        try:
            result = self.db.query("select name from user where name=%s", name)
            if len(result) != 0:
                return False
            else:
                return True
        except Exception as e:
            print __name__, 'name_not_exist exception: ', e
            return True

    # 删除一个员工
    def delete_one_user(self, name):
        try:
            result = self.db.execute_rowcount("delete from user where name=%s", name)
            self.db.commit()
            return result
        except Exception as e:
            print 'EmployeeModel:', e
            self.db.rollback()
            return -1

    def get_password(self, name):
        """
        根据给定的用户名，获得其密码
        :param name:
        :return:
        """
        ps = self.db.get('select password from user where name=%s', name)
        return ps['password'].encode('utf-8')

    def modify_password(self, name, new_password):
        """
        修改密码
        :param name:    用户名
        :param new_password:    新密码
        :return: 删除失败 0、sql错误 -1， 成功其他
        """
        try:
            result = self.db.update('update user set password=%s  where name=%s',
                                    *(new_password, name))
            self.db.commit()
            return result
        except Exception as e:
            print 'EmployeeModel: ', e
            self.db.rollback()
            return -1

    def modify_role(self, name, role):
        try:
            result = self.db.update('update user set role=%s  where name=%s',
                                    *(role, name))
            self.db.commit()
            return result
        except Exception as e:
            print 'EmployeeModel:', e
            self.db.rollback()
            return -1

    def modify_role_password(self, name, role, new_password):
        try:
            result = self.db.update('update user set role=%s, password=%s  where name=%s',
                                    *(role, new_password, name))
            self.db.commit()
            return result
        except Exception as e:
            print 'EmployeeModel:', e
            self.db.rollback()
            return -1

    def verify(self, name, ps):
        try:
            data = self.db.query("select role from user where name=%s and password=%s", *(name, md5util.md5(ps)))
            if len(data) == 0:
                return '-1'
            else:
                role = data[0]['role']
                if role == '0' or role == '1':
                    return role
                else:
                    return '-1'
        except Exception as e:
            print __name__, 'verify exception: ', e
            return '-1'

    def is_user_table_empty(self):
        # 判断用户表是否为空
        try:
            countt = self.db.row_count('select count(*) from user ')
            if countt == 0:
                return True
            else:
                return False
        except Exception as e:
            print __name__, 'is_user_table_empty exception: ', e
            return False

    def create_super_admin(self, name, ps):
        # 创建用户
        try:
            result = self.db.insert('insert into user (name, password, role) values (%s, %s, %s)',
                                    *(name, md5util.md5(ps), '0'))
            self.db.commit()
            return result
        except Exception as e:
            print __name__, 'create_super_admin exception: ', e
            self.db.rollback()
            return -1


user_model = UserModel()
