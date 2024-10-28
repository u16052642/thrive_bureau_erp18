{
    'name': 'Fitness Center',
    'version': '1.0',
    'category': 'Health and Fitness',
    'description': "",
    'depends': [
        'calendar',
        'contacts',
        'hr',
        'knowledge',
        'maintenance',
        'planning',
        'pos_sale',
        'purchase',
        'sale_project',
        'sale_subscription',
        'web_studio',
        'website_appointment',
        'website_sale',
    ],
    'data': [
        'data/res_config_settings.xml',
        'data/ir_attachment_pre.xml',
        'data/product_category.xml',
        'data/pos_category.xml',
        'data/product_pricelist.xml',
        'data/sale_subscription.xml',
        'data/project_task_type.xml',
        'data/project_project.xml',
        'data/project_task.xml',
        'data/product_product.xml',
        'data/pos_payment_method.xml',
        'data/pos_config.xml',
        'data/knowledge_cover.xml',
        'data/knowledge_article.xml',
        'data/knowledge_article_favorite.xml',
        'data/mail_message.xml',
        'data/appointment_resource.xml',
        'data/appointment_type.xml',
        'data/maintenance_equipment.xml',
        'data/appointment_view.xml',
        'data/planning_role.xml',
        'data/ir_actions_server.xml',
        'data/base_automation.xml',
        'data/ir_model_data.xml',
        'data/knowledge_tour.xml',
    ],
    'demo': [
        'demo/website.xml',
        'demo/res_partner.xml',
        'demo/hr_employee.xml',
        'demo/appointment_type.xml',
        'demo/calendar_event.xml',
        'demo/maintenance_request.xml',
        'demo/product_product.xml',
        'demo/product_supplierinfo.xml',
        'demo/purchase_order.xml',
        'demo/purchase_order_line.xml',
        'demo/purchase_order_post.xml',
        'demo/sale_order.xml',
        'demo/sale_order_line.xml',
        'demo/sale_order_post.xml',
        'demo/planning_recurrency.xml',
        'demo/planning_slot.xml',
        'demo/website_ir_attachment.xml',
        'demo/website_view.xml',
        'demo/website_theme_apply.xml',
        'demo/website_page.xml',
        'demo/website_menu.xml',
        'demo/product_pricelist.xml',
        'demo/payment_provider_demo_post.xml',
    ],
    'license': 'OPL-1',
    'assets': {
        'web.assets_backend': [
            'fitness/static/src/js/my_tour.js',
        ]
    },
    'author': 'Thrive S.A.',
    "cloc_exclude": [
        "data/knowledge_article.xml",
        "static/src/js/my_tour.js",
    ],
    'images': ['images/main.png'],
}
