# coding: utf-8

from thrive import fields, models


class ResCountryState(models.Model):
    _inherit = 'res.country.state'

    l10n_co_edi_code = fields.Integer("EDI State Code")
