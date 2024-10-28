# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.
from . import controllers
from . import models
from . import wizard
from . import report


def uninstall_hook(env):
    env.ref("account.account_analytic_line_rule_billing_user").write({'domain_force': "[(1, '=', 1)]"})

def _sale_timesheet_post_init(env):
    products = env['product.template'].search([
        ('type', '=', 'service'),
        ('service_tracking', 'in', ['no', 'task_global_project', 'task_in_project', 'project_only']),
        ('invoice_policy', '=', 'order'),
        ('service_type', '=', 'manual'),
    ])

    for product in products:
        product.service_type = 'timesheet'
        product._compute_service_policy()
