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
        _logging.info(f"  DEF54 remote_move_ints: {remote_move_ints}")

        remote_move_header_data = self.get_records_data( remote_url, remote_db, login_id, remote_pwd, 'account.move', remote_move_ints, remote_vars ) 
        _logging.info(f"  DEF57 \nvars: {remote_vars} \nremote_move_header_data: {remote_move_header_data}\n\n")

        list_var = 'invoice_line_ids.id'
        remote_account_move_json_list = self.data_array_to_data_json( list_var, remote_vars, remote_move_header_data.get('datas') )
        _logging.info(f"  DEF61 \nremote_account_move_json_list: {remote_account_move_json_list}\n\n")

        remote_account_move_json_list = self.change_variables( remote_account_move_json_list )
        _logging.info(f"  DEF64 \nremote_account_move_json_list: {remote_account_move_json_list}\n\n")

        for record in remote_account_move_json_list:  # 1663729248_10
            _logging.info(f"DEF62 account_move Record : {record}\n")
            xml_ids_to_create = set()
            try:
                if self.env.ref( record['id'] ):
                    _logging.info(f"  Ya Existe ID: { self.env.ref( record[0] ) } con External ID: {record[0]} ")
                    continue
            except:
                pass

            if record[ 'move_type' ] == "Customer Invoice":
                record[ 'move_type' ] = "out_invoice"

            _logging.info(f"DEF75 ========== Convert Ext Id to Local") 
            account_move_json_result = self.convert_external_id_to_local( remote_vars, record )
            _logging.info(f"DEF77 Local account_move_json_result: { account_move_json_result }")
            
            account_move_json = account_move_json_result.get('record_json')
            _logging.info(f"DEF80 account_move_json: { account_move_json }")

            xml_ids_to_create.update( account_move_json_result.get('not_found') )
            _logging.info(f"DEF87 xml_ids_to_create: {xml_ids_to_create}" )

            #Set Partner Account Payable
            currency_int = account_move_json.get('currency_id')
            #_logging.info(f"DEF90 currency_int: { currency_int }")
            currency_name = self.env['res.currency'].browse( currency_int ).name
            #_logging.info(f"DEF92 currency_name: { currency_name }")
            if currency_name == "USD":
                account_id = self.env['account.account'].search([
                    ('code', '=', '113002') # USD
                ])
            else: #currency_name == "CRC":
                account_id = self.env['account.account'].search([
                    ('code', '=', '113001') # CRC
                ])
            partner_int = account_move_json.get('partner_id')
            partner_id = self.env['res.partner'].browse( partner_int )
            partner_id.write({ 'property_account_receivable_id': account_id.id  })

            try:
                remote_line_ints = account_move_json.get( 'invoice_line_ids' )
            except:
                remote_line_ints = False

            for x in range(0, len(remote_line_ints) ):
                remote_line_ints[x] = int( remote_line_ints[x] )

            #_logging.info(f"DEF97 remote_line_ints: { remote_line_ints }" )
            
            remote_move_lines_data = self.get_records_data( remote_url, remote_db, login_id, remote_pwd, 'account.move.line', remote_line_ints , remote_line_vars )
            #_logging.info(f"DEF88 remote_move_lines_data: { remote_move_lines_data }" )

            list_var = 'NO_HAY_LINEAS_EN_ZERO'
            move_lines_json = self.data_array_to_data_json( list_var, remote_line_vars, remote_move_lines_data.get('datas') )
            _logging.info(f"DEF104 move_lines_json: { move_lines_json }\n\n" )

            local_move_lines = []
            for move_line in move_lines_json:
                #_logging.info( f"DEF99 move_line: { move_line }" )
                move_line_local_data = self.convert_external_id_to_local( remote_line_vars, move_line )
                #_logging.info(f"DEF110 move_line_local_data: { move_line_local_data }" )

                try:
                    if move_line_local_data.get('record_json').get('tax_ids') != False \
                            and type(move_line_local_data.get('record_json').get('tax_ids')) != list:
                        
                        move_line_local_data['record_json']['tax_ids'] = [ move_line_local_data.get('record_json').get('tax_ids') ] 
                except:
                    pass

                #_logging.info(f"DEF115 move_line_local_data: { move_line_local_data }" )
                local_move_lines.append( move_line_local_data.get('record_json') )
                #_logging.info(f"DEF104 local_move_lines: { local_move_lines }" )
                xml_ids_to_create.update( move_line_local_data.get('not_found') )

                #_logging.info(f"DEF118 tax_ids: {type(move_line.get('tax_ids'))} {move_line.get('tax_ids')}")

                #_logging.info( f"DEF115 local_move_lines: { local_move_lines }\n\n" )

            _logging.info(f"DEF122 account_move_json: { account_move_json }\
                    \n\nlocal_move_lines: { local_move_lines }\n\n xml_ids_to_create: { xml_ids_to_create }  " )
            account_move_json['invoice_line_ids'] = local_move_lines

            _logging.info(f"DEF133 account_move_json: { account_move_json }")

            move_id = self.env['account.move'].create( account_move_json )
            _logging.info(f"DEF136 move_id: { move_id}")
            
            #Create External ID account_move
            external_id_data = {
                    'name': record.get('id').split('.')[1],  # [0].split('.')[1],
                    'module': record.get('id').split('.')[0], # [0].split('.')[0],
                    'model': remote_model,
                    'res_id': move_id.id
                }
            self.env['ir.model.data'].create( external_id_data )
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
            if var_name == "invoice_line_ids.id":
                #_logging.info(f"DEF183====")
                new_json[ var_name[:-3] ] = record_json[var_name]
            elif var_name[-3:] == "/id" and record_json[var_name] != False:
                #_logging.info(f"DEF186====")
                try:
                    new_json[ var_name[:-3] ] = self.env.ref( record_json[var_name] ).id
                except:
                    #_logging.info(f"Error: HAY UN EXCEPT ====== ")
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

    def data_array_to_data_json( self, list_var, vars_array, data_array ): # 1661306266
        #_logging.info(f"DEF237 data_array: { data_array }")
        try:
            list_var_pos = vars_array.index( list_var )
        except:
            list_var_pos = 100000
        output_array = []
        
        for record_pos in range(0, len(data_array) ):   #1661306266_a
            #_logging.info(f"DEF256 record_pos: { record_pos }"  ) 
            if data_array[record_pos][0] != '':
                new_json = {}
                sub_list = []
                create_json = True
            else:
                create_json = False

            #_logging.info(f"DEF263 ") 

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
        #_logging.info(f"DEF273 output_array: { output_array }")
        return output_array


    def change_variables(self, json_lst):   # 1664318830
        for record in json_lst:

            if record.get('type_document_selection/code') == '09':
                record.pop('type_document_selection/code')
                record['move_type_extra'] = 'fee'

        return json_lst
