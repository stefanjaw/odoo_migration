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
        if login_data == False:
            _logging.info("ERROR: Login")
            return

        login_id = login_data.get('result')
        
        #GET RECORDS ID
        _logging.info("  DEF25")
        search_filter = data.get('search_filter')
        if not search_filter:
            search_filter = []

        _logging.info("    DEF44")
        records_lst = OdooMigration.get_records_id(
            # url, db, login_id, pwd, model, search_filter
            self, url, data.get('db'), login_id, pwd,self._name, search_filter,
        )
        if records_lst == False:
            return
        _logging.info("  DEF57 records_lst: %s", records_lst)

        #GET RECORDS DATA
        _logging.info("  DEF56")
        remote_data_array = OdooMigration.export_data(
            #url, db, login_id, pwd, model, ids, vars1
            self, url, data.get('db'), login_id, pwd, self._name,
            records_lst, data.get('remote_vars'),
        )
        if remote_data_array == False:
            return
        #_logging.info("  66 remote_data_array: %s", remote_data_array)

        #Check Data if exists in THIS instance
        remote_vars = data.get('remote_vars')
        local_vars = data.get('local_vars')
        vars_len = len( remote_vars )
        _logging.info("    vars_len: %s", vars_len)

        _logging.info("72 INICIO DEL FOR remote_data_array=====")
        for remote_record_lst in remote_data_array:
            
            #Identifica el Remote External ID
            remote_record_id = remote_record_lst[0]
            
            #Obtiene el Local Record ID Objeto
            local_record_id = self.env.ref( remote_record_id )  # Es el Objeto Local
            _logging.info("    80 test: %s", local_record_id.get_external_id() )
            STOP81
            
            #Si no lo encuentra, se debe crear el registro
            if not local_record_id:
                STOP74_REGISTRO_NO_ENCONTRADO
                CREAR_UN_ARRAY_PARA_CREAR_REGISTRO_POSTERIORMENTE
                
            #recorre cada variable del registro y
            #hace match el dato local con data.get('remote_vars')
            _logging.info("84 INICIO DEL FOR=====")
            for index, value in enumerate( data.get('remote_vars') ):
                _logging.info("  86 Index: %s value: %s", index, value)
                remote_var = remote_vars[index]
                local_var = local_vars[index]
                if remote_var == "id":
                    _logging.info("  DEF_84 remote_var es ID, Continue")
                    continue
                remote_value = remote_record_lst[index]
                _logging.info("    88 remote_value: %s", remote_value)
                local_value = eval( "local_record_id.{0}".format( local_var ) )
                _logging.info("    90 local_value: %s", local_value)
                if remote_value == local_value:
                    continue
                else:
                    _logging.info("  DIFERENCIAS: REMOTE: %s LOCAL: %s",
                        remote_value, local_value)
                    STOP_SE_DEBE_ACTUALIZAR_EL_REGISTRO

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
