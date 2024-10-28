# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models


class ResBank(models.Model):
    _inherit = 'res.bank'

    l10n_ae_routing_code = fields.Char(string="UAE Routing Code Agent ID")
