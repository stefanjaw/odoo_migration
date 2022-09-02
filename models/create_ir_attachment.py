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

    def create_ir_attachment(self, params={}):
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
        res_model = params.get('res_model') or False

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
            _logging.info(f"DEF60 remote_records_data: {str(remote_records_data)[:500] }")

            #OBTNER TODOS LOS REMOTE_RES_ID
            remote_res_id_int_lst = []
            res_id_pos = remote_vars.index( 'res_id' )
            for record in remote_records_data.get('datas'):
                remote_res_id_int_lst.append( record[ res_id_pos ] )

            #BUSCAR EL EXTERNAL_ID DE CADA REMOTE_RES_ID Y COLOCARLOS EN UNA VARIABLE
            remote_vars_external_id = [ 'model', 'complete_name', 'res_id' ]
            res_id_pos_external_id = remote_vars_external_id.index( 'res_id'  )
            remote_external_id_pos = remote_vars_external_id.index( 'complete_name'  )

            remote_filter_external_id = [ ['res_id', 'in',  remote_res_id_int_lst  ], [ 'model', '=', res_model ]  ]
            offset_external = 0
            limit_external = False
            order_external = "id asc"

            remote_res_id_ints = self.get_records_id(
                    remote_url, remote_db, login_id, remote_pwd, 'ir.model.data', remote_filter_external_id, offset_external, limit_external, order_external )
            #_logging.info(f"DEF77 { remote_res_id_ints }")

            external_ids_data = self.get_records_data( remote_url, remote_db, login_id, remote_pwd, 'ir.model.data', remote_res_id_ints, remote_vars_external_id )
            _logging.info(f"DEF80 { external_ids_data }")

            to_load = []
            for record in remote_records_data.get('datas'):

                records_data = self.bool_to_string( [ record ] )
                _logging.info(f"DEF85 LOADING records_data: \n{str(records_data)[0:300]}")

                #CAMBIAR DE REMOTE_RES_ID A EXTERNAL ID
                remote_res_id = record[ res_id_pos ]
                _logging.info(f"DEF92 {remote_res_id}")

                remote_external_id_data = [ x for x in external_ids_data.get('datas') if x[ res_id_pos_external_id ] == remote_res_id ]
                remote_external_id = remote_external_id_data[0][remote_external_id_pos]
                _logging.info(f"DEF98 { remote_external_id }")
                local_res_id = self.env.ref( remote_external_id )
                _logging.info(f"DEF100 { local_res_id }")
                record[ res_id_pos ] = local_res_id.id 

                to_load.append( record )
                _logging.info(f"DEF104 {str(to_load)[:300]}")
                #CAMBIAR DE EXTERNAL_ID A LOCAL_RES_ID

            logging.info(f"DEF106 LOADING: \n{str(to_load)[0:300]}")
            output = self.load_records_data(local_model, local_vars, to_load )
            records_loaded.append( output )
            _logging.info(f"DEF88 LOADING RESULT: \n{ output }\n")

            if len(records_loaded) >= max_records_to_load:
                _logging.info("END======== create_res_partner MAX RECORDS END ")
                return
        _logging.info("END======== create_res_partner END ")
        return records_loaded
