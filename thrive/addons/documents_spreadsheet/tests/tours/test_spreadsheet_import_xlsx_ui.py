# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

import base64

from thrive.tests import tagged
from thrive.tests.common import HttpCase
from thrive.tools import file_open


@tagged("post_install", "-at_install")
class TestSpreadsheetImportXLSXUi(HttpCase):
    def test_01_spreadsheet_clone_and_archive_xlsx(self):
        with file_open('documents_spreadsheet/tests/data/test.xlsx', 'rb') as f:
            spreadsheet_data = base64.encodebytes(f.read())

        folder = self.env["documents.document"].create({
            'name': 'Test folder',
            'type': 'folder',
            "is_pinned_folder": True,
            "access_internal": "view",
            "access_via_link": "none",
        })
        self.env['documents.document'].create({
            'datas': spreadsheet_data,
            'name': 'test.xlsx',
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'folder_id': folder.id
        })

        self.start_tour("/thrive", "spreadsheet_clone_xlsx", login="admin")
