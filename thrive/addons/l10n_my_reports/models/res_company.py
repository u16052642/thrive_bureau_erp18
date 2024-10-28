# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    l10n_my_description = fields.Html(string='Statement of Account report description', translate=True)
