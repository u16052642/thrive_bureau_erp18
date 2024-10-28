# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models
from thrive.tools import SQL


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    team_id = fields.Many2one(comodel_name='crm.team', string="Sales Team")

    def _select(self) -> SQL:
        return SQL("%s, move.team_id as team_id", super()._select())
