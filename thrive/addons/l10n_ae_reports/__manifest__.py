# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

{
    'name': 'United Arab Emirates - Accounting Reports',
    'countries': ['ae'],
    'version': '1.0',
    'category': 'Accounting/Localizations/Reporting',
    'description': """
        Accounting reports for the United Arab Emirates
    """,
    'depends': ['l10n_ae', 'account_reports'],
    'installable': True,
    'post_init_hook': '_l10n_ae_reports_post_init',
    'auto_install': ['l10n_ae', 'account_reports'],
    'website': 'https://www.thrivebureau.com/app/accounting',
    'license': 'OEEL-1',
}