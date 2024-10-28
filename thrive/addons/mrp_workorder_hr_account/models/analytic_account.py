# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models


class AccountAnalyticAccountLine(models.Model):
    _inherit = 'account.analytic.line'

    employee_id = fields.Many2one('hr.employee', "Employee")
