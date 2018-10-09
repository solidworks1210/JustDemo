# -*- coding:utf-8 -*-

from modules.common.model.BaseModel import BaseModel


class CollectionCompanyManagerModel(BaseModel):
    '''CollectionCompanyManagerModel'''

    def get_by_keyword(self, keyword, page_to_show, item_per_page):
        '''get_table'''

        # 偏移
        if page_to_show > 0:
            offset = (page_to_show - 1) * item_per_page
        else:
            offset = 0

        # 分页计算
        total_item_query = self.server.query(
            "SELECT count(*) as count FROM esp_proprietor "
            "WHERE esp_proprietor.name LIKE %s ", '%' + keyword + '%')
        if total_item_query:
            total_item = total_item_query[0]['count']
        else:
            total_item = 0

        if total_item % item_per_page != 0:
            page_total = total_item / item_per_page + 1
        else:
            page_total = total_item / item_per_page

        # 内容
        data_list = self.server.query(
            "SELECT * FROM esp_proprietor "
            "WHERE esp_proprietor.name LIKE %s "
            "ORDER BY esp_proprietor.id ASC "
            "limit %s offset %s", '%' + keyword + '%', item_per_page, offset)

        return {
            'item_per_page': item_per_page,
            'item_total': total_item,
            'page_total': page_total,
            'page_current': page_to_show if page_to_show > 0 else 1,
            'data': data_list
        }

    def choose_by_keyword(self, keyword, page_to_show, item_per_page):
        '''get_table'''

        # 偏移
        if page_to_show > 0:
            offset = (page_to_show - 1) * item_per_page
        else:
            offset = 0

        # 分页计算
        total_item_query = self.server.query(
            "SELECT count(*) as count FROM et_proprietor "
            "INNER JOIN et_economictype ON et_proprietor.economictypeid=et_economictype.id AND et_economictype.id!=23 AND et_economictype.id!=12 "
            "LEFT JOIN esp_proprietor ON et_proprietor.id=esp_proprietor.proprietor_id "
            "WHERE et_proprietor.proprietorname LIKE %s ", '%' + keyword + '%')
        if total_item_query:
            total_item = total_item_query[0]['count']
        else:
            total_item = 0

        if total_item % item_per_page != 0:
            page_total = total_item / item_per_page + 1
        else:
            page_total = total_item / item_per_page

        # 内容
        data_list = self.server.query(
            "SELECT et_proprietor.id as proprietor_id,et_proprietor.proprietorname as name,et_proprietor.address, "
            "et_proprietor.linkman as contact_name,et_proprietor.linkphone as contact_tel,et_economictype.economictype, "
            "COALESCE (esp_proprietor.id, 0) AS company_id "
            "FROM et_proprietor "
            "INNER JOIN et_economictype ON et_proprietor.economictypeid=et_economictype.id AND et_economictype.id!=23 AND et_economictype.id!=12 "
            "LEFT JOIN esp_proprietor ON et_proprietor.id=esp_proprietor.proprietor_id "
            "WHERE et_proprietor.proprietorname LIKE %s "
            "ORDER BY et_proprietor.id ASC "
            "limit %s offset %s", '%' + keyword + '%', item_per_page, offset)

        return {
            'item_per_page': item_per_page,
            'item_total': total_item,
            'page_total': page_total,
            'page_current': page_to_show if page_to_show > 0 else 1,
            'data': data_list
        }

    def add_company(self, params):
        '''添加'''
        try:
            result = self.server.execute_rowcount(
                "INSERT INTO esp_proprietor(username,password,name,address,contact_name,contact_tel,type_id,proprietor_id,status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                params["username"], params["password"], params["name"],
                params["address"], params["contact_name"],
                params["contact_tel"], params["type_id"],
                params["proprietor_id"], params["status"])
            self.server.commit()
            return result
        except Exception as e:
            self.server.rollback()
            return None

    def update_by_company_id(self, params):
        '''更新'''
        try:
            result = self.server.update(
                "UPDATE esp_proprietor SET "
                "username=%s, "
                "password=%s, "
                "name=%s, "
                "address=%s, "
                "contact_name=%s, "
                "contact_tel=%s, "
                "type_id=%s, "
                "proprietor_id=%s, "
                "status=%s "
                "WHERE id=%s ", params["username"], params["password"],
                params["name"], params["address"], params["contact_name"],
                params["contact_tel"], params["type_id"],
                params["proprietor_id"], params["status"], params["id"])
            self.server.commit()
            return result
        except Exception as e:
            self.server.rollback()
            return None

    def delete_by_company_id(self, company_id):
        '''删除'''
        try:
            result = self.server.execute_rowcount(
                "DELETE FROM esp_proprietor WHERE id=%s ", company_id)
            self.server.commit()
            return result
        except Exception as e:
            self.server.rollback()
            return None

    def get_by_company_id(self, company_id):
        '''查看'''
        try:
            result = self.server.get(
                "SELECT * FROM esp_proprietor WHERE id=%s ", company_id)
            return result
        except Exception as e:
            return None

    def get_by_proprietor_id(self, proprietor_id):
        '''是否存在'''
        try:
            result = self.server.get(
                "SELECT * FROM esp_proprietor WHERE id=%s", proprietor_id)
            return result
        except Exception as e:
            return None


collection_company_manager_model = CollectionCompanyManagerModel()
