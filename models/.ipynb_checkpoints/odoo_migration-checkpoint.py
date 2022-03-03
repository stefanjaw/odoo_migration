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

    def _make_request(self, url, params=False):
        ''' Make a request to proxy and handle the generic elements of the reponse (errors, new refresh token).
        '''
        payload = {
            'jsonrpc': '2.0',
            'method': 'call',
            'params': params or {},
            'id': uuid.uuid4().hex,
        }

        try:
            response = requests.post(
                url,
                json=payload,
                timeout=TIMEOUT,
                headers={'content-type': 'application/json'},
            )
        except (ValueError, requests.exceptions.ConnectionError, requests.exceptions.MissingSchema, requests.exceptions.Timeout, requests.exceptions.HTTPError):
            msg = ('The url that this service requested returned an error. The url it tried to contact was %s', url)
            raise ValidationError( _( msg ) )

        if 'error' in response:
            message = _('The url that this service requested returned an error. The url it tried to contact was %s. %s', url, response['error']['message'])
            if response['error']['code'] == 404:
                message = _('The url that this service does not exist. The url it tried to contact was %s', url)
            raise AccountEdiProxyError('connection_error', message)

        proxy_error = response['result'].pop('proxy_error', False)
        if proxy_error:
            error_code = proxy_error['code']

        return response['result']

    
    
    
    
    def get_loging_id(self, url, db, user, pwd):
        STOP57
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