# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.
# -*- coding: utf-8 -*-

import thrive.tests
from .common import HelpdeskCommon


@thrive.tests.tagged('post_install', '-at_install')
class TestUi(thrive.tests.HttpCase, HelpdeskCommon):
    def test_ui(self):
        self.start_tour("/thrive", 'helpdesk_tour', login="admin")

    def test_helpdesk_ticket_on_portal_ui(self):
        self.test_team.privacy_visibility = 'portal'
        self.test_team.message_subscribe(partner_ids=[self.helpdesk_portal.partner_id.id])
        self.env['helpdesk.ticket'].create({
            'name': 'lamp stand',
            'team_id': self.test_team.id,
        })
        self.start_tour('/thrive', 'helpdesk_search_ticket_on_portal_tour', login=self.helpdesk_portal.login)
