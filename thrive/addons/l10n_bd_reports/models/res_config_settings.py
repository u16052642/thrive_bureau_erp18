# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    l10n_bd_corporate_tax_liability = fields.Many2one(
        related="company_id.l10n_bd_corporate_tax_liability",
        readonly=False,
    )
    l10n_bd_corporate_tax_expense = fields.Many2one(
        related="company_id.l10n_bd_corporate_tax_expense",
        readonly=False,
    )
