# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import api, models, _
from thrive.exceptions import UserError


class Tags(models.Model):
    _inherit = 'documents.tag'

    @api.ondelete(at_uninstall=False)
    def _unlink_except_contract_signature_tag(self):
        tag = self.env.ref('documents_hr_contract.document_tag_signature_request', raise_if_not_found=False)
        if tag and tag in self:
            raise UserError(_('You cannot delete this tag as it is used to link employee contracts and signatures.'))
