# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import _, models
from thrive.exceptions import UserError


class ReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    def action_create_returns(self):
        for wizard in self:
            if wizard.company_id.account_fiscal_country_id.code == 'KE':
                if any(not l.to_refund and l.product_id.is_storable for l in wizard.product_return_moves):
                    raise UserError(_("You need to keep 'To Refund' checked as the KRA wants invoicing on delivery. "))
        return super().action_create_returns()
