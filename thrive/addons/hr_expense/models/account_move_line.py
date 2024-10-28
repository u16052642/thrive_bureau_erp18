# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import api, fields, models
from thrive.tools import SQL
from thrive.tools.misc import frozendict


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    expense_id = fields.Many2one('hr.expense', string='Expense', copy=True) # copy=True, else we don't know price is tax incl.

    @api.constrains('account_id', 'display_type')
    def _check_payable_receivable(self):
        super(AccountMoveLine, self.filtered(lambda line: line.move_id.expense_sheet_id.payment_mode != 'company_account'))._check_payable_receivable()

    def _get_attachment_domains(self):
        attachment_domains = super(AccountMoveLine, self)._get_attachment_domains()
        if self.expense_id:
            attachment_domains.append([('res_model', '=', 'hr.expense'), ('res_id', '=', self.expense_id.id)])
        return attachment_domains

    def _compute_totals(self):
        expenses = self.filtered('expense_id')
        super(AccountMoveLine, expenses.with_context(force_price_include=True))._compute_totals()
        super(AccountMoveLine, self - expenses)._compute_totals()

    def _get_extra_query_base_tax_line_mapping(self) -> SQL:
        return SQL(' AND (base_line.expense_id IS NULL OR account_move_line.expense_id = base_line.expense_id)')
