# -*- coding: utf-8 -*-

from odoo import models, fields, api

import json
import random
import base64
from odoo.http import request

class OdooMigration(models.Model):
    _name = 'odoo_migration'
    _description = 'odoo_migration.odoo_migration'

    def post_to_odoo(self, algo):
        method = "call"
        service = "xxxx"
        params_method = "xxxx"
        params_args = "xxxxx"
        payload1 = {
            "jsonrpc": "2.0",
            "method": method,
            "params": {
                "service": service,
                "method": params_method,
                "args": params_args,
            },
            "id": random.randint(0, 1000000000),
          }
        data = {
            method: 'POST',
            contentType: 'application/json',
            payload: json.dumps(payload1),
        }

''' Ejemplo de referencia
    data = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": random.randint(0, 1000000000),
    }
    req = urllib.request.Request(url=url, data=json.dumps(data).encode(), headers={
        "Content-Type":"application/json",
    })
    reply = json.loads(urllib.request.urlopen(req).read().decode('UTF-8'))
'''
        
    
#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
