# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import models


class Users(models.Model):
    _inherit = 'res.users'

    def get_totp_invite_url(self):
        if not self._is_internal():
            return '/my/security'
        else:
            return super(Users, self).get_totp_invite_url()
