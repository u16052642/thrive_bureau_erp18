# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models


class HrContract(models.Model):
    _inherit = 'hr.contract'

    l10n_au_report_to_w3 = fields.Boolean('Report in BAS - W3', help="Report the PAYG withholding in W3 instead of W1 and W2.")
