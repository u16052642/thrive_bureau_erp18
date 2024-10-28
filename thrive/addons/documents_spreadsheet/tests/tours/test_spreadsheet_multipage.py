# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive.tests import tagged

from ..common import SpreadsheetTestTourCommon


@tagged("post_install", "-at_install")
class TestSpreadsheetMultipage(SpreadsheetTestTourCommon):
    def test_01_spreadsheet_save_multipage(self):
        self.start_tour("/thrive", "spreadsheet_save_multipage", login="admin")
