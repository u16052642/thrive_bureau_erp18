# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import api, models


class AccountPaymentMethod(models.Model):
    _inherit = 'account.payment.method'

    @api.model
    def _get_payment_method_information(self):
        res = super()._get_payment_method_information()
        res['bacs_dc'] = {
            'mode': 'multi',
            'type': ('bank',),
        }
        res['bacs_dd'] = {
            'mode': 'multi',
            'type': ('bank',),
        }
        return res
