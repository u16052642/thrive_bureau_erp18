# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

{
    'name': 'Turkey - Payroll with Accounting',
    'author': 'Thrive',
    'version': '1.0',
    'category': 'Human Resources',
    'description': """
Accounting Data for Turkey Payroll Rules
==========================================
    """,
    'depends': ['hr_payroll_account', 'l10n_tr', 'l10n_tr_hr_payroll'],
    'data': [
        'data/account_chart_template_data.xml',
    ],
    'demo': [
        'data/l10n_tr_hr_payroll_account_demo.xml',
    ],
    'license': 'OEEL-1',
    'auto_install': True,
}
