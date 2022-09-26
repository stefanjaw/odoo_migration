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

    
    def create_account_move(self, params={}):   # 1663729248
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
        _logging.info(f"===INICIO=== DEF21 params:  \n move_ext_id: {move_ext_id}\n remote_filter: {remote_filter} \
                                                    \n order: {order}\n limit: {limit}\n company_int: {company_int}\n\n")

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
        _logging.info(f"  DEF55 \nvars: {remote_vars} \nremote_move_header_data: {remote_move_header_data}\n\n")

        list_var = 'invoice_line_ids/id'
        remote_account_move_json_list = self.data_array_to_data_json( list_var, remote_vars, remote_move_header_data.get('datas') )
        _logging.info(f"  DEF59 \nremote_account_move_json_list: {remote_account_move_json_list}\n\n")
        for record in remote_account_move_json_list:  # 1663729248_10
            _logging.info(f"DEF62 Record : {record}\n")
            xml_ids_to_create = set()
            try:
                if self.env.ref( record['id'] ):
                    _logging.info(f"  Ya Existe ID: { self.env.ref( record[0] ) } con External ID: {record[0]} ")
                    continue
            except:
                pass

            if record[ 'move_type' ] == "Customer Invoice":
                record[ 'move_type' ] = "out_invoice"
            
            account_move_temp = self.convert_external_id_to_local( remote_vars, record )
            _logging.info(f"DEF73 { account_move_temp }")
            STOP77
            account_move_json = account_move_temp.get('record_json')
            xml_ids_to_create.update( account_move_temp.get('not_found') )
            _logging.info(f"DEF76 { json.dumps(account_move_json, indent=4) } \n xml_ids_to_create: {xml_ids_to_create}\n\n")
            line_ids = account_move_json.get('invoice_line_ids.id')

            _logging.info(f"DEF80 before line_ids {line_ids}")
            if line_ids in [ [False], []  ]:
                lines_data = []
                pass
            else:
                for x in range(0,len(line_ids)): line_ids[x] = int( line_ids[x] )
                _logging.info(f"DEF86 {line_ids}")

                lines_data = self.get_records_data(
                    remote_url, remote_db, login_id, remote_pwd,
                    'account.move.line',
                    line_ids,
                    remote_line_vars )

            _logging.info(f"DEF94 {lines_data}\n\n")
            if len( lines_data ) > 0:
                lines_json = self.data_array_to_data_json( 'no_variable_defined_yet', remote_line_vars, lines_data.get('datas') )
            else: lines_json = [] 
            _logging.info(f"DEF99 {lines_json} ")
           
            invoice_line_ids_json = []
            for line_json in lines_json:
                #_logging.info(f"DEF102 line_json: {line_json}")
                line_temp  = self.convert_external_id_to_local( remote_line_vars, line_json )
                #_logging.info(f"DEF104 line_json: {line_temp}")
                line_json = line_temp.get('record_json')
                #_logging.info(f"DEF106 line_json: {line_json} xml_to_create: { len( line_temp.get('not_found')) }")
                if len( line_temp.get('not_found') ) >0:
                    xml_ids_to_create.update( line_temp.get('not_found') )
                #_logging.info(f"DEF111 xml_ids_to_create: {xml_ids_to_create}")
                #continue 

            account_move_json[ 'invoice_line_ids' ] = lines_json
            _logging.info(f"DEF113 { json.dumps(account_move_json, indent=4) } \n\n{xml_ids_to_create}")
            continue

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
            _logging.info(f"DEF124 \nheader_data: {header_data} xml_ids_to_create: {xml_ids_to_create}")
            lines_ids_pos = remote_vars.index('invoice_line_ids.id')
            _logging.info(f"DEF126 lines_ids_pos: {lines_ids_pos}")
            line_ints = record[lines_ids_pos]
            if type( line_ints ) == str: line_ints = [ int(line_ints) ]
            _logging.info(f"DEF129 {type(line_ints)}")
            _logging.info(f"DEF130 {line_ints}")
            remote_move_lines_data = self.get_records_data( remote_url, remote_db, login_id, remote_pwd, 'account.move.line', line_ints, remote_line_vars )
            _logging.info(f"DEF132 {remote_move_lines_data}")
            lines_dict = []
            for line_data in remote_move_lines_data.get('datas'):
                local_move_lines_data = self.convert_external_id_to_local( remote_line_vars, line_data )
                _logging.info(f"DEF136 {local_move_lines_data}")
                line_data = local_move_lines_data.get( 'record_array' )
                xml_ids_to_create.update( local_move_lines_data.get('xml_id_to_create') )
                line_json = self.convert_array_to_json(remote_line_vars, line_data)
                lines_dict.append( line_json   )
            _logging.info( f"DEF141 line_json: {lines_dict}"  )
            STOP81
            _logging.info(f"DEF143 remote_move_lines_data: {remote_move_lines_data}")
            _logging.info(f"DEF144 xml_ids_to_create: {xml_ids_to_create}")
            _logging.info(f"DEF145 len(xml_ids_to_create: {len(xml_ids_to_create)}")
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
            _logging.info(f"DEF166 xml_ids_to_create: {xml_ids_to_create}")
        return

    def text_replace(self, text_in, text_out, record_array):
        for value in record_array:
            value.replace( text_in, text_out )
        return record_array

    def convert_external_id_to_local(self, vars_array, record_json): # 1661214870 1663729574
        not_found = [] #set()
        new_json = {}
        for var_name in record_json:
            #_logging.info(f"DEF181 var_name: {var_name} => {record_json[var_name]} {type( record_json[var_name] )}")
            if var_name == "invoice_line_ids/id":
                #_logging.info(f"DEF183====")
                new_json[ var_name ] = record_json[var_name]
            elif var_name[-3:] == "/id" and record_json[var_name] != False:
                #_logging.info(f"DEF186====")
                try:
                    new_json[ var_name[:-3] ] = self.env.ref( record_json[var_name] ).id
                except:
                    #_logging.info(f"DEF190 passsss")
                    not_found.add( record_json[var_name] )
                    new_json[ var_name[:-3] ] = False
            elif var_name[-3:] == "/id" and record_json[var_name] ==  False:
                #_logging.info(f"DEF195 =====")
                new_json[ var_name[:-3] ] = record_json[var_name]
            else:
                #_logging.info(f"DEF198 =======")
                new_json[ var_name ] = record_json[var_name]
        
        #_logging.info(f"DEF201 new_json: {new_json} not_found: {not_found}")
        return {'record_json': new_json,
                'not_found': not_found,
               }

    def convert_array_to_json(self, vars_array, record_array):
        STOP163
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

    def data_array_to_data_json( self, list_var, vars_array, data_array ): #1661306266
        try:
            list_var_pos = vars_array.index( list_var )
        except:
            list_var_pos = 100000
        output_array = []
        
        for record_pos in range(0, len(data_array) ):   #1661306266_a
        
            if data_array[record_pos][0] != '':
                new_json = {}
                sub_list = []
                create_json = True
            else:
                create_json = False
                
            for var_pos in range(0, len(vars_array) ):  #1661306266_b
                if var_pos == list_var_pos:             #1661306266_b1
                    sub_list.append( data_array[record_pos][var_pos] )
                    value = sub_list
                elif create_json == True:               #1661306266_b2
                    value = data_array[record_pos][var_pos]            
                elif create_json == False:              #1661306266_b3
                    continue
                else:                                   #1661306266_b4
                    continue
                
                new_json[ vars_array[var_pos] ] = value
            
            try:                                        #1661306266_c1
                if data_array[record_pos+1][0] == '':
                    continue
            except:                                     #1661306266_c2
                output_array.append( new_json )
            
            if record_pos != len(data_array) -1 :       #1661306266_d1
                output_array.append( new_json )
        return output_array

