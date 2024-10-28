# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive.addons.account.tests.common import AccountTestInvoicingCommon
from thrive.tests.common import tagged, HttpCase


@tagged('post_install', '-at_install')
class TestUi(AccountTestInvoicingCommon, HttpCase):

    def test_01_sale_tour(self):
        self.env['res.partner'].create({'name': 'Agrolait', 'email': 'agro@lait.be'})
        self.start_tour("/thrive", 'sale_tour', login="admin", step_delay=100)
