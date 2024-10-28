# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    l10n_us_adp_code = fields.Char("ADP Code",
                           groups="hr.group_hr_user",
                           help="Usually a 6-digit code in ADP to identify your employees (File #).")
