# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.
from thrive import Command, fields
from thrive.tests import tagged
from thrive.addons.account.tests.common import AccountTestInvoicingHttpCommon


@tagged('post_install', '-at_install')
class TestTourAccountReports(AccountTestInvoicingHttpCommon):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        today = fields.Date.today()
        previous_year = fields.Date.from_string('%s-%s-01' % (today.year - 1, today.month))

        cls.out_invoice_current_year = cls.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': cls.partner_a.id,
            'invoice_date': today,
            'date': today,
            'invoice_line_ids': [
                Command.create({'name': 'line1', 'price_unit': 100.0}),
            ],
        })
        cls.out_invoice_current_year.action_post()

        cls.out_invoice_previous_year = cls.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': cls.partner_a.id,
            'invoice_date': previous_year,
            'date': previous_year,
            'invoice_line_ids': [
                Command.create({'name': 'line1', 'price_unit': 500.0}),
            ],
        })
        cls.out_invoice_previous_year.action_post()

    def test_tour_account_reports(self):
        self.start_tour("/thrive", 'account_reports_widgets', login=self.env.user.login)
