# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    ucm_code = fields.Char("UCM code", groups="hr.group_hr_user")
