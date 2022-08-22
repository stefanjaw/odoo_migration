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
    _name = 'odoo_migration'
    _description = 'odoo_migration.odoo_migration'

    def get_login_id(self, url, db, user, pwd):
        _logging.info("get_login =======")
        payload1 = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "common",
                "method": "login",
                "args": [db, user, pwd],
            },
            "id": self.random_int(),
        }
        #result = self._make_request( url, payload1 )
        return self._make_request( url, payload1 )

    def _make_request(self, url, payload=False):
        #_logging.info("  _make_request TO REMOTE SERVER")
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
            _logging.info("  DEF33 Error: %s", msg)
            return  msg
        #_logging.info("35=== %s", response.get("error"))
        if 'error' in response.json():
            _logging.info(f"  DEF54 Error: {response.json()}")
            message = _('The url that this service requested returned an error. The url it tried to contact was %s. %s', url, response.json()['error']['message'])
            if response.json()['error']['code'] == 404:
                _logging.info("  DEF40 Error:")
                message = _('The url that this service does not exist. The url it tried to contact was %s', url)

            #return message
            return json.dumps(response.json()['error'])
        
        try:
            output = response.json()['result']
        except:
            output =  response.json()
        #_logging.info(f"  DEF67 result: \n{str(output)[0:300]}")
        return output

    def b64decode(self, string):
        return base64.b64decode(string)
    
    def random_int(self):
        return random.randint(0, 1000000000)
    
    def json_str(self, string):
        return json.dumps(string)
    
    def console_log(self,string):
        _logging.info( string  )
        return

    def get_timestamp(self):
         return int( datetime.datetime.now().timestamp() )
    
    def test(self):
        result = self.env['res.partner'].load(
            ['id','name'],
            [['__export__.testsdfsdf123213', 'testing abcdef']]
        )
        _logging.info("==> {0}".format(result))
        STOP72
    
    ''' 
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
    '''

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

    def get_records_id(self, url, db, login_id, pwd, query_model, search_filter, offset, limit, sort):
        _logging.info("get_records_id=================")
        payload1 = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute",
                "args": [
                    db, login_id, pwd,
                    query_model,
                    'search',
                    search_filter,
                    offset,  #Offset
                    limit,  #limit
                    sort,
                ],
            },
            "id": self.random_int(),
        }
        return self._make_request( url, payload1 )

    def get_records_count(self, url, db, login_id, pwd, query_model, search_filter, sort):
        _logging.info("get_records_id=================")
        payload1 = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute",
                "args": [
                    db, login_id, pwd,
                    query_model,
                    'search_count',
                    search_filter,
                ],
            },
            "id": self.random_int(),
        }
        return self._make_request( url, payload1 )

    def get_records_data(self, url, db, login_id, pwd, query_model, ids_array, vars_array):
        _logging.info("get_records_data=======")
        # remote data: ids_array, vars_array

        payload1 = {
            "jsonrpc": "2.0",
            "method": "call",
                "params": {
                    "service": "object",
                    "method": "execute",
                    "args": [
                        db, login_id, pwd,
                        query_model,
                        'export_data',
                        ids_array,
                        vars_array,
                    ],
                },
                "id": self.random_int(),
        }
        return self._make_request( url, payload1 )

    def load_records_data(self, load_model, local_vars, load_data  ):
        _logging.info("loading_records_data ==== Qty: {0}\n".format( len(load_data) )  )
        result_dict = {'ids': [], 'errors': [] }
        result = self.env[ load_model  ].sudo().load(    #!!! BUG: Se tiene que crear previo como company
                    local_vars,
                    load_data
                )
        if result.get('ids') == False:    #Errors Condition
            _logging.info("  DEF224 loading_records Vars\n:{0} Data: \n{1}\n\n".format( local_vars, load_data )  )
            msg = "  Error Result: {0}\n\nvars: {1}\n\nData {2}".format(result, local_vars, load_data)
            result_dict['errors'].append( [ msg ]  )
            _logging.info( f"DEF223 Error Result: {msg[0:3000]}" )
        elif result.get('ids') != False:  #OK Condition
            result_dict['ids'].append( result.get('ids')[0]  )

        #_logging( "  DEF228 result_dict: {0}".format(result_dict)[0:200] )

        return result_dict

    def get_data_to_load(self, data_array, local_vars, max_records_to_load  ): #1660494696
        _logging.info(f"get_data_to_load========Qty: { len(data_array) }" )

        records_data_to_load = []
        iguales_counter = 0
        for remote_record_data in data_array:               
            if len( records_data_to_load  ) >= max_records_to_load:
                break

            local_external_id = remote_external_id = remote_record_data[0]

            try:
                local_record_id = self.env.ref( remote_external_id, raise_if_not_found=False  ).sudo()  #SUDO
            except:
                local_record_id = self.env.ref( remote_external_id, raise_if_not_found=False  )
            #_logging.info("DEF268=====")

            #_logging("  DEF103 remote_record_data: {0}".format(remote_record_data))
            if local_record_id in [None, False]:
                records_data_to_load.append( remote_record_data  )
                continue

            local_record_data = local_record_id.sudo().with_context(lang='en_US').export_data( local_vars ).get('datas')[0]
            for x in range( len(remote_record_data) ):
                if type( remote_record_data[x] ) == bool and remote_record_data[x] == False:
                    remote_record_data[x] = ''
                elif type( remote_record_data[x] ) == str and remote_record_data[x] != '' and remote_record_data[x][-1] == ' ':
                    remote_record_data[x] = remote_record_data[x][0:-1]

            for x in range( len(local_record_data) ):
                if type( local_record_data[x] ) == bool and local_record_data[x] == False:
                    local_record_data[x] = ''
                elif type(local_record_data[x]) == datetime.datetime:
                    local_record_data[x] = local_record_data[x].isoformat(' ')
                elif type(local_record_data[x]) == datetime.date:
                    local_record_data[x] = local_record_data[x].isoformat()
                elif type( local_record_data[x] ) == str and local_record_data[x] != '' and local_record_data[x][-1] == ' ':
                    local_record_data[x] = local_record_data[x][0:-1]
            
            if remote_record_data == local_record_data:
                iguales_counter += 1
                if iguales_counter % 100 == 0:
                    _logging.info(f'    Iguales: { iguales_counter }')
                continue
            else:
                pass
            _logging.info(f"DEF276 diferentes==================\n{remote_record_data}\n\n{local_record_data}\n")
            records_data_to_load.append( remote_record_data  )
            continue
        _logging.info( f"Registros Iguales: {iguales_counter} - Nuevos o Diferentes: {len(records_data_to_load)}\n===========")
        return records_data_to_load


    def remove_messages_from_records( self, load_model, records_id ):
        records_id = self.env['mail.message'].search([
                        ('res_id','in', records_id),
                        ('model', '=', load_model)
                    ])
        return records_id.sudo().unlink()

    def value_format_change( self, records_to_load, local_vars  ):           #Validation: Remove Value False or Bool before LOAD Data 
        STOP334
        for index_record, record in enumerate(records_to_load):
            #_logging( "  DEF169 Record: {0}".format( records_to_load[ index_record  ] )  )
    
            for index_var, var_name in enumerate( local_vars  ):
      
                if records_to_load[ index_record  ][ index_var ] == False:      #Bool to String
                    records_to_load[ index_record  ][ index_var ] = "False"
                elif records_to_load[ index_record  ][ index_var ] == True:     #Bool to String
                    records_to_load[ index_record  ][ index_var ] = "True"

                #Special Changes
                if var_name == "category_id/id" and records_to_load[ index_record  ][ index_var ] in [False, "False"]:
                    records_to_load[ index_record  ][ index_var ] = ""

                if var_name == "credit_limit" and records_to_load[ index_record  ][ index_var ] in [False, "False"]:
                    records_to_load[ index_record  ][ index_var ] = ""

                if var_name == "email" and records_to_load[ index_record  ][ index_var ] not in [False, "False", ""]: #Replace empty Spaces in Email
                    #  #_logging( "  DEF183 EMAIL: {0}".format(  records_to_load[ index_record  ][ index_var ]  )  )
                    records_to_load[ index_record  ][ index_var ] = records_to_load[ index_record  ][ index_var ].replace( " ", ""  )
      
      
                #Si no tiene email se le coloca uno default ( Se utiliza solo cuando es individual )
                #if var_name == "email" and records_to_load[ index_record  ][ index_var ] in [False, "False", ""]:
                #  #_logging( "  DEF183 EMAIL: {0}".format(  records_to_load[ index_record  ][ index_var ]  )  )
                #  records_to_load[ index_record  ][ index_var ] = str( self.get_timestamp()  ) + default_no_email
  
                #Comentado, si el nombre tiene numeros revisar si es una compania
                #y no una persona en la configuracion del registro
                #if var_name == "name":          #Check if it has numbers
                #  _logging( "  DEF189 name: {0}".format(  records_to_load[ index_record  ][ index_var ]  )  )

  
                #_logging( "  DEF182 Record2: {0}".format( records_to_load[ index_record  ] )  )
  
        return records_to_load

    def bool_to_string(self, array_in):
        for record in range(len(array_in)):
            for item in range( len(array_in[record]) ):
                if type(array_in[record][item]) == bool:
                    array_in[record][item] = str( array_in[record][item] )
        return array_in

    def vars_value_replace(self, array_vars, array_data, var_name, value_in, value_out ):
        try:
            var_pos = array_vars.index( var_name,  )
        except:
            _logging.info(f'    ERROR:var {var_name} not found in {array_vars}')
            return []
        
        for record in range(len(array_data)):
            if len( array_vars ) != len( array_data[record] ):
                _logging.info('  Error: Cantidad de elementos diferentes en vars: {array_vars}\n{array_data[record]}')
                return
            value = array_data[record][var_pos]
            if value == value_in:
                array_data[record][var_pos] = value_out
        return array_data

