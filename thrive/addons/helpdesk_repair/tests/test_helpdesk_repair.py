# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive.tests import Form
from thrive.addons.helpdesk.tests.common import HelpdeskCommon


class TestRepair(HelpdeskCommon):
    def test_lot_id(self):
        """ This test purpose is to ensure that, if present, the context key default_lot_id is not
        propagated to the action_repair_done(). """
        self.env.ref('base.group_user').implied_ids = [(4, self.env.ref('stock.group_production_lot').id)]

        company = self.env.company
        product = self.env['product.product'].create({'name': 'Product'})
        product_lot = self.env['stock.lot'].create({
            'product_id': product.id,
        })
        component = self.env['product.product'].create({'name': 'Component'})

        ro_form = Form(self.env['repair.order'].with_context(default_lot_id=product_lot.id))
        ro_form.product_id = product
        ro_form.partner_id = company.partner_id
        with ro_form.move_ids.new() as ro_line:
            ro_line.product_id = component

        repair_order = ro_form.save()
        repair_order.action_validate()
        repair_order.action_repair_start()
        repair_order.action_repair_end()

    def test_helpdesk_repair(self):
        self.test_team.use_product_repairs = True

        product = self.env['product.product'].create({'name': 'Product'})

        ticket = self.env['helpdesk.ticket'].create({
            'name': 'test',
            'partner_id': self.partner.id,
            'team_id': self.test_team.id,
        })

        ro_form = Form(self.env['repair.order'].with_context(default_ticket_id=ticket.id))
        ro_form.product_id = product

        repair_order = ro_form.save()
        repair_order._action_repair_confirm()

        self.assertEqual(ticket.repairs_count, 1, 'The ticket should be linked to a return')
        self.assertEqual(repair_order.id, ticket.repair_ids[0].id, 'The correct return should be referenced in the ticket')

        repair_order.action_repair_start()
        repair_order.action_repair_end()

        last_message = str(ticket.message_ids[0].body)

        self.assertTrue(repair_order.display_name in last_message and 'Repair' in last_message,
            'Repair validation should be logged on the ticket')

    def test_helpdesk_return_and_repair(self):
        self.test_team.use_product_returns = True
        self.test_team.use_product_repairs = True

        product = self.env['product.product'].create({
            'name': 'product 1',
            'is_storable': True,
            'invoice_policy': 'order',
        })
        so = self.env['sale.order'].create({
            'partner_id': self.partner.id,
        })
        self.env['sale.order.line'].create({
            'product_id': product.id,
            'price_unit': 10,
            'product_uom_qty': 1,
            'order_id': so.id,
        })
        so.action_confirm()
        delivery = so.picking_ids
        delivery.move_ids.quantity = 1
        delivery.move_ids.picked = True
        delivery.button_validate()

        ticket = self.env['helpdesk.ticket'].create({
            'name': 'test',
            'partner_id': self.partner.id,
            'team_id': self.test_team.id,
            'sale_order_id': so.id,
        })
        stock_picking_form = Form(self.env['stock.return.picking'].with_context({
            'active_model': 'helpdesk.ticket',
            'default_ticket_id': ticket.id
        }))

        stock_picking_form.picking_id = delivery
        wizzard = stock_picking_form.save()
        wizzard.product_return_moves.write({'quantity': 1.0})
        res = wizzard.action_create_returns()
        return_picking = self.env['stock.picking'].browse(res['res_id'])
        return_picking.move_ids.quantity = 1
        return_picking.move_ids.picked = True
        return_picking.button_validate()

        ro_form = Form(self.env['repair.order'].with_context(
            active_model='helpdesk.ticket', default_ticket_id=ticket.id, default_picking_id=delivery.id
        ))
        ro_form.product_id = product
        ro_form.partner_id = self.partner
        repair_order = ro_form.save()
        repair_order.action_validate()
        repair_order.action_repair_start()
        repair_order.action_repair_end()

        self.assertRecordValues(delivery.move_ids, [{'product_id': product.id, 'quantity': 1.0}])