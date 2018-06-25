# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError,UserError
import os
import  sys
import locale
from datetime import datetime, date, time, timedelta
import calendar
import pytz

class DateSalePiking(models.Model):
    _inherit = "sale.order"
    
    immediate_delivery = fields.Integer(string='Días de Entrega',default=5)
    exact_delivery_date = fields.Datetime('Fecha de Entrega')
    delivery_form = fields.Selection([('1', 'Fecha Inmediata'),('2', 'Fecha Exacta'),('3', 'Espera de Cliente')] , "Forma de Entrega", required=True, default='1',)
    date_ref = fields.Date('Fecha ref')
    @api.multi
    def action_confirm(self):
        for order in self:
            order.state = 'sale'
            order.confirmation_date = fields.Datetime.now()
            if self.env.context.get('send_email'):
                self.force_quotation_send()
            order.order_line._action_procurement_create()
            # valido las formas de envio
            #********
            if self.delivery_form == '1':
                for picking in order.picking_ids:
                    picking.min_date = self.get_immediate_delivery_work(picking.min_date)
            elif self.delivery_form == '2':
                for picking in order.picking_ids:
                    picking.min_date = self.get_exact_delivery_date()
            elif self.delivery_form == '3':
                for picking in order.picking_ids:
                    picking.customer_waiting_delivery = True
                    picking.waiting_delivery = True
            #********
        if self.env['ir.values'].get_default('sale.config.settings', 'auto_done_setting'):
            self.action_done()
        return True
        
    @api.multi
    def get_immediate_delivery_work(self,min_date):
        """retorna la fecha con la suma de los dias laborables a partir de la fecha actual y el valor de immediate_delivery"""
        date_object = datetime.strptime(min_date, '%Y-%m-%d %H:%M:%S')
        days_aux=int((datetime.isoweekday(datetime.now().date())+self.immediate_delivery)/5)*2+self.immediate_delivery
        date_object=date_object+timedelta(days=days_aux)
        if self.immediate_delivery < 0:
            raise UserError('La cantidad de días no puede ser menor a cero (0)!')
        return date_object

    @api.multi
    def get_exact_delivery_date(self):
        date_object = datetime.strptime(self.exact_delivery_date, '%Y-%m-%d %H:%M:%S')
        date_order_aux = datetime.strptime(self.date_order, '%Y-%m-%d %H:%M:%S')
        date_now = datetime.now()
        date_now = date_now + timedelta(seconds=-61)
        """
        if date_object < date_now:
            raise UserError('La fecha de envio no puede ser menor a la fecha de hoy!')
        """
        return date_object
    
    """
    @api.onchange('exact_delivery_date')
    def onchange_valid_exact_delivery_date(self):
        if self.exact_delivery_date:
            date_object = datetime.strptime(self.exact_delivery_date, '%Y-%m-%d %H:%M:%S')
            date_order_aux = datetime.strptime(self.date_order, '%Y-%m-%d %H:%M:%S')
            date_now = datetime.now()
            date_now = date_now + timedelta(seconds=-61)
            if date_object < date_now:
                raise UserError('La fecha de envio no puede ser menor a la fecha de hoy!')
    """
                
    @api.onchange('immediate_delivery')
    def onchange_immediate_delivery(self):
        """valida que la cantidad de dias de entrega no sea menor a 0"""
        if self.immediate_delivery < 0:
            raise UserError('La cantidad de días no puede ser menor a cero (0)!')


     

        
    
    
    
    
    
