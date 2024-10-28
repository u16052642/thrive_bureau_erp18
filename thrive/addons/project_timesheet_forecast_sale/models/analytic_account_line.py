# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import models

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    def write(self, vals):
        res = super().write(vals)
        if ('validated' in vals or 'unit_amount' in vals):
            timesheets = self.filtered(lambda aal: aal.so_line and aal.project_id)
            if timesheets:
                timesheets.so_line._post_process_planning_sale_line()
        return res
