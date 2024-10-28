# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import _, api, models
from thrive.exceptions import UserError


class AgedReceiableCustomHandler(models.AbstractModel):
    _inherit = "account.aged.receivable.report.handler"

    @api.model
    def action_print_report_statement_account(self, options, params):
        model, record_id = self.env['account.report']._get_model_info_from_id(params['line_id'])
        if model != 'res.partner':
            raise UserError(_("This option is only available for customers."))
        return self.env[model].browse(record_id).action_print_report_statement_account(options)
