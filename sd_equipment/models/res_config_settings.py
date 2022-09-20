# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from ast import literal_eval


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    location_id = fields.Many2one('stock.location', domain=[('usage', '=', 'supplier')], string="Location for Equipment")
    location_dest_id = fields.Many2one('stock.location', domain=[('usage', '=', 'customer')],
                                       string="Destination Location for Equipment")
    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('sd_equipment.location_id', self.location_id.id)
        self.env['ir.config_parameter'].sudo().set_param('sd_equipment.location_dest_id', self.location_dest_id.id)
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        with_user = self.env['ir.config_parameter'].sudo()
        location_id = with_user.get_param('sd_equipment.location_id')
        location_dest_id = with_user.get_param('sd_equipment.location_dest_id')
        if location_id:
            res.update(
                location_id=int(location_id))
        if location_dest_id:
            res.update(
                location_dest_id=int(location_dest_id))
        return res
