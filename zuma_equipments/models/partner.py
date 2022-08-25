# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    quant_ids = fields.One2many('stock.quant', 'owner_id', compute='_compute_quant_ids')
    allow_equipment = fields.Boolean('Allow Equipment', default=False,
                                     help="Show all equipment that are not assign to any other.")
    show_equipment_button = fields.Boolean(related='company_id.show_equipment_button')

    def _compute_quant_ids(self):
        """
        If we don't compute the Quants odoo will get all the quants of this contact, so for this purpose
        we are filtering the ones at 'Partner Locations/Customers' only.
        """
        for partner in self:
            location_dest_id = self.env['ir.config_parameter'].sudo().get_param('zuma_equipments.location_dest_id')
            if location_dest_id:
                domain = [('location_id', '=', int(location_dest_id)), ('owner_id', '=', partner.id)]
                partner.quant_ids = self.env['stock.quant'].sudo().search(domain)
            else:
                partner.quant_ids = False

    def action_open_zuma_equipments_wizard(self):
        return {
            'name': _('Add Customer Equipment'),
            'view_mode': 'form',
            'res_model': 'product.lot.wizard',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'context': {
                'is_customer': self.name,
                'partner_id': self.id,
            },
            'target': 'new'
        }
