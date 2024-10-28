# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import models


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    def _get_allowed_message_post_params(self):
        return super()._get_allowed_message_post_params() | {"rating_value"}
