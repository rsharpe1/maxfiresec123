# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, api, fields, _
from odoo.exceptions import ValidationError


class ProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    partner_id = fields.Many2one('res.partner')

    @api.model
    def create(self, vals_list):
        res = super(ProductionLot, self).create(vals_list)
        if res and self.env.context.get('is_equipment'):
            res._create_and_process_moves(res)
        return res

    def _create_and_process_moves(self, lot_id):
        """
        Create Moves, related move lines and trigger _action_done() to create Quants on 'Partner Locations/Customers'.

        :param lot_id: Lot to get values from
        """
        location_id = self.env['ir.config_parameter'].sudo().get_param('zuma_equipments.location_id')
        location_dest_id = self.env['ir.config_parameter'].sudo().get_param('zuma_equipments.location_dest_id')
        if not location_id or not location_dest_id:
            raise ValidationError(_("Please add locations in Settings > Inventory > Warehouse."))
        partner = self.env.context.get('partner_id', False)
        partner_id = self.env['res.partner'].search([('id', '=', partner)])
        if not partner_id:
            raise ValidationError(_("Please add customer in order to create a lot."))
        if partner_id:
            if partner_id.parent_id:
                partner_id = partner_id.parent_id

        ref = self.env.context.get('reference', '')
        company_id = lot_id.company_id.id
        move_line = self.env['stock.move.line'].create({
            'product_id': lot_id.product_id.id,
            'location_id': int(location_id),
            'location_dest_id': int(location_dest_id),
            'qty_done': 1,
            'lot_id': lot_id.id,
            'date': lot_id.create_date,
            'origin': ref,
            'owner_id': partner_id.id,
            'company_id': company_id,
            'product_uom_category_id': lot_id.product_id.uom_id.category_id.id,
            'product_uom_id': lot_id.product_id.uom_id.id
        })
        move_vals = move_line._prepare_stock_move_vals()
        move_vals['company_id'] = company_id
        move_vals['location_id'] = int(location_id)
        move_vals['location_dest_id'] = int(location_dest_id)
        new_move = self.env['stock.move'].create(move_vals)
        move_line.move_id = new_move.id
        move_line._action_done()