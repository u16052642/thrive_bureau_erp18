# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.
{
    'name': "Spreadsheet dashboard for stock",
    'category': 'Hidden',
    'summary': 'Spreadsheet',
    'description': 'Spreadsheet',
    'depends': ['spreadsheet_dashboard', 'stock_enterprise'],
    'data': [
        "data/dashboards.xml",
    ],
    'installable': True,
    'auto_install': ['stock_enterprise'],
    'license': 'OEEL-1',
}
