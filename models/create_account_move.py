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
        remote_line_vars = params.get('remote_line_vars') or []

        if remote_model == False:
            _logging.info(f"Error: Model Not Found\n================================")
            return False
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
        remote_move_ints = self.get_records_id( remote_url, remote_db, login_id, remote_pwd, remote_model, remote_filter, offset, limit, order )
        _logging.info(f"  DEF48 remote_move_ints: {remote_move_ints}")

        remote_move_header_data = self.get_records_data( remote_url, remote_db, login_id, remote_pwd, 'account.move', remote_move_ints, remote_vars ) 
        _logging.info(f"  DEF55 {remote_move_header_data}\n")

        xml_ids_to_create = set()
        for record in remote_move_header_data.get('datas'):
            _logging.info(f"DEF59 {record}\n")
            try:
                if self.env.ref( record[0] ):
                    _logging.info(f"  Ya Existe ID: { self.env.ref( record[0] ) } con External ID: {record[0]} ")
                    continue
            except:
                pass
            move_type_pos = remote_vars.index('move_type')
            if record[ move_type_pos ] == "Customer Invoice":
                record[ move_type_pos ] = "out_invoice"
            
            local_move_header_data = self.convert_external_id_to_local( remote_vars, record )
            header_data = local_move_header_data.get('record_array')
            account_move_json = self.convert_array_to_json(remote_vars,header_data)
            _logging.info(f"DEF68 { account_move_json }")
            line_ids_int = account_move_json.get('invoice_line_ids')
            account_move_json.pop( 'invoice_line_ids' )
            #move_type_pos = remote_vars.index('move_type')
            _logging.info(f"DEF69 account_move_json: {account_move_json:}")
            move_id = self.env['account.move'].sudo().create( account_move_json )
            _logging.info(f"DEF65 move_id: {move_id}"  )

            external_id_data = {
                    'name': record[0].split('.')[1],
                    'module': record[0].split('.')[0],
                    'model': remote_model,
                    'res_id': move_id.id
                }
            self.env['ir.model.data'].create( external_id_data )
            return
            STOP64
            xml_ids_to_create = local_move_header_data.get('xml_id_to_create')
            _logging.info(f"DEF60 \nheader_data: {header_data} xml_ids_to_create: {xml_ids_to_create}")
            lines_ids_pos = remote_vars.index('invoice_line_ids.id')
            _logging.info(f"DEF65 lines_ids_pos: {lines_ids_pos}")
            line_ints = record[lines_ids_pos]
            if type( line_ints ) == str: line_ints = [ int(line_ints) ]
            _logging.info(f"DEF68 {type(line_ints)}")
            _logging.info(f"DEF69 {line_ints}")
            remote_move_lines_data = self.get_records_data( remote_url, remote_db, login_id, remote_pwd, 'account.move.line', line_ints, remote_line_vars )
            _logging.info(f"DEF71 {remote_move_lines_data}")
            lines_dict = []
            for line_data in remote_move_lines_data.get('datas'):
                local_move_lines_data = self.convert_external_id_to_local( remote_line_vars, line_data )
                _logging.info(f"DEF73 {local_move_lines_data}")
                line_data = local_move_lines_data.get( 'record_array' )
                xml_ids_to_create.update( local_move_lines_data.get('xml_id_to_create') )
                line_json = self.convert_array_to_json(remote_line_vars, line_data)
                lines_dict.append( line_json   )
            _logging.info( f"DEF80 line_json: {lines_dict}"  )
            STOP81
            _logging.info(f"DEF81 remote_move_lines_data: {remote_move_lines_data}")
            _logging.info(f"DEF82 xml_ids_to_create: {xml_ids_to_create}")
            _logging.info(f"DEF83 len(xml_ids_to_create: {len(xml_ids_to_create)}")
            if len(xml_ids_to_create) > 0:
                move_id = self.env['account.move'].create({
                            'move_type': 'entry',
                            'ref': "Error External IDs para: " + record[0],
                        })
                _logging.info(f"  DEF89 move_id: {move_id}")
                move_id.button_cancel()

                activity_type_id = self.env.ref('mail.mail_activity_data_todo')
                summary = "Error: External IDs no encontrados para: " + record[0] 
                note = "<b>External IDs:</b><br>{0}<br>".format( xml_ids_to_create )
                move_id.activity_schedule(
                    '', None, summary, note,
                    **{ 'user_id': activity_type_id.default_user_id.id,
                        'activity_type_id': activity_type_id.id }
                )
        return

    def text_replace(self, text_in, text_out, record_array):
        for value in record_array:
            value.replace( text_in, text_out )
        return record_array

    def convert_external_id_to_local(self, vars_array, record_array):
        xml_id_to_create = set()
        for pos in range(1, len(vars_array)):
            if vars_array[pos][-3:] == "/id" and record_array[pos] != False:
                try:
                    record_array[pos] = self.env.ref( record_array[pos] ).id
                    vars_array[pos] = vars_array[pos][0:-3]
                except:
                    xml_id_to_create.add( record_array[pos] )
                    record_array[pos] = False
                    vars_array[pos] = vars_array[pos][0:-3]
            elif record_array[pos] == False:
                vars_array[pos] = vars_array[pos][0:-3]
            if vars_array[pos][-3:] == ".id":
                vars_array[pos] = vars_array[pos][0:-3]
        return {'record_array': record_array,
                'xml_id_to_create': xml_id_to_create,
               }

    def convert_array_to_json(self, vars_array, record_array):
        _logging.info(f"DEF120 {record_array}")
        output_json = {}
        for pos in range(0, len(vars_array)):
            _logging.info(f"DEF121 {vars_array[pos]}: {record_array[pos]}")
            output_json[vars_array[pos]] = record_array[pos]
            _logging.info(f"DEF123 output_json: {output_json}")

        return output_json
