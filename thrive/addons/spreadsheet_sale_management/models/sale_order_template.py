# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models


class SaleOrderTemplate(models.Model):
    _inherit = 'sale.order.template'

    spreadsheet_template_id = fields.Many2one(
        'sale.order.spreadsheet',
        string="Quote calculator",
        domain="[('order_id', '=', False), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    )
