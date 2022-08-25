# -*- coding: utf-8 -*-
from odoo import models


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _prepare_invoice_values(self, order, name, amount, so_line):

        res = super(SaleAdvancePaymentInv, self)._prepare_invoice_values(order, name, amount, so_line)
        if res and order.product_id:
            res['product_id'] = order.product_id
        if res and order.lot_id:
            res['lot_id'] = order.lot_id
        return res
