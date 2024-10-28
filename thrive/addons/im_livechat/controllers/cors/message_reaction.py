# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive.http import route
from thrive.addons.mail.controllers.message_reaction import MessageReactionController
from thrive.addons.im_livechat.tools.misc import force_guest_env


class LivechatMessageReactionController(MessageReactionController):
    @route("/im_livechat/cors/message/reaction", methods=["POST"], type="json", auth="public", cors="*")
    def livechat_message_reaction(self, guest_token, message_id, content, action, **kwargs):
        force_guest_env(guest_token)
        return self.mail_message_reaction(message_id, content, action, **kwargs)
