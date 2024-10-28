# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import _, api, fields, models
from thrive.exceptions import UserError

from thrive.addons.payment_demo import const


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('demo', 'Demo')], ondelete={'demo': 'set default'})

    #=== COMPUTE METHODS ===#

    def _compute_feature_support_fields(self):
        """ Override of `payment` to enable additional features. """
        super()._compute_feature_support_fields()
        self.filtered(lambda p: p.code == 'demo').update({
            'support_express_checkout': True,
            'support_manual_capture': 'partial',
            'support_refund': 'partial',
            'support_tokenization': True,
        })

    # === CONSTRAINT METHODS ===#

    @api.constrains('state', 'code')
    def _check_provider_state(self):
        if self.filtered(lambda p: p.code == 'demo' and p.state not in ('test', 'disabled')):
            raise UserError(_("Demo providers should never be enabled."))

    def _get_default_payment_method_codes(self):
        """ Override of `payment` to return the default payment method codes. """
        default_codes = super()._get_default_payment_method_codes()
        if self.code != 'demo':
            return default_codes
        return const.DEFAULT_PAYMENT_METHOD_CODES
