# -*- coding: utf-8 -*-

from odoo import models, fields, api

from .odoo_migration import OdooMigration

import logging
_logging = logging.getLogger(__name__)

class ResPartnerInheritMigration(models.Model):
    _inherit = 'res.partner'

    def migrate(self, data):
        _logging.info("DEF_12_migrate self: %s data: %s", self, data)
        OdooMigration.post_to_odoo(self, data)
        STOP10

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
