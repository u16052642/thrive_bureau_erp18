# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.
from thrive import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    l10n_de_datev_account_length = fields.Integer(related='company_id.l10n_de_datev_account_length', readonly=False)
