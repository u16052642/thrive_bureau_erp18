# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models


class Website(models.Model):
    _inherit = 'website'

    newsletter_id = fields.Many2one(string="Newsletter List", comodel_name='mailing.list')
