# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive.addons.base.models.ir_config_parameter import _default_parameters
from thrive.exceptions import ValidationError
from thrive.tests.common import TransactionCase


class TestIrConfigParameter(TransactionCase):

    def test_default_parameters(self):
        """ Check the behavior of _default_parameters
        when updating keys and deleting records. """
        for key in _default_parameters:
            config_parameter = self.env['ir.config_parameter'].search([('key', '=', key)], limit=1)
            with self.assertRaises(ValidationError):
                config_parameter.unlink()

            new_key = f"{key}_updated"
            with self.assertRaises(ValidationError):
                config_parameter.write({'key': new_key})
