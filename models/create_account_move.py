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
        lines_int_array = self.get_line_ints_array( 'invoice_line_ids.id', remote_vars, remote_move_header_data.get('datas')  )
        _logging.info(f"  DEF55 {lines_int_array}\n")

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
            
            account_move_json = self.convert_array_to_json(remote_vars, record)
            _logging.info(f"DEF71 { account_move_json }")
            account_move_temp = self.convert_external_id_to_local( remote_vars, account_move_json)
            _logging.info(f"DEF73 { account_move_temp }")
            account_move_json = account_move_temp.get('record_json')
            xml_ids_to_create = account_move_temp.get('not_found')
            _logging.info(f"DEF76 { json.dumps(account_move_json, indent=4) } \n\n{xml_ids_to_create}")
            remote_invoice_line_data = self.get_records_data(
                    remote_url, remote_db, login_id, remote_pwd,
                    'account.move.line',
                    lines_int_array,
                    remote_line_vars )
            _logging.info(f"DEF85 {remote_invoice_line_data} ")

            STOP74
            #Create External ID account_move
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

    def convert_external_id_to_local(self, vars_array, record_json):
        not_found = set()
        new_json = {}
        for var_name in record_json:
            if var_name[-3:] == "/id" and record_json[var_name] != False:
                try:
                    new_json[ var_name[:-3] ] = self.env.ref( record_json[var_name] ).id
                except:
                    not_found.add( record_json[var_name] )
                    new_json[ var_name[:-3] ] = False
            elif var_name[-3:] == "/id" == False:
                new_json[ var_name[-3:] ] = record_json[var_name]
            else:
                new_json[ var_name ] = record_json[var_name]

        return {'record_json': new_json,
                'not_found': not_found,
               }

    def convert_array_to_json(self, vars_array, record_array):
        _logging.info(f"DEF120 {record_array}")
        output_json = {}
        for pos in range(0, len(vars_array)):
            _logging.info(f"DEF121 {vars_array[pos]}: {record_array[pos]}")
            output_json[vars_array[pos]] = record_array[pos]
            _logging.info(f"DEF123 output_json: {output_json}")

        return output_json

    def get_line_ints_array( self, var_name ,vars_array, records_array ):
        var_pos = vars_array.index( var_name )

        new_array = []
        for record in records_array:
            new_array.append( int( record[var_pos] )  )
        return new_array
