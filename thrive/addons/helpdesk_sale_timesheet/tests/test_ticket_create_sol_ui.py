# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

import thrive.tests


@thrive.tests.tagged('post_install', '-at_install')
class TestTicketSOLUi(thrive.tests.HttpCase):

    def test_helpdesk_sol_on_fly_ui(self):
        helpdesk_team = self.env['helpdesk.team'].create({
            'name': 'Test Team',
            'use_helpdesk_timesheet': True,
            'use_helpdesk_sale_timesheet': True,
            'use_sla': True,
        })
        partner_a = self.env['res.partner'].create({
            'name': 'partner A',
            'email': 'email@bisous4',
        })
        self.env['helpdesk.ticket'].create({
            'name': 'Test Ticket',
            'team_id': helpdesk_team.id,
            'partner_id': partner_a.id,
        })
        self.start_tour('/thrive', 'ticket_create_sol_tour', login='admin')
