# -*- coding: utf-8 -*-
# from odoo import http


# class OdooMigration(http.Controller):
#     @http.route('/odoo_migration/odoo_migration/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo_migration/odoo_migration/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo_migration.listing', {
#             'root': '/odoo_migration/odoo_migration',
#             'objects': http.request.env['odoo_migration.odoo_migration'].search([]),
#         })

#     @http.route('/odoo_migration/odoo_migration/objects/<model("odoo_migration.odoo_migration"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo_migration.object', {
#             'object': obj
#         })
