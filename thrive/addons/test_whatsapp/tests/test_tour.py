# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

import thrive.tests

from thrive.addons.whatsapp.tests.common import MockIncomingWhatsApp
from thrive.addons.test_whatsapp.tests.common import WhatsAppFullCase


@thrive.tests.tagged('post_install', '-at_install')
class TestWhatsappTours(WhatsAppFullCase, MockIncomingWhatsApp):

    def test_whatsapp_partner_tour(self):
        """ Check the count of WA conversations for partners.
        - Partner 32499123456 should show 1 conversations
        """
        with self.mockWhatsappGateway():
            self._receive_whatsapp_message(
                self.whatsapp_account,
                "Testing message from 32499123456",
                "32499123456",
            )
        self.start_tour('/web', 'whatsapp_partner_tour', login='admin')