# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.
{
    'name': 'New Zealand - Accounting',
    'icon': '/account/static/description/l10n.png',
    'countries': ['nz'],
    'version': '1.1',
    'category': 'Accounting/Localizations/Account Charts',
    'description': """
New Zealand Accounting Module
=============================

New Zealand accounting basic charts and localizations.

Also:
    - activates a number of regional currencies.
    - sets up New Zealand taxes.
    """,
    'author': 'Thrive Bureau ERP, Richard deMeester - Willow IT',
    'website': 'https://www.thrivebureau.com/documentation/master/applications/finance/fiscal_localizations.html',
    'depends': [
        'account',
    ],
    'auto_install': ['account'],
    'data': [
        'data/account_tax_report_data.xml',
        'data/res_currency_data.xml',
        'views/report_invoice.xml',
        'views/res_company_views.xml',
        'views/res_partner_views.xml',
    ],
    'demo': [
        'demo/demo_company.xml',
    ],
    'license': 'LGPL-3',
}
