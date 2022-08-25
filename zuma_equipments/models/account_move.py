# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    product_id = fields.Many2one('product.product',
                                 string='Equipment')
    lot_id = fields.Many2one(
        'stock.production.lot',
        string='Equipment Serial Number')
