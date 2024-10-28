# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.
from thrive import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    l10n_cl_dte_email = fields.Char(string='DTE Email', help="Chile: Email used to send and receive electronic documents.")

    def _l10n_cl_is_foreign(self):
        return self.country_id.code != "CL"
