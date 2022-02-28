# -*- coding: utf-8 -*-

from odoo import models, fields, api

from .odoo_migration import OdooMigration

import logging
_logging = logging.getLogger(__name__)

class ResPartnerInheritMigration(models.Model):
    _inherit = 'res.partner'

    def migrate(self, data):
        _logging.info("DEF_14 migrate")

        login_data = OdooMigration.get_loging_id(self,
            data.get('url'), data.get('db'), data.get('usr'), data.get('pwd'),
        )
        _logging.info("  login_data: %s", login_data)
        if login_data == False:
            _logging.info("ERROR: Login")

        login_id = login_data.get('result')

        _logging.info("  DEF25")
        search_filter = data.get('search_filter')
        if not search_filter:
            search_filter = []
        
        response = OdooMigration.get_records_id(
            # url, db, login_id, pwd, model, search_filter
            self, data.get('url'), data.get('db'), login_id, data.get('pwd'),\
            self._name, search_filter,
        )
        
        _logging.info("  get_records_id: %s", response)
        
        return
        
        
        
        

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
