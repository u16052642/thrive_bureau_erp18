# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    l10n_ke_nssf_number = fields.Char(string="NSSF Number", help="NSSF Number provided by the NSSF")
    l10n_ke_kra_pin = fields.Char(string="KRA PIN", help="KRA PIN provided by the KRA")
