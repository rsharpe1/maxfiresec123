# -*- coding: utf-8 -*-

from ast import literal_eval
from odoo import _, api, fields, models


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    @api.model
    def create(self, vals):
        """
        Update owner_id in vals and return super.
        if 'Owner Assignment' is set in Field Service configuration settings
        """
        auto_owner_assignment = self.env['ir.config_parameter'].sudo().get_param(
            'zuma_equipments.auto_owner_assignment')
        if auto_owner_assignment == 'True':
            self._assign_owner(vals)
        return super(StockQuant, self).create(vals)

    def _assign_owner(self, vals):
        """
        Based on a number of conditions assign the owner_id to the location
        """

        location_dest_id = self.env['ir.config_parameter'].sudo().get_param('zuma_equipments.location_dest_id')
        owner_assignments = self.env['ir.config_parameter'].sudo().get_param('zuma_equipments.owner_assignment_ids')
        if 'location_id' in vals and 'product_id' in vals:
            if owner_assignments and location_dest_id:
                owner_assignments_ids = literal_eval(owner_assignments)
                product_id = self.env['product.product'].sudo().search([('id', '=', vals.get('product_id'))])
                if product_id and product_id.categ_id.id in owner_assignments_ids and int(location_dest_id) == vals.get(
                        'location_id'):
                    vals['owner_id'] = self.env.context.get('partner_id', False)


class Picking(models.Model):
    _inherit = "stock.picking"

    def _action_done(self):
        """
        Pass partner_id in context in order to assign owner_id at partner location in stock.quants
        if 'Owner Assignment' is set in Field Service configuration settings
        """
        auto_owner_assignment = self.env['ir.config_parameter'].sudo().get_param(
            'zuma_equipments.auto_owner_assignment')
        if auto_owner_assignment == 'True':
            self = self.with_context(partner_id=self.partner_id.id)
        return super(Picking, self)._action_done()
