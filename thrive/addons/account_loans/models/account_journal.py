from thrive import models, fields


class AccountJournal(models.Model):
    _inherit = "account.journal"

    loan_properties_definition = fields.PropertiesDefinition('Model Properties')
