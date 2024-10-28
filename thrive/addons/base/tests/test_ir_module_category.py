# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.
from thrive.exceptions import ValidationError
from thrive.tests.common import TransactionCase

class TestModuleCategory(TransactionCase):

    def test_parent_circular_dependencies(self):
        Cats = self.env['ir.module.category']

        def create(name, **kw):
            return Cats.create(dict(kw, name=name))

        category_a = create('A', parent_id=False)
        category_b = create('B', parent_id=category_a.id)
        category_c = create('C', parent_id=category_b.id)

        with self.assertRaises(ValidationError):
            category_a.write({'parent_id': category_c.id})
        with self.assertRaises(ValidationError):
            category_b.write({'parent_id': category_b.id})
