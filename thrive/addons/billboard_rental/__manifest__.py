{
    'name': 'Billboard Rental',
    'version': '1.0',
    'category': 'Services',
    'description': """
This industry caters to billboard rental businesses, specializing in managing outdoor advertising spaces. It involves coordinating prime location leases, complying with regulations, and maximizing client visibility.
""",
    'depends': [
        'hr',
        'industry_fsm',
        'knowledge',
        'project_sale_subscription',
        'sale_timesheet',
        'web_studio',
        'website_appointment',
        'website_crm',
        'worksheet',
    ],
    'data': [
        'data/res_config_settings.xml',
        'data/ir_model.xml',
        'data/ir_model_fields.xml',
        'data/ir_ui_view.xml',
        'data/ir_actions_act_window.xml',
        'data/ir_ui_menu.xml',
        'data/ir_model_access.xml',
        'data/ir_rule.xml',
        'data/worksheet_template.xml',
        'data/account_analytic_account.xml',
        'data/project_task_type.xml',
        'data/project_project.xml',
        'data/sale_subscription_pricing.xml',
        'data/product_product.xml',
        'data/sale_order_template.xml',
        'data/sale_order_template_line.xml',
        'data/crm_stage.xml',
        'data/website_view.xml',
        'data/website_theme_apply.xml',
        'data/knowledge_article.xml',
        'data/knowledge_article_favorite.xml',
        'data/mail_message.xml',
        'data/appointment_type.xml',
        'data/ir_model_data.xml',
        'data/knowledge_tour.xml',
    ],
    'demo': [
        'demo/website.xml',
        'demo/res_partner.xml',
        'demo/account_analytic_plan.xml',
        'demo/account_analytic_account.xml',
        'demo/appointment_type.xml',
        'demo/sale_order.xml',
        'demo/sale_order_line.xml',
        'demo/sale_order_post.xml',
        'demo/website_view.xml',
        'demo/website_theme_apply.xml',
    ],
    'license': 'OPL-1',
    'assets': {
        'web.assets_backend': [
            'billboard_rental/static/src/js/my_tour.js',
        ]
    },
    'author': 'Thrive S.A.',
    "cloc_exclude": [
        "data/knowledge_article.xml",
        "static/src/js/my_tour.js",
    ],
    'images': ['images/main.png'],
}