# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.
# Copyright (C) 2004-2008 PC Solutions (<http://pcsol.be>). All Rights Reserved
from thrive import fields, models, api, _
from thrive.exceptions import UserError


class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

    pos_session_id = fields.Many2one('pos.session', string="Session", copy=False)
