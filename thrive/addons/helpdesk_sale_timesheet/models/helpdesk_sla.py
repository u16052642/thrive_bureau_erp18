# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models

class HelpdeskSLA(models.Model):
    _inherit = 'helpdesk.sla'

    product_ids = fields.Many2many('product.template',
        string="Services",
        domain="[('sale_ok', '=', True), ('type', '=', 'service')]",
    )
    use_helpdesk_sale_timesheet = fields.Boolean(related="team_id.use_helpdesk_sale_timesheet")