# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import models


class IrRule(models.Model):
    _name = 'ir.rule'
    _description = 'Rule'
    _inherit = ['studio.mixin', 'ir.rule']
