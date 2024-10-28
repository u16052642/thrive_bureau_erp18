# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models


class View(models.Model):
    _inherit = 'ir.ui.view'

    type = fields.Selection(selection_add=[('map', "Map")])

    def _get_view_info(self):
        return {'map': {'icon': 'fa fa-map-marker'}} | super()._get_view_info()
