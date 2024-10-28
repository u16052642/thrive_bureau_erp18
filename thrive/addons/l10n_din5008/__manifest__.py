# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

{
    'name': 'DIN 5008',
    'version': '1.0',
    'category': 'Accounting/Localizations',
    'description': "This is the base module that defines the DIN 5008 standard in Thrive.",
    'depends': ['account'],
    'auto_install': True,
    'countries': ['de', 'ch'],
    'data': [
        'report/din5008_base_document_layout.xml',
        'report/din5008_report.xml',
        'data/report_layout.xml',
    ],
    'assets': {
        'web.report_assets_common': [
            'l10n_din5008/static/src/**/*',
        ],
    },
    'license': 'LGPL-3',
}
