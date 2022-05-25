# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrderTemplate(models.Model):
    _inherit = 'sale.order.template'

    lines_note = fields.Html('Note')