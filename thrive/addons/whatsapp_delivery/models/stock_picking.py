# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _get_whatsapp_safe_fields(self):
        return {'partner_id.name', 'name', 'company_id.name', 'carrier_tracking_url'}
