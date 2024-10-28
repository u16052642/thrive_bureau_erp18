# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    wa_sale_template_id = fields.Many2one(related="website_id.wa_sale_template_id", readonly=False)
