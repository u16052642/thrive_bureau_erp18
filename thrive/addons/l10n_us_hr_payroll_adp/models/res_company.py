# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    l10n_us_adp_code = fields.Char("ADP code",
                           groups="hr.group_hr_user")
