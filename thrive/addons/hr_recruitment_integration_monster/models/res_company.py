# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    hr_recruitment_monster_username = fields.Char(string='Identifier', groups="base.group_system")
    hr_recruitment_monster_password = fields.Char(string='Password', groups="base.group_system")
