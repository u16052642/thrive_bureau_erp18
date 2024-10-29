{
    'name': 'Software Reseller',
    'version': '1.0',
    'category': 'Services',
    'description': """
This setup if for IT companies reselling software licenses, and consulting services.🚀
The typical sale is a 1 year Oracle Database license that is purchased to Oracle, and resold to client at a margin, with extra services to setup the database.
""",
    'depends': [
        'knowledge',
        'project',
        'sale_planning',
        'sale_purchase',
        'sale_subscription',
        'sale_timesheet',
        'web_studio',
    ],
    'data': [
        'data/ir_attachment_pre.xml',
        'data/ir_actions_act_window.xml',
        'data/ir_ui_menu.xml',
        'data/project_task_type.xml',
        'data/product_category.xml',
        'data/account_analytic_plan.xml',
        'data/account_analytic_account.xml',
        'data/project_project.xml',
        'data/uom_category.xml',
        'data/uom_uom.xml',
        'data/planning_role.xml',
        'data/product_product.xml',
        'data/sale_subscription_plan.xml',
        'data/sale_order_template.xml',
        'data/sale_order_template_line.xml',
        'data/knowledge_cover.xml',
        'data/knowledge_article.xml',
        'data/knowledge_article_favorite.xml',
        'data/mail_message.xml',
        'data/knowledge_tour.xml',
    ],
    'demo': [
        'demo/res_partner.xml',
        'demo/product_supplierinfo.xml',
        'demo/product_product.xml',
        'demo/sale_order.xml',
        'demo/sale_order_line.xml',
        'demo/sale_order_confirm.xml',
        'demo/project_task.xml',
        'demo/purchase_order_confirm.xml',
        'demo/planning_slot.xml',
    ],
    'license': 'OPL-1',
    'assets': {
        'web.assets_backend': [
            'software_reseller/static/src/js/my_tour.js',
        ]
    },
    'author': 'Thrive S.A.',
    "cloc_exclude": [
        "data/knowledge_article.xml",
        "static/src/js/my_tour.js",
    ],
    'images': ['images/main.png'],
}