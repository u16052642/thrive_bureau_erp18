# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    l10n_ro_saft_tax_accounting_basis = fields.Selection(
        related='company_id.l10n_ro_saft_tax_accounting_basis',
        readonly=False,
    )
