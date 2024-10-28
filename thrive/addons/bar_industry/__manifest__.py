{
    'name': 'Bar & Pub',
    'version': '1.0',
    'category': 'Hospitality',
    'description': """
        This module offers a vibrant selection of cocktails, soft drinks, and other essential items for the bar and pub industry. It is an invaluable resource for anyone looking to elevate their establishment, enhance customer experience, or explore new trends in mixology and hospitality.
""",
    'depends': [
        'account_followup',
        'hr_hourly_cost',
        'hr_skills',
        'knowledge',
        'loyalty',
        'planning',
        'point_of_sale',
        'pos_restaurant',
        'pos_self_order',
        'project_enterprise',
        'purchase_stock',
        'stock_account',
    ],
    'data': [
        'data/res_config_settings.xml',
        'data/ir_attachment_pre.xml',
        'data/project_task_type.xml',
        'data/project_project.xml',
        'data/planning_role.xml',
        'data/product_pricelist.xml',
        'data/product_product.xml',
        'data/product_packaging.xml',
        'data/knowledge_cover.xml',
        'data/knowledge_article.xml',
        'data/knowledge_article_favorite.xml',
        'data/mail_message.xml',
        'data/knowledge_tour.xml',
    ],
    'demo': [
        'demo/pos_config.xml',
        'demo/product_product.xml',
        'demo/res_partner.xml',
        'demo/hr_employee.xml',
        'demo/product_supplierinfo.xml',
        'demo/project_task.xml',
        'demo/stock_warehouse_orderpoint.xml',
        'demo/purchase_order.xml',
        'demo/purchase_order_line.xml',
        'demo/purchase_order_confirm.xml',
        'demo/planning_recurrency.xml',
        'demo/planning_slot.xml',
    ],
    'license': 'OPL-1',
    'assets': {
        'web.assets_backend': [
            'bar_industry/static/src/js/my_tour.js',
        ]
    },
    'author': 'Thrive S.A.',
    "cloc_exclude": [
        "data/knowledge_article.xml",
        "static/src/js/my_tour.js",
    ],
    'images': ['images/main.png'],
}
