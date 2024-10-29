# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.
{
    'name': 'Estonia - Accounting',
    'website': 'https://www.thrivebureau.com/documentation/master/applications/finance/fiscal_localizations.html',
    'version': '1.1',
    'icon': '/account/static/description/l10n.png',
    'countries': ['ee'],
    'category': 'Accounting/Localizations/Account Charts',
    'description': """
This is the base module to manage the accounting chart for Estonia in Thrive.
    """,
    'author': 'Thrive Bureau ERP',
    'depends': [
        'account',
    ],
    'auto_install': ['account'],
    'data': [
        'data/account_tax_report_data.xml',
        'views/account_tax_form.xml',
    ],
    'demo': [
        'demo/demo_company.xml',
    ],
    'license': 'LGPL-3',
}