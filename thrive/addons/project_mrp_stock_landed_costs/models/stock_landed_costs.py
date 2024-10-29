# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import models


class AdjustmentLines(models.Model):
    _inherit = 'stock.valuation.adjustment.lines'

    def _prepare_account_move_line_values(self):
        res = super()._prepare_account_move_line_values()
        if self.cost_id.target_model == 'manufacturing':
            res['analytic_distribution'] = self.move_id.production_id.project_id._get_analytic_distribution()
        return res