# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive.addons.phone_validation.tools import phone_validation
from thrive.addons.test_mail.tests.common import TestRecipients


class TestSMSRecipients(TestRecipients):

    @classmethod
    def setUpClass(cls):
        super(TestSMSRecipients, cls).setUpClass()
        cls.partner_numbers = [
            phone_validation.phone_format(partner.mobile, partner.country_id.code, partner.country_id.phone_code, force_format='E164')
            for partner in (cls.partner_1 | cls.partner_2)
        ]
