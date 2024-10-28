# -*- coding:utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import models, fields


class HrPayrollStructureType(models.Model):
    _inherit = 'hr.payroll.structure.type'
    _description = 'Salary Structure Type'

    salary_benefits_ids = fields.One2many('hr.contract.salary.benefit', 'structure_type_id')
