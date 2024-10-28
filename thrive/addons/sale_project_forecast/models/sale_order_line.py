# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _planning_slot_values(self):
        return {
            **super()._planning_slot_values(),
            'project_id': self.project_id.id or self.task_id.project_id.id,
        }
