# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive.addons.mail.controllers import thread


class ThreadController(thread.ThreadController):

    def _get_allowed_message_post_params(self):
        return super()._get_allowed_message_post_params() | {"rating_value"}
