# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.
{
    'name': 'United Kingdom - Accounting',
    'icon': '/account/static/description/l10n.png',
    'countries': ['gb'],
    'version': '1.1',
    'category': 'Accounting/Localizations/Account Charts',
    'description': """
This is the latest UK Thrive localisation necessary to run Thrive accounting for UK SME's with:
=================================================================================================
    - a CT600-ready chart of accounts
    - VAT100-ready tax structure
    - InfoLogic UK counties listing
    - a few other adaptations""",
    'author': 'SmartMode LTD',
    'website': 'https://www.thrivebureau.com/documentation/master/applications/finance/fiscal_localizations/united_kingdom.html',
    'depends': [
        'account',
        'base_iban',
        'base_vat',
    ],
    'auto_install': ['account'],
    'data': [
        'data/l10n_uk_chart_data.xml',
        'data/account_tax_report_data.xml',
    ],
    'demo': [
        'demo/l10n_uk_demo.xml',
        'demo/demo_company.xml',
    ],
    'license': 'LGPL-3',
}
