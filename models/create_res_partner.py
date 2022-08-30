# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

import json
import random
import base64
from odoo.http import request
import requests

import uuid
import datetime  #For timestamp

import logging
_logging = logging.getLogger(__name__)

class OdooMigration(models.Model):
    _inherit = 'odoo_migration'

    def create_res_partner(self, params={}):
        _logging.info(f"DEF21 params: \n{params}")
        remote_filter = params.get('remote_filter') or []
        order = params.get('order') or False
        limit = int( params.get('limit') ) or 1000
        company_int = params.get('company_int') or 1
        max_records_to_load = params.get('max_records_to_load') or 100
        remote_vars = params.get('remote_vars') or []
        local_vars = params.get('local_vars') or []
        remote_model = params.get('remote_model') or False
        local_model = params.get('local_model') or False
        offset = params.get('offset') or 0

        if remote_model == False:
            _logging.info(f"Error: Model Not Found\n================================")
            return False

        company_id = self.env['res.company'].browse( company_int )

        remote_url = company_id.remote_url
        remote_db = company_id.remote_db
        remote_user = company_id.remote_user
        remote_pwd = company_id.remote_pwd

        login_id = self.get_login_id( remote_url, remote_db, remote_user, remote_pwd  )     #Remote Login ID
        if login_id == False:
            raise UserError ( "Login Incorrect" )
        _logging.info(f"  Login ID: {login_id}" )

        records_total = self.get_records_count(remote_url, remote_db, login_id, remote_pwd, remote_model, remote_filter)
        _logging.info(f"  records_total: {records_total}" )
        records_loaded = []
        for a in range(0, round( records_total / limit ) + 1 ):
            offset = a * limit
            _logging.info(f"    offset: {offset} limit: {limit}")

            records_ints = self.get_records_id( remote_url, remote_db, login_id, remote_pwd, remote_model, remote_filter, offset, limit, order )
            _logging.info(f"DEF57 records_ints: {records_ints}")

            remote_records_data = self.get_records_data( remote_url, remote_db, login_id, remote_pwd, remote_model, records_ints, remote_vars )
            #_logging.info(f"DEF60 remote_records_data: {remote_records_data}")

            for record in remote_records_data.get('datas'):
                try:
                    local_record_ids = self.env.ref( record[0] )
                except:
                    local_record_ids = []

                if len( local_record_ids ) == 1:
                    record = self.vars_value_replace( remote_vars, [record], 'parent_id/id', False, '' )[0]
                    record = self.vars_value_replace( remote_vars, [record], 'company_id/id', False, '' )[0]

                    local_record_data = local_record_ids[0].with_context( {'lang': 'en_US'}   ).export_data( local_vars )#.with_context( {'lang': 'en_US'}   )
                    #_logging.info(f"DEF75 COMPARANDO:==============\n\n{local_vars}\n\n{[record]}\n\n{local_record_data.get('datas')}\n")
                    if [ record ] == local_record_data.get('datas'):
                        #_logging.info(f"DEF72 IGUALES:==============")
                        continue
                    else:
                        _logging.info(f"DEF79 COMPARANDO:==============\n\n{local_vars}\n\n{[record]}\n\n{local_record_data.get('datas')}\n")
                
                #Cambiando variables
                record = self.vars_value_replace( remote_vars, [record], 'category_id/id', False, '' )[0]
                _logging.info(f"DEF82 record: {record}")

                remote_records_data = self.bool_to_string( [ record ] )
                _logging.info(f"DEF85 LOADING remote_records_data: {remote_records_data}")
                output = self.load_records_data(local_model, local_vars, remote_records_data )
                records_loaded.append( output )
                _logging.info(f"DEF88 LOADING RESULT: \n{ output }\n")

                if len(records_loaded) >= max_records_to_load:
                    _logging.info("END======== create_res_partner MAX RECORDS END ")
                    return
        _logging.info("END======== create_res_partner END ")
        return records_loaded

        STOP222
