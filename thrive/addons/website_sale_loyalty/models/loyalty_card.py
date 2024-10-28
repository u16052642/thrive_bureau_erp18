# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import models

class LoyaltyCard(models.Model):
    _inherit = 'loyalty.card'

    def action_coupon_share(self):
        self.ensure_one()
        return self.env['coupon.share'].create_share_action(coupon=self)
