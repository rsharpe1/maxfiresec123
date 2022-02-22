# Copyright 2021 VentorTech OU
# See LICENSE file for full copyright and licensing details.
from odoo.tests import common


SECURITY_GROUP = 'printnode_base.printnode_security_group_user'


class TestPrintNodeCommon(common.TransactionCase):

    def setUp(self):
        super().setUp()

        self.company = self.env.ref('base.main_company')
        self.company.printnode_enabled = True
        self.company.printnode_recheck = False

        self.user = self.env['res.users'].with_context({
            'no_reset_password': True
        }).create({
            'name': 'Direct Print User',
            'company_id': self.company.id,
            'login': 'user',
            'email': 'user@print.node',
            'groups_id': [(6, 0, [
                self.env.ref(SECURITY_GROUP).id
            ])]
        })

        # report

        self.report = self.env['ir.actions.report'].create({
            'name': 'Model Overview',
            'model': 'ir.model',
            'report_type': 'qweb-pdf',
            'report_name': 'base.report_irmodeloverview',
        })

        # device

        self.account = self.env['printnode.account'].create({
            'api_key': 'apikey'
        })
        self.computer = self.env['printnode.computer'].create({
            'name': 'Local Computer',
            'status': 'connected',
            'account_id': self.account.id,
        })
        self.printer = self.env['printnode.printer'].create({
            'name': 'Local Printer',
            'status': 'offline',
            'computer_id': self.computer.id,
        })
        self.policy = self.env['printnode.report.policy'].create({
            'report_id': self.report.id,
        })
        self.so_model = self.env['ir.model'].search([('model', '=', 'sale.order')])
        self.so_report = self.env['ir.actions.report'].search([
            ('name', '=', 'Quotation / Order'),
        ])
        self.action_method = self._get_or_create_action_confirm()
        self.action_button = self.env['printnode.action.button'].create({
            'model_id': self.so_model.id,
            'method_id': self.action_method.id,
            'description': 'Print SO by confirm button',
            'report_id': self.so_report.id,
        })
        self.user_rule = self.env['printnode.rule'].create({
            'user_id': self.user.id,
            'printer_id': self.printer.id,
            'report_id': self.so_report.id,
        })
        self.del_slip_rep = self.env['ir.actions.report'].search([
            ('name', '=', 'Delivery Slip'),
        ])

    def _get_or_create_action_confirm(self):
        method = self.env['printnode.action.method'].search([
            ('model_id', '=', self.so_model.id),
            ('method', '=', 'action_confirm'),
        ])
        if not method:
            method = self.env['printnode.action.method'].create({
                'name': 'SO Print',
                'model_id': self.so_model.id,
                'method': 'action_confirm',
            })
        return method

    def _add_printers(self):
        company_printer = self.env['printnode.printer'].create({
            'name': 'Company Printer',
            'status': 'online',
            'computer_id': self.computer.id,
        })
        user_printer = self.env['printnode.printer'].create({
            'name': 'User Printer',
            'status': 'online',
            'computer_id': self.computer.id,
        })
        action_printer = self.env['printnode.printer'].create({
            'name': 'Action Printer',
            'status': 'online',
            'computer_id': self.computer.id,
        })
        return company_printer, user_printer, action_printer
