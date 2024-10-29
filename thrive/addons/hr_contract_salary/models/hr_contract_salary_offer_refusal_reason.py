# -*- coding:utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models


class HrContractSalaryOffer(models.Model):
    _name = 'hr.contract.salary.offer.refusal.reason'
    _description = 'Salary Offer Refusal Reasons'
    _order = "sequence, id"

    name = fields.Char("Description")
    sequence = fields.Integer("Sequence")