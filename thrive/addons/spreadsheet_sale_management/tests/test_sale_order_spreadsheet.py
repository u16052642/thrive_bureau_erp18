# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

import json

from thrive.tests.common import TransactionCase


class SaleOrderSpreadsheet(TransactionCase):

    def test_create_spreadsheet(self):
        spreadsheet = self.env["sale.order.spreadsheet"].create({"name": "spreadsheet"})
        data = spreadsheet.join_spreadsheet_session()["data"]
        self.assertTrue(data["lists"])
        self.assertTrue(data["globalFilters"])
        revision = spreadsheet.spreadsheet_revision_ids
        self.assertEqual(len(revision), 1)
        commands = json.loads(revision.commands)["commands"]
        self.assertEqual(commands[0]["type"], "RE_INSERT_THRIVE_LIST")
        self.assertEqual(commands[1]["type"], "CREATE_TABLE")

    def test_sale_order_action_open(self):
        spreadsheet = self.env["sale.order.spreadsheet"].create({"name": "spreadsheet"})
        quotation_template = self.env["sale.order.template"].create({
            "name": "Test template",
            "spreadsheet_template_id": spreadsheet.id
        })
        sale_order = self.env["sale.order"].create({
            "partner_id": self.env.user.partner_id.id,
            "sale_order_template_id": quotation_template.id
        })
        self.assertFalse(sale_order.spreadsheet_ids)
        action = sale_order.action_open_sale_order_spreadsheet()
        self.assertEqual(action["tag"], "action_sale_order_spreadsheet")
        self.assertTrue(sale_order.spreadsheet_ids)
        self.assertEqual(sale_order.spreadsheet_ids.id, action["params"]["spreadsheet_id"])

    def test_sale_order_action_open_twice(self):
        spreadsheet = self.env["sale.order.spreadsheet"].create({"name": "spreadsheet"})
        quotation_template = self.env["sale.order.template"].create({
            "name": "Test template",
            "spreadsheet_template_id": spreadsheet.id
        })
        sale_order = self.env["sale.order"].create({
            "partner_id": self.env.user.partner_id.id,
            "sale_order_template_id": quotation_template.id
        })
        sale_order.action_open_sale_order_spreadsheet()
        spreadsheet = sale_order.spreadsheet_ids
        sale_order.action_open_sale_order_spreadsheet()
        self.assertEqual(sale_order.spreadsheet_ids, spreadsheet, "it should be the same spreadsheet")