# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.
{
    'name': 'Saudi Arabia - Accounting',
    'icon': '/account/static/description/l10n.png',
    'countries': ['sa'],
    'version': '2.0',
    'author': 'Thrive Bureau ERP, DVIT.ME (http://www.dvit.me)',
    'category': 'Accounting/Localizations/Account Charts',
    'description': """
Thrive Arabic localization for most Saudi Arabia.
""",
    'website': 'https://www.thrivebureau.com/documentation/master/applications/finance/fiscal_localizations/saudi_arabia.html',
    'depends': [
        'l10n_gcc_invoice',
        'account',
    ],
    'auto_install': ['account'],
    'data': [
        'data/account_data.xml',
        'data/account_tax_report_data.xml',
        'views/report_invoice.xml',
    ],
    'demo': [
        'demo/demo_company.xml',
    ],
    'license': 'LGPL-3',
}
