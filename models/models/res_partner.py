# -*- coding: utf-8 -*-

from odoo import models, fields, api
from .odoo_migration import OdooMigration

import base64

import logging
_logging = logging.getLogger(__name__)

import xmlrpc.client

class ResPartnerInheritMigration(models.Model):
    _inherit = 'res.partner'

    
    
    def migrate(self, data):
        _logging.info("DEF_19 migrate")

        try:
            pwd = base64.b64decode( data.get('pwd') ).decode('utf-8')
        except:
            _logging.info("  Error: Password format incorrect")
            return False
        
        try:
            url = data.get('url') + "/jsonrpc"
        except:
            _logging.info("  Error: URL format incorrect")
            return False
        
        #Login DATA
        login_data = OdooMigration.get_loging_id(self,
            url, data.get('db'), data.get('usr'), pwd,
        )
        if login_data == False:
            _logging.info("ERROR: Login")
            return

        login_id = login_data.get('result')
        STOP42
        '''
        login_data = OdooMigration.get_loging_id(self,
                    url, data.get('db'), data.get('usr'), pwd,
                )
        '''             
        
        
        
        
        
        
        
        
        
        
        
        
        
        #payment_model = self.env['account.payment']
        #PROBAR LLAMANDO MANUALMENTE EL action_validate_invoice_payment con el SELF
        
        payment_int = 32098    #ID del PAGO
        account_move = 233835  #ID del Asiento Contable de la Factura
        account_move = 233890  #ID del Asiento Contable relacionado al PAGO
        
        account_move_line = 643877 #Apunte Contable Debito 0, Credito 1.99 
        
        payment_id = self.env['account.payment'].browse( payment_int )
        
        new_context = {'lang': 'es_CR', 'tz': 'America/Costa_Rica', 'uid': 2, 'allowed_company_ids': [1], 'params': {'action': 276, 'cids': 1, 'id': 233835, 'menu_id': 335, 'model': 'account.move', 'view_type': 'form'}, 'dont_redirect_to_payments': True, 'active_model': 'account.move', 'active_id': 233835, 'active_ids': [233835]}
        output = payment_id.with_context( new_context )
        output.action_post()
        
        _logging.info("  DEF30 output: %s", output)
        _logging.info("  DEF31 output._context: %s", output._context)
        
        invoice_id = self.env['account.move'].browse( invoice_int )
        new_context = {'bin_size': True, 'lang': 'es_CR', 'tz': 'America/Costa_Rica', 'uid': 2, 'allowed_company_ids': [1], 'params': {'action': 276, 'cids': 1, 'id': 233835, 'menu_id': 335, 'model': 'account.move', 'view_type': 'form'}, 'default_move_type': 'out_invoice'}
        output = invoice_id.with_context( new_context )._compute_authorized_transaction_ids()
        _logging.info("  DEF37 output: %s", output)
        
        return
        
        
        payment_model.action_validate_invoice_payment = "stuff"
        _logging.info( "DEF25: %s", dir(payment_model.action_validate_invoice_payment)  )
        
        STOP29
        ''' Opcion 1
        payment_model = self.env['account.payment']
        payment_id = payment_model.browse( payment_int )
        
        #_logging.info( "  DEF2 dir payment_id: %s", dir(payment_id) )
        #STOP26
        payment_id.invoice_origin = invoice_int
        _logging.info( "  DEF26 result: %s", payment_id.action_post() )
        return
        '''
        
        
        url1 = "https://avalantec-intecr1-stag1b-4314073.dev.odoo.com"
        db1 = "avalantec-intecr1-stag1b-4314073"
        username1 = "admin"
        password1 = "0987654321!"
        
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url1))
        _logging.info("DEF_19 common.version(): %s", common.version()) 
        
        uid = common.authenticate(db1, username1, password1, {})
        _logging.info("DEF_29 uid: %s", uid ) 
        
        models_xml = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url1))
        _logging.info("DEF_31 models: %s", models_xml ) 

        
        confirm_result = models_xml.execute_kw(db1, uid, password1,
            'account.payment',
            'action_validate_invoice_payment',
            [payment_int],
            {   
                'invoice_id': invoice_int,
                #"active_id": invoice_int,
                #"active_ids":[invoice_int],
                #"active_model": "account.move",
                #"default_invoice_ids": [invoice_int],#[[4,invoice_id,False]],
                #"journal_type":"sale",
                #"lang":"en_US",
                #"search_disable_custom_filters": True,
                #"type": "out_invoice",
                #"tz": False,
                
            },
        )
        
        _logging.info("DEF45 confirm_result: %s", confirm_result)
        return
        
        
        
        '''
        register_payment_row = [
            [payment_id],
            {
                "active_id": invoice_id,
                "active_ids":[invoice_id],
                "active_model": "account.move",
                "default_invoice_ids": [invoice_id],#[[4,invoice_id,False]],
                "journal_type":"sale",
                "lang":"en_US",
                "search_disable_custom_filters": True,
                "type": "out_invoice",
                "tz": False,
                #"uid": 2,
            }
        ]
        _logging.info("DEF52 register_payment_row: %s", register_payment_row )
        '''
        
        '''
        output = models_xml.execute_kw("avalantec-intecr1-stag1b-4314073", 2, "0987654321!")
        _logging.info("DEF42 output: %s", output)
        return
    
    
        '''
        
        confirm_result = models_xml.execute_kw(db1, uid, password1,
            'account.payment',
            'action_validate_invoice_payment',
            register_payment_row,
        )
        
        _logging.info("DEF45 confirm_result: %s", confirm_result)

        return
    
        
    def invoiceRegisterPayment(self,register_payment_row):        
        
        return confirm_result
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        invoice_id = self.env['account.move'].browse( 233835 )
        #_logging.info("DEF20 record_id: %s", dir(record_id) )
        
        payment_id = 32071
        vals = [{'date': '2022-03-02', 'amount': 1.23, 'payment_type': 'inbound', 'partner_type': 'customer', 'ref': '00100001040000000424time1655', 'journal_id': 71, 'currency_id': 39, 'partner_id': False, 'partner_bank_id': 10, 'payment_method_id': 1, 'destination_account_id': 6, 'payment_token_id': False, 'team_id': 1}]
        #payment_id = record_id.payment_id.create( vals ) # ========
        #payment_id.action_post()
        #payment_id.action_validate_invoice_payment
        #payment_id.authorized_transaction_ids
        #payment_id.transaction_ids()
        '''
        payment_id = self.env['account.payment']
            .with_context(active_ids=[self.id],active_model='account.invoice')
            .create({
            'amount': self.residual,
            'journal_id': journal_id.id,
            'payment_method_id': payment_method_ids and payment_method_ids[0].id
        })
        payment_id.action_validate_invoice_payment()
        '''
        
        
        account_payment = self.env['account.payment']
        payment_id = account_payment.with_context(active_ids=[invoice_id.id],active_model=['account.move'])\
            .create({
                'amount': 3.21,
                'journal_id': 71,
                'payment_method_id': 1,   #1 Manual inbound, 2 Manual outbound, 3 Electronic Inbound
                'partner_id': invoice_id.partner_id.id,
        })#.action_post()
        payment_id.action_validate_invoice_payment() #NO FUNCIONO
        #payment_id.reconciled_invoice_ids('XXXXXXX')
        _logging.info("DEF31 payment_transaction: %s", payment_id )
        
        #logging.info("  DEF25 payment_id: %s", dir(payment_id))
        #logging.info("  DEF26 payment_id: %s", payment_id)
        return
        
        #_logging.info("DEF24 output: %s", dir(output))
        _logging.info("DEF24 output: %s", output._name)
        
        #_logging.info("DEF20 record_id: %s", record_id.authorized_transaction_ids() )
        return
        
        '''
        #============================ _onchange_partner_id
        record_id = self.env['account.move'].browse(192219)
        _logging.info("  20 record_id: %s", record_id)
        _logging.info("  21 Fecha Contable: %s", record_id.date)
        _logging.info("  22 Fecha Vencimiento: %s", record_id.invoice_date_due)
        _logging.info("  23 Plazo de Pago: %s", record_id.invoice_payment_term_id.name)
        
        record_id.button_draft()
        record_id._onchange_partner_id()
        record_id.action_post()
        '''
        '''
        record_id.write({
            'partner_id': 73332,
        })
        '''
        
        return
        
        
        #============================
        try:
            pwd = base64.b64decode( data.get('pwd') ).decode('utf-8')
        except:
            _logging.info("  Error: Password format incorrect")
            return False
        
        try:
            url = data.get('url') + "/jsonrpc"
        except:
            _logging.info("  Error: URL format incorrect")
            return False
        
        #Login DATA
        login_data = OdooMigration.get_loging_id(self,
            url, data.get('db'), data.get('usr'), pwd,
        )
        if login_data == False:
            _logging.info("ERROR: Login")
            return

        login_id = login_data.get('result')
        
        #GET RECORDS ID
        _logging.info("  DEF25")
        search_filter = data.get('search_filter')
        if not search_filter:
            search_filter = []

        _logging.info("    DEF44")
        records_lst = OdooMigration.get_records_id(
            # url, db, login_id, pwd, model, search_filter
            self, url, data.get('db'), login_id, pwd,self._name, search_filter,
        )
        if records_lst == False:
            return
        _logging.info("  DEF57 records_lst: %s", records_lst)

        #GET RECORDS DATA
        _logging.info("  DEF56")
        remote_data_array = OdooMigration.export_data(
            #url, db, login_id, pwd, model, ids, vars1
            self, url, data.get('db'), login_id, pwd, self._name,
            records_lst, data.get('remote_vars'),
        )
        if remote_data_array == False:
            return
        #_logging.info("  66 remote_data_array: %s", remote_data_array)

        #Check Data if exists in THIS instance
        remote_vars = data.get('remote_vars')
        local_vars = data.get('local_vars')
        vars_len = len( remote_vars )
        _logging.info("    vars_len: %s", vars_len)

        _logging.info("72 INICIO DEL FOR remote_data_array=====")
        for remote_record_lst in remote_data_array:
            
            #Identifica el Remote External ID
            remote_record_id = remote_record_lst[0]
            
            #Obtiene el Local Record ID Objeto
            local_record_id = self.env.ref( remote_record_id )  # Es el Objeto Local
            _logging.info("    80 test: %s", local_record_id.get_external_id() )
            STOP81
            
            #Si no lo encuentra, se debe crear el registro
            if not local_record_id:
                STOP74_REGISTRO_NO_ENCONTRADO
                CREAR_UN_ARRAY_PARA_CREAR_REGISTRO_POSTERIORMENTE
                
            #recorre cada variable del registro y
            #hace match el dato local con data.get('remote_vars')
            _logging.info("84 INICIO DEL FOR=====")
            for index, value in enumerate( data.get('remote_vars') ):
                _logging.info("  86 Index: %s value: %s", index, value)
                remote_var = remote_vars[index]
                local_var = local_vars[index]
                if remote_var == "id":
                    _logging.info("  DEF_84 remote_var es ID, Continue")
                    continue
                remote_value = remote_record_lst[index]
                _logging.info("    88 remote_value: %s", remote_value)
                local_value = eval( "local_record_id.{0}".format( local_var ) )
                _logging.info("    90 local_value: %s", local_value)
                if remote_value == local_value:
                    continue
                else:
                    _logging.info("  DIFERENCIAS: REMOTE: %s LOCAL: %s",
                        remote_value, local_value)
                    STOP_SE_DEBE_ACTUALIZAR_EL_REGISTRO

            DETECTAR_SI_EXISTE_EL_EXTERNAL_ID_COMO_CAMPO_DE_UN_REGISTRO
                    
        return
        
        
        
        

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
