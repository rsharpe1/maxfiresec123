# -*- coding: utf-8 -*-
import json
from ast import literal_eval
from odoo import models, fields, api, _


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    product_domain = fields.Char(compute="_compute_product_domain", readonly=True, store=False)
    lots_domain = fields.Char(compute="_compute_lots_domain", readonly=True, store=False)

    @api.onchange('partner_id')
    def _compute_product_domain(self):
        """
        Compute domain for the Equipments

        Set the domain for all customer Equipments(From Customer Quants Tab)

        If 'Allow Equipment' is set on customer, then set the domain for all the additional Equipments
        that satisfy the following conditions:

        1): Location is in Stock Internal Locations set in Field Service configuration.
        2): Owner is not set
        3): Product is tracked by serials

        """
        for ticket in self:
            domain = [('id', '=', 0)]
            product_ids = self.env['product.product']
            if ticket.partner_id:
                partner_id = ticket.partner_id
                if ticket.partner_id.parent_id:
                    partner_id = ticket.partner_id.parent_id
                product_ids = partner_id.quant_ids.mapped('product_id')
                if partner_id.allow_equipment:
                    internal_location_ids = []
                    internal_location = self.env['ir.config_parameter'].sudo().get_param(
                        'zuma_equipments.internal_location_ids')
                    if internal_location:
                        internal_location_ids = literal_eval(internal_location)
                    domain = [('owner_id', '=', False), ('location_id', 'in', internal_location_ids)]
                    internal_quant_ids = self.env['stock.quant'].sudo().search(domain)
                    if internal_quant_ids:
                        internal_quants_product_ids = internal_quant_ids.mapped('product_id').filtered(lambda p: p.tracking != 'none')
                        product_ids += internal_quants_product_ids
            if product_ids:
                domain = [('id', 'in', product_ids.ids)]
            ticket.product_domain = json.dumps(domain)

    @api.onchange('partner_id', 'product_id')
    def _compute_lots_domain(self):
        """
        Compute domain for the Lots

        Get Lots from Quants

        """
        for ticket in self:
            domain = [('id', '=', 0)]
            if ticket.product_id:
                domain = [('product_id', '=', ticket.product_id.id)]
                lot_ids = self.env['stock.production.lot']
                if ticket.partner_id:
                    partner_id = ticket.partner_id
                    if ticket.partner_id.parent_id:
                        partner_id = ticket.partner_id.parent_id
                    lot_ids = partner_id.quant_ids.filtered(lambda p: p.product_id == ticket.product_id).mapped('lot_id')

                    if partner_id.allow_equipment:
                        internal_location_ids = []
                        internal_location = self.env['ir.config_parameter'].sudo().get_param(
                            'zuma_equipments.internal_location_ids')
                        if internal_location:
                            internal_location_ids = literal_eval(internal_location)
                        domain = [('owner_id', '=', False), ('location_id', 'in', internal_location_ids)]
                        internal_quant_ids = self.env['stock.quant'].sudo().search(domain)
                        if internal_quant_ids:
                            internal_quants_lot_ids = internal_quant_ids.mapped('lot_id')
                            lot_ids += internal_quants_lot_ids
                if lot_ids:
                    domain = [('id', 'in', lot_ids.ids)]
            ticket.lots_domain = json.dumps(domain)

    @api.onchange('lot_id')
    def _sd_onchange_lot_id(self):
        for ticket in self:
            if not ticket.product_id:
                ticket.product_id = ticket.lot_id.product_id

    @api.onchange('product_id')
    def _sd_onchange_product_id(self):
        for ticket in self:
            if ticket.product_id != ticket.lot_id.product_id:
                ticket.lot_id = False

    @api.onchange('partner_id')
    def _sd_onchange_partner_id(self):
        for ticket in self:
            ticket.product_id = False

    def action_open_product_lot_wizard(self):
        partner_id = self.partner_id
        if partner_id and partner_id.parent_id:
            partner_id = partner_id.parent_id
        lot_name = ''
        if self.lot_id:
            lot_name = self.lot_id.name
        return {
            'name': _('Add Customer Equipment'),
            'view_mode': 'form',
            'res_model': 'product.lot.wizard',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'context': {
                'default_helpdesk_ticket_id': self.id,
                'partner_id': partner_id.id,
                'default_product_id': self.product_id.id,
                'default_lot_name': lot_name,
            },
            'target': 'new'
        }
