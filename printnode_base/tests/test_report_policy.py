# Copyright 2021 VentorTech OU
# See LICENSE file for full copyright and licensing details.
from unittest.mock import patch

from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tools import mute_logger
from odoo.addons.printnode_base.tests.common import TestPrintNodeCommon


@tagged('post_install', '-at_install')
class TestPrintNodeReport(TestPrintNodeCommon):

    @mute_logger('odoo.addons.printnode_base.models.printnode_device')
    def test_printnode_module_disabled(self):
        self.company.printnode_enabled = False

        with self.assertRaises(UserError), self.cr.savepoint():
            self.printer.with_user(self.user.id).printnode_check_and_raise()

    @mute_logger('odoo.addons.printnode_base.models.printnode_device')
    def test_printnode_recheck(self):
        self.company.printnode_enabled = True
        self.company.printnode_recheck = True

        with self.assertRaises(UserError), self.cr.savepoint(), \
                patch.object(type(self.account), 'recheck_printer', return_value=False):
            self.printer.with_user(self.user.id).printnode_check_and_raise()

    def test_printnode_no_recheck(self):
        self.company.printnode_enabled = True

        self.printer.with_user(self.user.id).printnode_check_and_raise()

    def test_printnode_policy_report_no_size_and_printer_no_size(self):
        self.company.printnode_enabled = True

        self.policy.report_paper_id = None
        self.printer.paper_ids = [(5, 0, 0)]

        self.printer.with_user(self.user.id).printnode_check_report(self.report)

    @mute_logger('odoo.addons.printnode_base.models.printnode_device')
    def test_printnode_policy_report_no_size_and_printer_size(self):
        self.company.printnode_enabled = True

        self.policy.report_paper_id = None
        self.printer.paper_ids = [(6, 0, [
            self.env.ref('printnode_base.printnode_paper_a4').id])]

        with self.assertRaises(UserError), self.cr.savepoint():
            self.printer.with_user(self.user.id).printnode_check_report(self.report)

    @mute_logger('odoo.addons.printnode_base.models.printnode_device')
    def test_printnode_policy_report_size_and_printer_no_size(self):
        self.company.printnode_enabled = True

        self.policy.report_paper_id = \
            self.env.ref('printnode_base.printnode_paper_a6')
        self.printer.paper_ids = [(5, 0, 0)]

        self.printer.with_user(self.user.id).printnode_check_report(self.report)

    @mute_logger('odoo.addons.printnode_base.models.printnode_device')
    def test_printnode_policy_report_size_not_eq_printer_size(self):
        self.company.printnode_enabled = True

        self.policy.report_paper_id = \
            self.env.ref('printnode_base.printnode_paper_a6')
        self.printer.paper_ids = [(6, 0, [
            self.env.ref('printnode_base.printnode_paper_a4').id])]

        with self.assertRaises(UserError), self.cr.savepoint():
            self.printer.with_user(self.user.id).printnode_check_report(self.report)

    def test_printnode_policy_report_size_eq_printer_size(self):
        self.company.printnode_enabled = True

        self.policy.report_paper_id = \
            self.env.ref('printnode_base.printnode_paper_a6')
        self.printer.paper_ids = [(6, 0, [
            self.env.ref('printnode_base.printnode_paper_a6').id])]

        self.printer.with_user(self.user.id).printnode_check_report(self.report)

    @mute_logger('odoo.addons.printnode_base.models.printnode_device')
    def test_printnode_policy_report_type_and_printer_no_type(self):
        self.company.printnode_enabled = True

        self.policy.report_type = 'qweb-pdf'
        self.printer.format_ids = [(5, 0, 0)]

        self.printer.with_user(self.user.id).printnode_check_report(self.report)

    @mute_logger('odoo.addons.printnode_base.models.printnode_device')
    def test_printnode_policy_report_type_not_eq_printer_type(self):
        self.company.printnode_enabled = True

        self.policy.report_type = 'qweb-pdf'
        self.printer.format_ids = [(6, 0, [
            self.env.ref('printnode_base.printnode_content_type_raw').id])]

        with self.assertRaises(UserError), self.cr.savepoint():
            self.printer.with_user(self.user.id).printnode_check_report(self.report)

    def test_printnode_policy_report_type_eq_printer_type(self):
        self.company.printnode_enabled = True

        self.policy.report_type = 'qweb-pdf'
        self.printer.format_ids = [(6, 0, [
            self.env.ref('printnode_base.printnode_content_type_pdf').id])]

        self.printer.with_context(user=self.user).printnode_check_report(self.report)

    @mute_logger('odoo.addons.printnode_base.models.printnode_device')
    def test_printnode_policy_attachment_wrong_type(self):
        self.company.printnode_enabled = True

        self.printer.paper_ids = [(6, 0, [
            self.env.ref('printnode_base.printnode_paper_a4').id])]
        self.printer.format_ids = [(6, 0, [
            self.env.ref('printnode_base.printnode_content_type_raw').id])]

        with self.assertRaises(UserError), self.cr.savepoint():
            self.printer.with_user(self.user.id).printnode_check_and_raise({
                'title': 'Label',
                'type': 'qweb-pdf',
                'size': self.env.ref('printnode_base.printnode_paper_a4'),
            })

    @mute_logger('odoo.addons.printnode_base.models.printnode_device')
    def test_printnode_policy_attachment_wrong_size(self):
        self.company.printnode_enabled = True

        self.printer.paper_ids = [(6, 0, [
            self.env.ref('printnode_base.printnode_paper_a6').id])]
        self.printer.format_ids = [(6, 0, [
            self.env.ref('printnode_base.printnode_content_type_pdf').id])]

        with self.assertRaises(UserError), self.cr.savepoint():
            self.printer.with_user(self.user.id).printnode_check_and_raise({
                'title': 'Label',
                'type': 'qweb-pdf',
                'size': self.env.ref('printnode_base.printnode_paper_a4'),
            })

    @mute_logger('odoo.addons.printnode_base.models.printnode_device')
    def test_printnode_policy_attachment_empty_params(self):
        self.company.printnode_enabled = True

        self.printer.paper_ids = [(6, 0, [
            self.env.ref('printnode_base.printnode_paper_a4').id])]
        self.printer.format_ids = [(6, 0, [
            self.env.ref('printnode_base.printnode_content_type_pdf').id])]

        with self.assertRaises(UserError):
            self.printer.with_user(self.user.id).printnode_check_and_raise({
                'title': 'Label',
            })

    def test_printnode_policy_attachment_valid_params(self):
        self.company.printnode_enabled = True

        self.printer.paper_ids = [(6, 0, [
            self.env.ref('printnode_base.printnode_paper_a4').id])]
        self.printer.format_ids = [(6, 0, [
            self.env.ref('printnode_base.printnode_content_type_pdf').id])]

        self.printer.with_user(self.user.id).printnode_check_and_raise({
            'title': 'Label',
            'type': 'qweb-pdf',
            'size': self.env.ref('printnode_base.printnode_paper_a4'),
        })

    def test_action_domain(self):
        self.partner_1 = self.env['res.partner'].create({'name': 'Direct Print Partner1'})
        self.partner_2 = self.env['res.partner'].create({'name': 'Direct Print Partner2'})
        self.sl_order = self.env['sale.order'].create({'partner_id': self.partner_1.id})

        # Empty action domain
        self.assertEqual(self.action_button.domain, '[]')
        objects = self.action_button._get_model_objects(self.sl_order.ids)
        self.assertEqual(objects, self.sl_order)

        # Set action domain for 'partner_1' (partner for 'sl_order')
        self.action_button.domain = '[["partner_id", "=", %s]]' % self.partner_1.id
        objects = self.action_button._get_model_objects(self.sl_order.ids)
        self.assertEqual(objects, self.sl_order)

        # Set action domain for 'partner_2'. Sale Order will be filtered.
        self.action_button.domain = '[["partner_id", "=", %s]]' % self.partner_2.id
        objects = self.action_button._get_model_objects(self.sl_order.ids)
        self.assertFalse(objects)

    def test_get_printer_for_action_button(self):
        company_printer, user_printer, action_printer = self._add_printers()

        self.company.write({'printnode_printer': company_printer.id})
        self.user.write({'printnode_printer': user_printer.id})
        self.action_button.write({'printer_id': action_printer.id})

        # Expected ActionButton Printer
        printer, printer_bin = self.action_button.with_user(self.user.id)._get_action_printer()
        self.assertEqual(printer.id, action_printer.id)

        # Expected UserRule Printer
        self.action_button.write({'printer_id': False})
        printer, printer_bin = self.action_button.with_user(self.user.id)._get_action_printer()
        self.assertEqual(printer.id, self.user_rule.printer_id.id)

        # Expected User's Printer
        self.user_rule.write({'report_id': self.del_slip_rep.id})
        printer, printer_bin = self.action_button.with_user(self.user.id)._get_action_printer()
        self.assertEqual(printer.id, self.user.printnode_printer.id)

        # Expected Company's Printer
        self.user.write({'printnode_printer': False})
        printer, printer_bin = self.action_button.with_user(self.user.id)._get_action_printer()
        self.assertEqual(printer.id, self.company.printnode_printer.id)

    def test_get_printer_within_report_download(self):
        company_printer, user_printer, _ = self._add_printers()

        self.company.write({'printnode_printer': company_printer.id})
        self.user.write({'printnode_printer': user_printer.id})

        # Expected UserRule Printer
        self.action_button.write({'printer_id': False})
        printer, printer_bin = self.user.get_report_printer(self.so_report.id)
        self.assertEqual(printer.id, self.user_rule.printer_id.id)

        # Expected User's Printer
        self.user_rule.write({'report_id': self.del_slip_rep.id})
        printer, printer_bin = self.user.get_report_printer(self.so_report.id)
        self.assertEqual(printer.id, self.user.printnode_printer.id)

        # Expected Company's Printer
        self.user.write({'printnode_printer': False})
        printer, printer_bin = self.user.get_report_printer(self.so_report.id)
        self.assertEqual(printer.id, self.company.printnode_printer.id)
