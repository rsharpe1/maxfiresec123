# Copyright 2021 VentorTech OU
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, _
from odoo.exceptions import UserError


class User(models.Model):
    """ User entity. Add 'Default Printer' field (no restrictions).
    """
    _inherit = 'res.users'

    printnode_enabled = fields.Boolean(
        string='Auto-print via Direct Print',
        default=False,
    )

    printnode_printer = fields.Many2one(
        'printnode.printer',
        string='Default Printer',
    )

    scales_enabled = fields.Boolean(
        string='Auto-measure with Scales',
        default=False,
    )

    printnode_scales = fields.Many2one(
        'printnode.scales',
        string='Default Scales',
    )

    user_label_printer = fields.Many2one(
        'printnode.printer',
        string='Shipping Label Printer',
    )

    printnode_rule_ids = fields.One2many(
        comodel_name='printnode.rule',
        inverse_name='user_id',
        string='Direct Print Rules',
    )

    @property
    def SELF_READABLE_FIELDS(self):
        readable_fields = ['printnode_enabled',
                           'printnode_printer',
                           'printnode_scales',
                           'scales_enabled',
                           'user_label_printer',
                           'printnode_rule_ids']

        return super().SELF_READABLE_FIELDS + readable_fields

    @property
    def SELF_WRITEABLE_FIELDS(self):
        writable_fields = ['printnode_enabled',
                           'printnode_printer',
                           'printnode_scales',
                           'scales_enabled',
                           'user_label_printer']

        return super().SELF_WRITEABLE_FIELDS + writable_fields

    def get_shipping_label_printer(self):
        company = self.env.company

        printer = self.user_label_printer or company.company_label_printer
        if not printer:
            raise UserError(_(
                'Neither on company level, no on user level default label printer '
                'is defined. Please, define it.'
            ))
        return printer

    def get_report_printer(self, report_id):
        self.ensure_one()
        rule = self.printnode_rule_ids.filtered(lambda r: r.report_id.id == report_id)[:1]
        printer = rule.printer_id or self.printnode_printer or self.env.company.printnode_printer
        printer_bin = rule.printer_bin if rule.printer_id else printer.default_printer_bin
        return printer, printer_bin

    def get_scales(self):
        self.ensure_one()
        scales = self.printnode_scales or self.env.company.printnode_scales
        return scales
