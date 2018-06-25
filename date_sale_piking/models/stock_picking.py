# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError,UserError
import os
import  sys
import locale
from datetime import datetime,timedelta
class PickingWaiting(models.Model):
    _inherit = "stock.picking"
    
    customer_waiting_delivery = fields.Boolean('Espera de Cliente', default = False)
    waiting_delivery = fields.Boolean('Entrega en Espera', default = False)
