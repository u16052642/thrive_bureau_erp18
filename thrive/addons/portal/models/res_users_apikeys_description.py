# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import models, _
from thrive.exceptions import AccessError


class APIKeyDescription(models.TransientModel):
    _inherit = 'res.users.apikeys.description'

    def check_access_make_key(self):
        try:
            return super().check_access_make_key()
        except AccessError:
            if self.env['ir.config_parameter'].sudo().get_param('portal.allow_api_keys'):
                if self.env.user._is_portal():
                    return
                else:
                    raise AccessError(_("Only internal and portal users can create API keys"))
            raise