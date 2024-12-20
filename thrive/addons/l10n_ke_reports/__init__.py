# -*- encoding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from . import models


def _l10n_ke_reports_post_init(env):
    for company in env['res.company'].search([('chart_template', '=', 'ke')]):
        ChartTemplate = env['account.chart.template'].with_company(company)
        ChartTemplate._load_data({
            'res.company': ChartTemplate._get_ke_reports_res_company(company.chart_template),
        })
