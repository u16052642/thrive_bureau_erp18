# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive.tests import HttpCase, tagged, users


@tagged('post_install', '-at_install')
class AppointmentCrmLeadPropagationTest(HttpCase):

    @users('admin')
    def test_tour_default_opportunity_propagation(self):
        """ Test that the opportunity is correctly propagated to the appointment invitation created """
        self.env.user.tz = "Europe/Brussels"
        opportunity = self.env['crm.lead'].create({
            'name': 'Test Opportunity'
        })
        appointment_type = self.env['appointment.type'].create({'name': "Test AppointmentCRM"})
        self.start_tour('/thrive', 'appointment_crm_meeting_tour', login='admin')
        appointment_invite = self.env['appointment.invite'].search([('appointment_type_ids', 'in', appointment_type.ids)])
        self.assertTrue(appointment_invite.opportunity_id == opportunity)
