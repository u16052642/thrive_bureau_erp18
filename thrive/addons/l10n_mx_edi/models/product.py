# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models, api, _
from thrive.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    l10n_mx_edi_predial_account = fields.Char(string="Cuenta predial", size=150)

    @api.constrains('l10n_mx_edi_predial_account')
    def _check_l10n_mx_edi_predial_account(self):
        for record in self:
            if record.l10n_mx_edi_predial_account and not record.l10n_mx_edi_predial_account.isdigit():
                raise ValidationError(_("Cuenta predial must be only numbers!"))
