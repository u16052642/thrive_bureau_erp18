# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import api, fields, models, _
from thrive.exceptions import ValidationError


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    partena_code = fields.Char("Partena code", groups="hr.group_hr_user")

    @api.constrains('partena_code')
    def _check_partena_code(self):
        if any(employee.partena_code and len(employee.partena_code) != 6 for employee in self):
            raise ValidationError(_('The Partena number should have 6 characters!'))
