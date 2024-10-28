# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import api, models


class LeaveReportCalendar(models.Model):
    _inherit = "hr.leave.report.calendar"

    @api.model
    def _gantt_unavailability(self, field, res_ids, start, stop, scale):
        return self.env['hr.leave']._gantt_unavailability(field, res_ids, start, stop, scale)
