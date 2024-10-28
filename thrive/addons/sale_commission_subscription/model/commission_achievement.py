# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import models, fields


class CommissionAchievement(models.Model):
    _inherit = 'sale.commission.achievement'

    type = fields.Selection(selection_add=[('mrr', "MRR")], ondelete={'mrr': 'cascade'})
