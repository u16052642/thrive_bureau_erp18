# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from werkzeug.exceptions import NotFound

from thrive import http
from thrive.http import request
from thrive.addons.mail.models.discuss.mail_guest import add_guest_to_context
from thrive.addons.mail.tools.discuss import Store


class MessageReactionController(http.Controller):
    @http.route("/mail/message/reaction", methods=["POST"], type="json", auth="public")
    @add_guest_to_context
    def mail_message_reaction(self, message_id, content, action, **kwargs):
        message = request.env["mail.message"]._get_with_access(int(message_id), "create", **kwargs)
        if not message:
            raise NotFound()
        partner, guest = self._get_reaction_author(message, **kwargs)
        if not partner and not guest:
            raise NotFound()
        store = Store()
        # sudo: mail.message - access mail.message.reaction through an accessible message is allowed
        message.sudo()._message_reaction(content, action, partner, guest, store)
        return store.get_result()

    def _get_reaction_author(self, message, **kwargs):
        return request.env["res.partner"]._get_current_persona()
