# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError

class ProductLabelLayout(models.TransientModel):
    _inherit = 'product.label.layout'
    print_format = fields.Selection(selection_add=[('dymo4_6', '4 X 6 Dymo'),
                                                   ('2x7xprice', '2 x 7 with price')
                                                   ], ondelete={'dymo4_6': 'cascade'}, default='dymo4_6')


    def _prepare_report_data(self):
        if self.custom_quantity <= 0:
            raise UserError(_('You need to set a positive quantity.'))
        # Get layout grid
        if self.print_format == 'dymo4_6':
            xml_id = 'max_fire_dymo_report.report_product_template_label_dymo_4_6'
        elif self.print_format == 'dymo':
            xml_id = 'product.report_product_template_label_dymo'
        elif 'x' in self.print_format:
            xml_id = 'product.report_product_template_label'
        else:
            xml_id = ''

        active_model = ''
        if self.product_tmpl_ids:
            products = self.product_tmpl_ids.ids
            active_model = 'product.template'
        elif self.product_ids:
            products = self.product_ids.ids
            active_model = 'product.product'

        # Build data to pass to the report
        data = {
            'active_model': active_model,
            'quantity_by_product': {p: self.custom_quantity for p in products},
            'layout_wizard': self.id,
            'price_included': 'xprice' in self.print_format,
        }
        return xml_id, data

