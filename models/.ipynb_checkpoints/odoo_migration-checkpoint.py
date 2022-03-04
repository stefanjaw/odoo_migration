# -*- coding: utf-8 -*-

from odoo import models, fields, api

import json
import random
import base64
from odoo.http import request
import requests

import uuid

import logging
_logging = logging.getLogger(__name__)

class OdooMigration(models.Model):
    _name = 'odoo_migration'
    _description = 'odoo_migration.odoo_migration'

    def _make_request(self, url, payload=False):
        ''' Make a request to proxy and handle the generic elements of the reponse (errors, new refresh token).'''
        TIMEOUT = 5
        
        try:
            response = requests.post(
                url,
                json=payload,
                timeout=TIMEOUT,
                headers={'content-type': 'application/json'},
            )
        except (ValueError, requests.exceptions.ConnectionError, requests.exceptions.MissingSchema, requests.exceptions.Timeout, requests.exceptions.HTTPError):
            msg = ('The url that this service requested returned an error. The url it tried to contact was %s', url)
            _logging.info("Error: %s", msg)
            return  msg

        if 'error' in response:
            message = _('The url that this service requested returned an error. The url it tried to contact was %s. %s', url, response['error']['message'])
            if response['error']['code'] == 404:
                message = _('The url that this service does not exist. The url it tried to contact was %s', url)
            return message
        _logging.info("  Response: %s", response)
        
        return response.json()['result']

    def b64decode(self, string):
        return base64.b64decode(string)
    
    def random_int(self):
        return random.randint(0, 1000000000)
    
    def json_str(self, string):
        return json.dumps(string)
    
    def get_loging_id(self, url, db, user, pwd):
        header = {'content-type': 'application/json'}

        payload1 = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "common",
                "method": "login",
                #'args': "[{0},{1},{2}]".format(db, user, pwd),
                "args": [db, user, pwd],
            },
            "id": random.randint(0, 1000000000),
        }
        _logging.info("DEF88 payload1: %s", payload1)
        data = json.dumps(payload1).encode().decode('utf-8')
        _logging.info("DEF90 ")
        response = requests.post(
            url,
            data = data,
            headers = header,
        )
        _logging.info("DEF98 response: %s",  response)
        _logging.info("DEF98 response: %s",  response.text )

        try:
            _logging.info("DEF100 response: %s", response.json() )
            
            return response.json()
        except:
            return False
    
    def get_records_id(self, url, db, login_id, pwd, model, search_filter):
        _logging.info("    DEF43")
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
        _logging.info("    DEF6")
        response = requests.post(
            url,
            data= json.dumps(payload1).encode().decode('utf-8'),
            headers = header,
        )
        _logging.info("    DEF69 response: %s", response)
        try:
            records_lst = response.json().get('result')
            _logging.info("    DEF71 records_lst: %s", records_lst)
            if len(records_lst) == 0:
                _logging.info("  NO RECORDS FOUND")
                return False
            return records_lst
        except:
            return False
        
    def export_data(self, url, db, login_id, pwd, model, ids, vars1):
        _logging.info("    DEF81")
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
                    'export_data',
                    ids,
                    vars1,
                ],
            },
            'id': random.randint(0, 1000000000),
        }
        _logging.info("    DEF102 payload1: %s", payload1)
        response = requests.post(
            url,
            data= json.dumps(payload1).encode().decode('utf-8'),
            headers = header,
        )
        _logging.info("    DEF108 response: %s", response)
        try:
            records_array = response.json().get('result')
            #{'datas': [['_....], ... ]
            _logging.info("    DEF111 records_id: %s", records_array)
            return records_array.get('datas')
        except:
            return False