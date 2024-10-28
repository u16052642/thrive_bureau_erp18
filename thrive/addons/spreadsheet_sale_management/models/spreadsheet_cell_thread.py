# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models


class SpreadsheetCellThread(models.Model):
    _inherit = 'spreadsheet.cell.thread'

    sale_order_spreadsheet_id = fields.Many2one(
        'sale.order.spreadsheet',
        readonly=True,
        ondelete='cascade',
    )

    def _get_spreadsheet_record(self):
        return super()._get_spreadsheet_record() or self.sale_order_spreadsheet_id
