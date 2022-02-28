# -*- coding: utf-8 -*-

from odoo import models, fields, api

from .odoo_migration import OdooMigration

import base64

import logging
_logging = logging.getLogger(__name__)

class ResPartnerInheritMigration(models.Model):
    _inherit = 'res.partner'

    def migrate(self, data):
        _logging.info("DEF_14 migrate")

        try:
            pwd = base64.b64decode( data.get('pwd') ).decode('utf-8')
        except:
            _logging.info("  Error: Password format incorrect")
            return False
        
        try:
            url = data.get('url') + "/jsonrpc"
        except:
            _logging.info("  Error: URL format incorrect")
            return False
        
        #Login DATA
        login_data = OdooMigration.get_loging_id(self,
            url, data.get('db'), data.get('usr'), pwd,
        )
        _logging.info("  login_data: %s", login_data)
        if login_data == False:
            _logging.info("ERROR: Login")

        login_id = login_data.get('result')
        _logging.info("  login_id: %s", login_id)
        #GET RECORDS ID
        _logging.info("  DEF25")
        search_filter = data.get('search_filter')
        if not search_filter:
            search_filter = []
        
        response = OdooMigration.get_records_id(
            # url, db, login_id, pwd, model, search_filter
            self, url, data.get('db'), login_id, pwd,self._name, search_filter,
        )
        
        records_id = response.get('result')
        if len(records_id) == 0:
            _logging.info("  NO RECORDS FOUND")
            return
        _logging.info("  57records_id: %s", records_id)

        
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
