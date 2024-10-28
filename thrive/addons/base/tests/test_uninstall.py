# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

# This assumes an existing but uninitialized database.

from contextlib import contextmanager
import unittest

from thrive import api, SUPERUSER_ID
from thrive.tests import common
from thrive.tests.common import BaseCase

from thrive.modules.registry import Registry


@contextmanager
def environment():
    """ Return an environment with a new cursor for the current database; the
        cursor is committed and closed after the context block.
    """
    reg = Registry(common.get_db_name())
    with reg.cursor() as cr:
        yield api.Environment(cr, SUPERUSER_ID, {})


MODULE = 'test_uninstall'
MODEL = 'test_uninstall.model'


class TestUninstall(BaseCase):
    """
    Test the install/uninstall of a test module. The module is available in
    `thrive.tests` which should be present in the addons-path.
    """

    def test_01_install(self):
        """ Check a few things showing the module is installed. """
        with environment() as env:
            module = env['ir.module.module'].search([('name', '=', MODULE)])
            assert len(module) == 1
            module.button_install()
        Registry.new(common.get_db_name(), update_module=True)

        with environment() as env:
            self.assertIn('test_uninstall.model', env.registry)
            self.assertTrue(env['ir.model.data'].search([('module', '=', MODULE)]))
            self.assertTrue(env['ir.model.fields'].search([('model', '=', MODEL)]))

            env.cr.execute(
                r"""
                SELECT conname
                  FROM pg_constraint
                 WHERE conrelid = 'res_users'::regclass
                   AND conname LIKE 'res\_users\_test\_uninstall\_res\_user\_%'
                """
            )
            existing_constraints = [r[0] for r in env.cr.fetchall()]
            self.assertTrue(len(existing_constraints) == 4, existing_constraints)

    def test_02_uninstall(self):
        """ Check a few things showing the module is uninstalled. """
        with environment() as env:
            module = env['ir.module.module'].search([('name', '=', MODULE)])
            assert len(module) == 1
            module.button_uninstall()
        Registry.new(common.get_db_name(), update_module=True)

        with environment() as env:
            self.assertNotIn('test_uninstall.model', env.registry)
            self.assertFalse(env['ir.model.data'].search([('module', '=', MODULE)]))
            self.assertFalse(env['ir.model.fields'].search([('model', '=', MODEL)]))

            env.cr.execute(
                r"""
                SELECT conname
                  FROM pg_constraint
                 WHERE conrelid = 'res_users'::regclass
                   AND conname LIKE 'res\_users\_test\_uninstall\_res\_user\_%'
                """
            )
            remaining_constraints = [r[0] for r in env.cr.fetchall()]
            self.assertFalse(remaining_constraints)


if __name__ == '__main__':
    unittest.main()
