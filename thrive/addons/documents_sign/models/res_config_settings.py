# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    documents_sign_folder_id = fields.Many2one(
        'documents.document', domain=[('type', '=', 'folder'), ('shortcut_document_id', '=', False)],
        related='company_id.documents_sign_folder_id', readonly=False, string="Sign Base Folder")
