# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    candidate_properties_definition = fields.PropertiesDefinition('Candidate Properties')
    job_properties_definition = fields.PropertiesDefinition("Job Properties")
