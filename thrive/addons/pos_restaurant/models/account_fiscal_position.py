from thrive import models, api
from thrive.osv.expression import OR


class AccountFiscalPosition(models.Model):
    _inherit = 'account.fiscal.position'

    @api.model
    def _load_pos_data_domain(self, data):
        params = super()._load_pos_data_domain(data)
        params = OR([params, [('id', '=', data['pos.config']['data'][0]['takeaway_fp_id'])]])
        return params
