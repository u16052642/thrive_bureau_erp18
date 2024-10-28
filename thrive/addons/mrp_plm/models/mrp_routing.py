# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import models


class MrpRoutingWorkcenter(models.Model):
    _inherit = 'mrp.routing.workcenter'

    def _get_sync_values(self):
        if not self:
            return tuple()
        self.ensure_one()
        return tuple([self.name, self.workcenter_id] + self.bom_product_template_attribute_value_ids.ids)
