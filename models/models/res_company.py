# -*- coding: utf-8 -*-

from odoo import models, fields, api
from .odoo_migration import OdooMigration

import base64

import logging
_logging = logging.getLogger(__name__)

class ResCompanyInheritMigration(models.Model):
    _inherit = 'res.company'

    remote_url = fields.Char('Remote Server')
    remote_db = fields.Char('Remote Database')
    remote_user = fields.Char('Remote user')
    remote_pwd = fields.Char('Remote password')

