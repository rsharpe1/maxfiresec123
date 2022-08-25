# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details

from odoo import models


class CreateTask(models.TransientModel):
    _inherit = 'helpdesk.create.fsm.task'

    def action_generate_task(self):
        res = super(CreateTask, self).action_generate_task()
        if res:
            res.write({
                'product_id': self.helpdesk_ticket_id.product_id.id,
                'lot_id': self.helpdesk_ticket_id.lot_id
            })
        return res
