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
            _logging.info("  37Error:")
            message = _('The url that this service requested returned an error. The url it tried to contact was %s. %s', url, response.json()['error']['message'])
            if response.json()['error']['code'] == 404:
                _logging.info("  40Error:")
                message = _('The url that this service does not exist. The url it tried to contact was %s', url)
            #return message
            return json.dumps(response.json()['error'])
        
        try:
            output = response.json()['result']
        except:
            output =  response.json()
        _logging.info(f"  DEF67 result: \n{str(output)[0:300]}")
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

    def get_records_data(self, url, db, login_id, pwd, query_model, ids_array, vars_array):
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
        #_logging("DEF95 Loading Records Qty: {0}".format( len(load_data) )  )
        #_logging( "  DEF95 LOAD RECORDS DATA: {0}".format(  load_data)[0:300] )
        result_dict = {'ids': [], 'errors': [] }
                                                                                            # QUITAAAAAR
        for record_data in load_data:
            #_logging( "  DEF98 record_data: {0}".format(  record_data[0]  )  )

            record_id = self.env.ref( record_data[0], raise_if_not_found=False   )
            #_logging("DEF102 Record_id Existente: {0}".format(record_id  ))
            record_new = False
            if record_id == None:
                #_logging("DEF104 Creando record temporal")
                record_new = True
                result = self.env[ load_model  ].sudo().load(    #!!! BUG: Se tiene que crear previo como company
                            ['id',  'name', 'company_type'],                    #Es un error de Odoo que por default lo pone como person
                            [[ record_data[0], 'NombreTemporal',  'company']],
                        )
                #_logging( "  DEF112 result temporal name: {0}".format(  result  )  )
                record_id_int = result.get('ids')                                       #GET TEMPO RECORD IDs
                record_id = self.env[ load_model  ].sudo().browse( record_id_int )
            else:
                pass
    
            result = record_id.sudo().load(
                        local_vars,
                        [ record_data ],
                    )
            #_logging( "  DEF113 result DEBE SER EL MISMO RECORD ID: {0}".format(  result  )  )
    

            if result.get('ids') == False:    #Errors Condition
                msg = "  DEF123 Error: Result: {0}\n\nvars: {1}\nData {2}".format(result, local_vars, record_data)
                result_dict['errors'].append( [ msg ]  )
                #_logging( msg )
                #_logging( "  DEF126 Eliminando registro temporal: {0}".format(  record_id  )  )
                if record_new == True:
                    record_id.sudo().unlink()
            elif result.get('ids') != False:  #OK Condition
                result_dict['ids'].append( result.get('ids')[0]  )
        #_logging( "  DEF128 result_dict: {0}".format(result_dict)[0:200] )
  
        return result_dict

    def get_data_to_load(self, data_array, local_vars, max_records_to_load  ):                    # Create Record external_id if it's not found locally
        _logging.info("  DEF253 get_data_to_load======== " )

        records_data_to_load = []
        for remote_record_data in data_array:               
            #_logging.info(f"DEF91: remote_record_data: \n{remote_record_data}\n")
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
                #_logging.info("  DEF272")
      
                records_data_to_load.append( remote_record_data  )
                continue

            #_logging.info("DEF277=====")

            local_record_data = local_record_id.sudo().export_data( local_vars ).get('datas')[0]

            for x in range( len(remote_record_data) ):
                if type( remote_record_data[x] ) == bool and remote_record_data[x] == False:
                    remote_record_data[x] = ''
                if type( remote_record_data[x] ) == str and remote_record_data[x] != '' and remote_record_data[x][-1] == ' ':
                    remote_record_data[x] = remote_record_data[x][0:-1]

            for x in range( len(local_record_data) ):
                if type(local_record_data[x]) == datetime.datetime:
                    local_record_data[x] = local_record_data[x].isoformat(' ')
                if type( local_record_data[x] ) == str and local_record_data[x] != '' and local_record_data[x][-1] == ' ':
                    local_record_data[x] = local_record_data[x][0:-1]
            
            if remote_record_data == local_record_data:
                _logging.info(f'DEF288 Iguales: { remote_record_data[0] }')
                continue
            else:
                pass
            _logging.info(f"DEF294 diferentes==================\n{remote_record_data}\n\n{local_record_data}\n")
            records_data_to_load.append( remote_record_data  )
            continue
            '''
            STOP286
            for index_var, local_var_name in enumerate( local_vars ):            # BUSQUEDA DE CADA VAR
                remote_value = remote_record_data[ index_var  ]
                local_value = local_record_data[ index_var  ]
                #_logging( "Local Var: {2}\nremote_value: {0}\nlocal_value:  {1} ".format(remote_value, local_value, local_var_name)  )    #Comparando el valor de cada variable
                if remote_value == local_value:
                    continue
                elif remote_value == False and local_value == "":
                    continue
                elif local_var_name == "email" and remote_value in ["", False]:   #No toma en cuenta si el email viene vacío
                    #_logging("  DEF138 remote Email is empty for the record: {0}".format( remote_record_data ) )
                    continue
                elif local_var_name == "email" and local_value.replace(" ", "") == remote_value.replace(" ", ""): #Emails con espacios no los considera
                    continue
      
                #_logging( "  DEF140 Registros Diferentes para VAR: {4}\nremote value: {0}\nlocal_value: {1}\nremote_record_data: {2}\nlocal_record_data:  {3}".format(
                #    remote_value, local_value, remote_record_data, local_record_data, local_var_name )[0:2000]
                #)

                records_data_to_load.append(  remote_record_data  )
                break
                #raise UserError(  "115 Diferentes Valores\nRemote value: {0}\n  Local value: {1}".format( remote_value, local_value )  )
            '''
        #_logging( "DEF152 records_data_to_load: {0}".format( records_data_to_load ))
        return records_data_to_load


    def remove_messages_from_records( load_model, records_id ):
        STOP310
        records_id = env['mail.message'].search([
                        ('res_id','in', records_id),
                        ('model', '=', load_model)
                    ])
        #_logging( "  DEF162 messages records_id: {0}".format( records_id )  )
        return records_id.sudo().unlink()

    def value_format_change( self, records_to_load, local_vars  ):           #Validation: Remove Value False or Bool before LOAD Data 
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


