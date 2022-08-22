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
    
    def create_account_move(self, params={}):
        move_ext_id = params.get('move_ext_id') or False
        remote_filter = params.get('remote_filter') or []
        order = params.get('order') or False
        limit = int( params.get('limit') ) or 1000
        company_int = params.get('company_int') or 1
        max_records_to_load = params.get('max_records_to_load') or 100
        remote_vars = params.get('remote_vars') or []
        local_vars = params.get('local_vars') or []
        remote_model = params.get('remote_model') or False
        offset = params.get('offset') or 0

        _logging.info(f"DEF21 params: {move_ext_id} {remote_filter} {order} {limit} {company_int}")

        company_id = self.env['res.company'].browse( company_int )

        remote_url = company_id.remote_url
        remote_db = company_id.remote_db
        remote_user = company_id.remote_user
        remote_pwd = company_id.remote_pwd

        login_id = self.get_login_id( remote_url, remote_db, remote_user, remote_pwd  )     #Remote Login ID
        if login_id == False:
            raise UserError ( "Login Incorrect" )
        _logging.info(f"  Login ID: {login_id}" )

        #Contar los registros para obtener el offset
        move_ints = self.get_records_id( remote_url, remote_db, login_id, remote_pwd, remote_model, remote_filter, offset, limit, order )
        _logging.info(f"  DEF48 move_ints: {move_ints}")


        STOP21
