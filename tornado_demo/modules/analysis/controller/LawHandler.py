# -*- coding:utf-8 -*- 


import tornado.concurrent
import tornado.gen

from ..model.LawModel import law_model
from ...common.controller.base import BaseHandler


# --------------------------------------------------------- 执法单位
class GetLawUnitHandler(BaseHandler):

    @tornado.gen.coroutine
    def get(self):
        data = yield self.get_data()
        if data:
            self.write(data)
        else:
            self.write({'type': 'law_unit', 'data': {}})

    @tornado.concurrent.run_on_executor(executor='thread_pool')
    def get_data(self):
        return law_model.get_law_unit_list()


# --------------------------------------------------------- 执法人员
class GetLawPeopleHandler(BaseHandler):

    @tornado.gen.coroutine
    def get(self):
        data = yield self.get_data()
        if data:
            self.write(data)
        else:
            self.write({'type': 'law_people', 'data': {}})

    @tornado.concurrent.run_on_executor(executor='thread_pool')
    def get_data(self):
        return law_model.get_law_people()


# --------------------------------------------------------- 执法车辆
class GetLawVehicleHandler(BaseHandler):

    @tornado.gen.coroutine
    def get(self):
        data = yield self.get_data()
        if data:
            self.write(data)
        else:
            self.write({'type': 'law_vehicle', 'data': {}})

    @tornado.concurrent.run_on_executor(executor='thread_pool')
    def get_data(self):
        return law_model.get_law_vehicle()
