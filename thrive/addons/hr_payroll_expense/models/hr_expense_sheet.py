# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models, _
from thrive.exceptions import UserError


class HrExpenseSheet(models.Model):
    _inherit = "hr.expense.sheet"

    refund_in_payslip = fields.Boolean(
        string="Reimburse In Next Payslip",
        groups='hr_expense.group_hr_expense_team_approver,account.group_account_invoice,hr_contract.group_hr_contract_employee_manager')
    payslip_id = fields.Many2one('hr.payslip', string="Payslip", readonly=True)

    def _compute_is_editable(self):
        """ Add the condition that an expense sheet is not editable if it is linked to a payslip."""
        # EXTENDS hr_expense
        super()._compute_is_editable()
        for sheet in self:
            sheet.is_editable = sheet.is_editable and not sheet.payslip_id

    def action_reset_expense_sheets(self):
        # EXTENDS hr_expense
        if any(slip.state in {'done', 'paid'} for slip in self.payslip_id):
            raise UserError(_(
                "You cannot remove an expense from a payslip that has already been validated.\n"
                "Expenses can only be removed from draft or canceled payslips."
            ))
        self.action_remove_from_payslip()
        res = super().action_reset_expense_sheets()
        self.refund_in_payslip = False
        return res

    def action_report_in_next_payslip(self):
        """ Allow the report to be included in the next employee payslip computation. """
        if not self:
            raise UserError(_("There are no valid expense sheets selected."))
        if self.filtered(lambda sheet: sheet.state != 'approve' or sheet.payment_mode != 'own_account'):
            raise UserError(_("Only approved expense reports that were paid by an employee can be reimbursed in a payslip."))
        if any(self.account_move_ids.filtered(lambda move: move.state != 'draft')):
            raise UserError(_(
                "The state of the accounting entries linked to this expense report do not allow it to be reimbursed through a payslip."
            ))

        # Do not raise if already reported, just ignore it
        to_report = self.filtered(lambda sheet: not sheet.refund_in_payslip)
        to_report.refund_in_payslip = True
        for record in to_report:
            record.message_post(
                body=_('Expense report ("%(name)s") will be added to the next payslip.', name=record.name),
                partner_ids=record.employee_id.user_id.partner_id.ids,
                email_layout_xmlid='mail.mail_notification_light',
                subtype_id=self.env['ir.model.data']._xmlid_to_res_id('mail.mt_note'),
            )

    def action_remove_from_payslip(self):
        """
            Disallow the report to be included to the next employee payslip computation and/or unlink it from its payslip if possible.
        """
        valid_sheets = self.filtered(
            lambda sheet: not sheet.payslip_id or (not sheet.payslip_id.move_id and sheet.payslip_id.state in {'draft', 'cancel'})
        )
        # Don't raise in case of batch action for smooth flow
        if not valid_sheets:
            raise UserError(_(
                "You cannot remove an expense from a payslip that has already been validated.\n"
                "Expenses can only be removed from draft or canceled payslips."
            ))
        previous_payslips = valid_sheets.payslip_id
        # Only edit & post message when really needed
        sheets_to_edit = valid_sheets.filtered(lambda sheet: sheet.payslip_id or sheet.refund_in_payslip)
        for sheet in sheets_to_edit:
            sheet.message_post(
                body=_('Expense report ("%(name)s") was removed from the next payslip.', name=sheet.name),
                partner_ids=sheet.employee_id.user_id.partner_id.ids,
                email_layout_xmlid='mail.mail_notification_light',
                subtype_id=sheet.env['ir.model.data']._xmlid_to_res_id('mail.mt_note'),
            )
        sheets_to_edit.write({'refund_in_payslip': False, 'payslip_id': False})
        if previous_payslips:
            # Remove the sheets amounts from the payslips
            previous_payslips._update_expense_input_line_ids()

    def action_open_payslip(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Payslip'),
            'res_model': 'hr.payslip',
            'view_mode': 'form',
            'res_id': self.payslip_id.id,
        }