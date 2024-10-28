# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta

from thrive import fields
from thrive.addons.event_product.tests.common import TestEventProductCommon
from thrive.addons.sales_team.tests.common import TestSalesCommon


class TestEventSaleCommon(TestEventProductCommon, TestSalesCommon):

    @classmethod
    def setUpClass(cls):
        super(TestEventSaleCommon, cls).setUpClass()

        cls.event_0 = cls.env['event.event'].create({
            'name': 'TestEvent',
            'date_begin': fields.Datetime.to_string(datetime.today() + timedelta(days=1)),
            'date_end': fields.Datetime.to_string(datetime.today() + timedelta(days=15)),
            'date_tz': 'Europe/Brussels',
        })
