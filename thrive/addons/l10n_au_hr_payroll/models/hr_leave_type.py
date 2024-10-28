# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models


class HolidaysType(models.Model):
    _inherit = "hr.leave.type"

    l10n_au_leave_type = fields.Selection(
        selection=[
            ("annual", "Annual"),
            ("long_service", "Long Service"),
            ("personal", "Personal Leave"),
        ],
        default="personal",
        required=True,
        string="Unused Leave Type"
    )
