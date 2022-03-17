# Copyright 2021 VentorTech OU
# See LICENSE file for full copyright and licensing details.
from random import randint

from odoo.tests import tagged, Form
from odoo.addons.printnode_base.tests.common import TestPrintNodeCommon


@tagged('post_install', '-at_install')
class TestProductLabelLayout(TestPrintNodeCommon):

    def test_raise_product_product_multi_printing_wizard(self):
        self.env.user.printnode_printer = self.printer

        prods = self.env['product.product'].create([
            {'name': 'product_variant_1'},
            {'name': 'product_variant_2'}
        ])
        action = prods.action_open_label_layout()
        ctx = action['context'].copy()
        ctx['active_model'] = 'product.product'
        form_wizard = Form(self.env['product.label.layout'].with_context(ctx))
        wiz = form_wizard.save()
        self.assertEqual(self.env.user.printnode_printer.id, wiz.printer_id.id)
        self.assertEqual(wiz.product_line_ids.mapped('product_id'), prods)

    def test_raise_product_template_multi_printing_wizard(self):
        self.env.user.printnode_printer = self.printer

        prods = self.env['product.product'].create([
            {'name': 'product_tmpl_1'},
            {'name': 'product_tmpl_2'}
        ])
        templs = prods.mapped('product_tmpl_id')
        action = templs.action_open_label_layout()
        ctx = action['context'].copy()
        ctx['active_model'] = 'product.template'
        form_wizard = Form(self.env['product.label.layout'].with_context(ctx))
        wiz = form_wizard.save()

        self.assertEqual(self.env.user.printnode_printer.id, wiz.printer_id.id)
        self.assertEqual(wiz.product_line_ids.mapped('product_tmpl_id'), templs)

    def test_raise_stock_picking_multi_printing_wizard(self):
        products = []
        total_qty = 0
        self.env.user.printnode_printer = self.printer

        for i in range(1, 6):
            product = self.env['product.product'].create({
                'name': 'product_{}'.format(i),
                'type': 'product',
            })
            qty = randint(1, 5)
            total_qty += qty
            products.append((product, qty))

        self.customer = self.env['res.partner'].create({
            'name': 'Customer',
        })
        self.sale_order = self.env['sale.order'].create({
            'partner_id': self.customer.id,
            'order_line':
            [(0, 0, {'product_id': prod.id, 'product_uom_qty': qty}) for prod, qty in products],
        })
        self.sale_order.action_confirm()

        wh_out = self.sale_order.picking_ids[:1]
        action = wh_out.action_open_label_layout()
        ctx = action['context'].copy()
        form_wizard = Form(self.env['product.label.layout'].with_context(ctx))
        wiz = form_wizard.save()
        self.assertEqual(wiz.picking_quantity, 'picking')
        self.assertEqual(self.env.user.printnode_printer.id, wiz.printer_id.id)
        self.assertEqual(
            wiz.product_line_ids.mapped('product_id.id'),
            [p.id for p, q in products]
        )
