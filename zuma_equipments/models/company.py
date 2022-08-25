from odoo import fields, models, api


class ResCompany(models.Model):
    """
        Inherit Class add custom field
    """
    _inherit = 'res.company'

    show_equipment_button = fields.Boolean('Show Equipment Button', default=True, help="Show Equipment Button on Contact")
    internal_location_ids = fields.Many2many('stock.location', string="Stock Internal Locations", )
