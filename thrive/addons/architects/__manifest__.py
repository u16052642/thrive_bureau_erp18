{
    'name': 'Architecture Firm',
    'version': '1.0',
    'category': 'Services',
    'description': """
This industry is made for Architecture Firm that sell all kind of architectural services such as feasibility studies,
schematic design, design development, worksite follow-up, energy efficiency assessment.
""",
    'depends': [
        'account_followup',
        'base_automation',
        'base_geolocalize',
        'crm_enterprise',
        'documents_hr',
        'documents_project_sale',
        'documents_spreadsheet',
        'knowledge',
        'sale_crm',
        'sale_expense',
        'sale_planning',
        'timesheet_grid',
        'web_studio',
        'website_crm',
        'website_partner',
        'theme_real_estate',
    ],
    'data': [
        'data/res_config_settings.xml',
        'data/crm_stage.xml',
        'data/base_automation.xml',
        'data/ir_actions_server.xml',
        'data/ir_attachment_pre.xml',
        'data/ir_model_fields.xml',
        'data/ir_ui_view.xml',
        'data/ir_actions_act_window.xml',
        'data/project_task_type.xml',
        'data/project_project.xml',
        'data/product_product.xml',
        'data/sale_order_template.xml',
        'data/sale_order_template_line.xml',
        'data/knowledge_cover.xml',
        'data/knowledge_article.xml',
        'data/knowledge_article_favorite.xml',
        'data/mail_message.xml',
        'data/website_view.xml',
        'data/website_theme_apply.xml',
        'data/ir_model_data.xml',
        'data/knowledge_tour.xml',
    ],
    'demo': [
        'demo/website.xml',
        'demo/res_partner.xml',
        'demo/crm_lead.xml',
        'demo/sale_order.xml',
        'demo/sale_order_line.xml',
        'demo/sale_order_confirm.xml',
        'demo/website_views.xml',
        'demo/website_theme_apply.xml',
        'demo/hr_expense.xml',
        'demo/hr_expense_action.xml',
    ],
    'license': 'OPL-1',
    'assets': {
        'web.assets_backend': [
            'architects/static/src/js/my_tour.js',
        ]
    },
    'author': 'Thrive S.A.',
    "cloc_exclude": [
        "data/knowledge_article.xml",
        "static/src/js/my_tour.js",
    ],
    'images': ['images/main.png'],
}
