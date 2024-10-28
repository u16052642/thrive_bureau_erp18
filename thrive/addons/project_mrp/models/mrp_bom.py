# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    project_id = fields.Many2one('project.project')
