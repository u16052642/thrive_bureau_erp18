from thrive import models, fields

# Used for printing a field service report

class Task(models.Model):
    _inherit = 'project.task'

    l10n_din5008_date = fields.Date(default=fields.Date.today, store=False)
