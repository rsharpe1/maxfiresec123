# -*- coding: utf-8 -*-
from odoo import models, fields, _
from odoo.exceptions import ValidationError


class ProductLotWizard(models.TransientModel):
    _name = 'product.lot.wizard'
    _description = 'Product and Lot Details Wizard'

    def default_get_categ_id(self):
        """ Get default product category from config parameters """
        categ_id = False
        product_categ_id = self.env['ir.config_parameter'].sudo().get_param('zuma_equipments.product_categ_id')
        if product_categ_id:
            categ_id = int(product_categ_id)
        else:
            product_categ_id = self.env['product.category'].sudo().search([('name', '=', 'All')], limit=1)
            if product_categ_id:
                categ_id = product_categ_id.id
        return categ_id

    helpdesk_ticket_id = fields.Many2one('helpdesk.ticket', string='Equipment')
    product_id = fields.Many2one('product.product', string='Equipment',
                                 domain=[('sale_ok', '=', False), ('purchase_ok', '=', False),
                                         ('type', '=', 'product'), ('tracking', '=', 'serial')], required=True)
    lot_name = fields.Char(string='Serial Number', required=True)
    product_categ_id = fields.Many2one('product.category', default=default_get_categ_id, string="Equipment Category")

    def action_create_product_lot_details(self):
        """
        Create Product Lot and write the product and created lot in active helpdesk Ticket,
        if button is clicked in helpdesk ticket. Else skip writing on helpdesk ticket.
        """
        if not self.lot_name:
            raise ValidationError(_("Please add name for the lot."))
        elif not self.product_id:
            raise ValidationError(_("Please add product for the lot."))
        else:
            vals = {
                'name': self.lot_name,
                'product_id': self.product_id.id,
                'company_id': self.env.company.id,
                'partner_id': self.env.context.get('partner_id'),
            }
            ref = ''
            if self.helpdesk_ticket_id:
                ref = self.helpdesk_ticket_id.name
            elif self.env.context.get('is_customer', ''):
                ref = self.env.context.get('is_customer', '')

            lot_id = self.env['stock.production.lot'].sudo().with_context(is_equipment=True, reference=ref).create(vals)

        if self.product_id and lot_id and self.helpdesk_ticket_id:
            self.helpdesk_ticket_id.sudo().write({'product_id': self.product_id, 'lot_id': lot_id.id})
