# -*- coding: utf-8 -*-

from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    product_id = fields.Many2one(
        related='task_id.product_id',
        string='Equipment', copy=False)
    lot_id = fields.Many2one(
        related='task_id.lot_id',
        string='Equipment Serial Number', copy=False)

    def _create_invoices(self, grouped=False, final=False, date=None, start_date=None, end_date=None):
        res = super(SaleOrder, self)._create_invoices(grouped, final)
        if self.product_id:
            res.product_id = self.product_id.id
        if self.lot_id:
            res.lot_id = self.lot_id.id
        return res
