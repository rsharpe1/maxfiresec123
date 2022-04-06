# -*- coding: utf-8 -*-

from collections import defaultdict
from odoo import _, models
from odoo.exceptions import UserError


class DymoCustomReport(models.AbstractModel):
    _name = 'report.max_fire_dymo_report.dymo_custom_report'
    _description = 'Product Label reter'

    def _get_report_values(self, docids, data):
        if data.get('active_model') == 'product.template':
            Product = self.env['product.template'].with_context(display_default_code=False)
        elif data.get('active_model') == 'product.product':
            Product = self.env['product.product'].with_context(display_default_code=False)
        else:
            raise UserError(_('Product model not defined, Please contact your administrator.'))

        total = 0
        quantity_by_product = defaultdict(list)
        for p, q in data.get('quantity_by_product').items():
            product = Product.browse(int(p))
            quantity_by_product[product].append((product.barcode, q))
            total += q
        if data.get('custom_barcodes'):
            # we expect custom barcodes format as: {product: [(barcode, qty_of_barcode)]}
            for product, barcodes_qtys in data.get('custom_barcodes').items():
                quantity_by_product[Product.browse(int(product))] += (barcodes_qtys)
                total += sum(qty for _, qty in barcodes_qtys)

        layout_wizard = self.env['product.label.layout'].browse(data.get('layout_wizard'))
        if not layout_wizard:
            return {}

        return {
            'quantity': quantity_by_product,
            'rows': layout_wizard.rows,
            'columns': layout_wizard.columns,
            'page_numbers': (total - 1) // (layout_wizard.rows * layout_wizard.columns) + 1,
            'price_included': data.get('price_included'),
            'extra_html': layout_wizard.extra_html,
        }

