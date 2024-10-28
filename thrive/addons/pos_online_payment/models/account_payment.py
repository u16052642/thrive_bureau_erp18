# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import _, fields, models


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    pos_order_id = fields.Many2one('pos.order', string='POS Order', help='The Point of Sale order linked to this payment', readonly=True)

    def action_view_pos_order(self):
        """ Return the action for the view of the pos order linked to the payment.
        """
        self.ensure_one()

        action = {
            'name': _("POS Order"),
            'type': 'ir.actions.act_window',
            'res_model': 'pos.order',
            'target': 'current',
            'res_id': self.pos_order_id.id,
            'view_mode': 'form'
        }
        return action
