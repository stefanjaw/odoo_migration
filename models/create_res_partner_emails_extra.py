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
    
    def create_res_partner_emails_extra(self, params={}):
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

        records_ints = self.get_records_id( remote_url, remote_db, login_id, remote_pwd, remote_model, remote_filter, offset, limit, order )
        total_records = len( records_ints )
        _logging.info(f"DEF50 total_records: {total_records}")
        remote_records_data = self.get_records_data( remote_url, remote_db, login_id, remote_pwd, remote_model, records_ints, remote_vars )
        #_logging.info(f"DEF50 remote_records_data: { remote_records_data }" )

        records_loaded = []
        _logging.info(f"DEF55 total_records: {total_records}")
        for a in range(0, round( total_records / limit ) + 1 ):
            offset = a * limit
            _logging.info(f"DEF55 a: {a} offset: {offset} limit: {limit}")
        STOP56


        for record in remote_records_data.get('datas'):
            #_logging.info(f"DEF53 record: {record}")
            try:
                local_record_ids = self.env.ref( record[0] )
            except:
                local_record_ids = []

            if len( local_record_ids ) == 1:
                local_record_data = local_record_ids[0].export_data( local_vars ) 
                if [ record ] == local_record_data.get('datas'):
                    continue
            _logging.info(f"DEF64 LOADING: { record }\n")
            remote_records_data = self.bool_to_string( [ record ] )
            output = self.load_records_data(local_model, local_vars, remote_records_data )
            records_loaded.append( output )
            _logging.info(f"DEF68 records_loaded result: { output }\n")
            _logging.info(f"DEF69 records_loaded result: { output.get('errors') }\n")
        _logging.info("END======== create_res_partner_emails_extra ")
        return records_loaded
