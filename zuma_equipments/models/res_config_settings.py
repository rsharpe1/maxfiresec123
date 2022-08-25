# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from ast import literal_eval


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    product_categ_id = fields.Many2one('product.category', string="Equipment Category")
    location_id = fields.Many2one('stock.location', domain=[('usage', '=', 'supplier')], string="Location for Equipment")
    location_dest_id = fields.Many2one('stock.location', domain=[('usage', '=', 'customer')],
                                       string="Destination Location for Equipment")
    auto_owner_assignment = fields.Boolean(string="Automatic Owner Assignment",
                                           config_parameter='zuma_equipments.auto_owner_assignment')
    owner_assignment_ids = fields.Many2many('product.category', string="Owner Assignment")
    internal_location_ids = fields.Many2many('stock.location', string="Stock Internal Locations",related='company_id.internal_location_ids', readonly=False,domain = "['|', ('company_id', '=', False), ('company_id', '=', company_id)]")

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('zuma_equipments.location_id', self.location_id.id)
        self.env['ir.config_parameter'].sudo().set_param('zuma_equipments.location_dest_id', self.location_dest_id.id)
        self.env['ir.config_parameter'].sudo().set_param('zuma_equipments.product_categ_id', self.product_categ_id.id)
        self.env['ir.config_parameter'].sudo().set_param('zuma_equipments.owner_assignment_ids', self.owner_assignment_ids.ids)
        # self.env['ir.config_parameter'].sudo().set_param('zuma_equipments.internal_location_ids', self.internal_location_ids.ids)
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        with_user = self.env['ir.config_parameter'].sudo()
        location_id = with_user.get_param('zuma_equipments.location_id')
        location_dest_id = with_user.get_param('zuma_equipments.location_dest_id')
        product_categ_id = with_user.get_param('zuma_equipments.product_categ_id')
        owner_assignment_ids = with_user.get_param('zuma_equipments.owner_assignment_ids')
        # internal_location_ids = with_user.get_param('zuma_equipments.internal_location_ids')
        if location_id:
            res.update(
                location_id=int(location_id))
        if location_dest_id:
            res.update(
                location_dest_id=int(location_dest_id))
        if product_categ_id:
            res.update(
                product_categ_id=int(product_categ_id))
        if owner_assignment_ids:
            res.update(
                owner_assignment_ids=[(6, 0, literal_eval(owner_assignment_ids))] if owner_assignment_ids else False, )
        # if internal_location_ids:
        #     res.update(
        #         internal_location_ids=[(6, 0, literal_eval(internal_location_ids))] if internal_location_ids else False, )
        return res
