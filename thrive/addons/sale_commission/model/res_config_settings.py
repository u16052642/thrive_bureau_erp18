# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_commission_forecast = fields.Boolean("Achievement Forecast", implied_group='sale_commission.group_commission_forecast')
