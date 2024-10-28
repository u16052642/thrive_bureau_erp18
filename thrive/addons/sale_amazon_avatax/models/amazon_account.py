# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import models


class AmazonAccount(models.Model):
    _inherit = 'amazon.account'

    def _create_order_from_data(self, order_data):
        """ Override to avoid recomputing taxes for orders made through Amazon. """
        order = super()._create_order_from_data(order_data)
        if order.fiscal_position_id.is_avatax:
            order.fiscal_position_id = False
        return order
