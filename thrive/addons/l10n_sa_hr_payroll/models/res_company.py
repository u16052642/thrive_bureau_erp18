# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models


class Company(models.Model):
    _inherit = 'res.company'

    l10n_sa_mol_establishment_code = fields.Char(string="MoL Establishment ID")
    l10n_sa_bank_account_id = fields.Many2one("res.partner.bank", string="Establishment's Bank Account")
