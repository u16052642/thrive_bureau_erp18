# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models


class HolidaysType(models.Model):
    _inherit = "hr.leave.type"

    l10n_us_show_on_payslip = fields.Boolean(string="Show On Payslip", default=True)
