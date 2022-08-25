# -*- coding: utf-8 -*-

from odoo import models, fields


class ProjectTask(models.Model):
    _inherit = 'project.task'

    product_id = fields.Many2one(
        related='helpdesk_ticket_id.product_id',
        string='Equipment', copy=False, store=True)
    lot_id = fields.Many2one(
        related='helpdesk_ticket_id.lot_id',
        string='Equipment Serial Number', copy=False, store=True)
