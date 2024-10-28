# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models


class IotDevice(models.Model):
    _inherit = 'iot.device'

    picking_type_ids = fields.Many2many('stock.picking.type', string="Operation Types", domain=[('code', '!=', 'mrp_operation'), ])
