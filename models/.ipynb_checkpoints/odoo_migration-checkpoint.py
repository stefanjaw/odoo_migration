# -*- coding: utf-8 -*-

from odoo import models, fields, api

import json
import random
import base64
from odoo.http import request
import requests

import logging
_logging = logging.getLogger(__name__)

class OdooMigration(models.Model):
    _name = 'odoo_migration'
    _description = 'odoo_migration.odoo_migration'

    def get_loging_id(self, url, db, user, pwd):
        try:
            pwd = base64.b64decode(pwd).decode('utf-8')
        except:
            _logging.info("  Error: Password format incorrect")
            return False
        
        try:
            url = url + "/jsonrpc"
        except:
            _logging.info("  Error: URL format incorrect")
            return False

        header = { 'Content-Type': 'application/json', }
        
        payload1 = {
            'jsonrpc': '2.0',
            'method': 'call',
            'params': {
                'service': 'common',
                'method': 'login',
                'args': [ db, user, pwd ],
            },
            'id': random.randint(0, 1000000000),
        }
        
        response = requests.post(
            url,
            data= json.dumps(payload1).encode().decode('utf-8'),
            headers = header,
        )
        try:
            response_json = response.json()
            return response_json
        except:
            return False
    
    def get_records_id(self, url, db, login_id, pwd, model, search_filter):
        try:
            pwd = base64.b64decode(pwd).decode('utf-8')
        except:
            _logging.info("  Error: Password format incorrect")
            return False
        
        try:
            url = url + "/jsonrpc"
        except:
            _logging.info("  Error: URL format incorrect")
            return False

        header = { 'Content-Type': 'application/json', }
        
        payload1 = {
            'jsonrpc': '2.0',
            'method': 'call',
            'params': {
                'service': 'object',
                'method': 'execute',
                'args': [
                    db,
                    login_id,
                    pwd,
                    model,
                    'search',
                    search_filter,
                ],
            },
            'id': random.randint(0, 1000000000),
        }
        
        _logging.info("    payload1: %s", payload1)
        
        response = requests.post(
            url,
            data= json.dumps(payload1).encode().decode('utf-8'),
            headers = header,
        )
        try:
            response_json = response.json()
            return response_json
        except:
            return False