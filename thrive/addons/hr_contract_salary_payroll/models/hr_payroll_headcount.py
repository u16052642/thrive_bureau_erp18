# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models


class HrPayrollHeadcountLine(models.Model):
    _inherit = 'hr.payroll.headcount.line'

    employer_cost = fields.Monetary(related='contract_id.monthly_yearly_costs', string='Employer Cost')
