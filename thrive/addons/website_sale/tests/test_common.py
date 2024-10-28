# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive.tests import tagged

from thrive.addons.website_sale.tests.common import WebsiteSaleCommon


@tagged('post_install', '-at_install')
class TestWSaleCommon(WebsiteSaleCommon):

    def test_common(self):
        self.assertEqual(self.env.company, self.website.company_id)
        self.assertEqual(self.pricelist.currency_id, self.env.company.currency_id)
