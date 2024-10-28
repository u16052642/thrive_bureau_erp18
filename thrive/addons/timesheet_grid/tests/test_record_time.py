# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.
# -*- coding: utf-8 -*-

from thrive.tests import HttpCase, tagged

@tagged('-at_install', 'post_install')
class TestRecordTime(HttpCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.env['project.project'].create({
            'name': 'Test Project'
        })

    def test_record_time(self):
        self.start_tour('/thrive', 'timesheet_record_time', login='admin', timeout=100)
