# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

import thrive
import thrive.exceptions
from thrive.modules.registry import Registry


def check(db, uid, passwd):
    res_users = Registry(db)['res.users']
    return res_users.check(db, uid, passwd)

def compute_session_token(session, env):
    self = env['res.users'].browse(session.uid)
    return self._compute_session_token(session.sid)


def check_session(session, env, request=None):
    self = env['res.users'].browse(session.uid)
    expected = self._compute_session_token(session.sid)
    if expected and thrive.tools.misc.consteq(expected, session.session_token):
        if request:
            env['res.device.log']._update_device(request)
        return True
    return False
