# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    lines_note = fields.Html('Note')

    @api.onchange('sale_order_template_id')
    def _max_onchange_sale_order_template_id(self):
        if self.sale_order_template_id:
            template = self.sale_order_template_id.with_context(lang=self.partner_id.lang)
            if template:
                self.lines_note = template.lines_note

