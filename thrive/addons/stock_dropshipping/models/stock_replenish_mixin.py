# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import models
from thrive.osv import expression


class ProductReplenishMixin(models.AbstractModel):
    _inherit = 'stock.replenish.mixin'

    def _get_allowed_route_domain(self):
        domains = super()._get_allowed_route_domain()
        return expression.AND([domains, [('id', '!=', self.env.ref('stock_dropshipping.route_drop_shipping', raise_if_not_found=False).id)]])
