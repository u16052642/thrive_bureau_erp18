{
    'name': 'Beverage Distributor',
    'version': '1.0',
    'category': 'Supply Chain',
    'description': "",
    'depends': [
        'base_automation',
        'calendar',
        'knowledge',
        'mrp',
        'pos_loyalty',
        'product_barcodelookup',
        'sale_crm',
        'sale_management',
        'sale_purchase',
        'sale_service',
        'web_studio',
        'website_crm',
        'website_sale',
        'website_sale_stock',
        'theme_bistro',
    ],
    'data': [
        'data/product_category.xml',
        'data/ir_attachment_pre.xml',
        'data/ir_model_fields.xml',
        'data/ir_ui_view.xml',
        'data/ir_actions_server.xml',
        'data/base_automation.xml',
        'data/ir_default.xml',
        'data/product_public_category.xml',
        'data/pos_category.xml',
        'data/account_tax.xml',
        'data/product_template.xml',
        'data/product_attribute.xml',
        'data/product_attribute_value.xml',
        'data/product_pricelist.xml',
        'data/product_template_attribute_line.xml',
        'data/product_template_attribute_value.xml',
        'data/product_product.xml',
        'data/product_template_package.xml',
        'data/ptal.xml',
        'data/knowledge_cover.xml',
        'data/knowledge_article.xml',
        'data/knowledge_article_favorite.xml',
        'data/mail_message.xml',
        'data/delivery_carrier.xml',
        'data/ir_attachment_post.xml',
        'data/pos_config.xml',
        'data/res_config_settings.xml',
        'data/knowledge_tour.xml',
    ],
    'demo': [
        'demo/website.xml',
        'demo/res_partner.xml',
        'demo/crm_lead.xml',
        'demo/product_template.xml',
        'demo/product_supplierinfo.xml',
        'demo/sale_order.xml',
        'demo/sale_order_line.xml',
        'demo/sale_order_confirm.xml',
        'demo/website_attachment.xml',
        'demo/website_view.xml',
        'demo/website_theme_apply.xml',
        'demo/website_page.xml',
        'demo/website_menu.xml',
        'demo/purchase_order.xml',
        'demo/purchase_order_line.xml',
        'demo/purchase_order_confirm.xml',
        'demo/validate_deliveries.xml',
        'demo/validate_receipts.xml',
        'demo/stock_quant.xml',
        'demo/mail_activity.xml',
        'demo/delivery_carrier.xml',
        'demo/payment_provider_demo_post.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'beverage_distributor/static/src/js/my_tour.js',
        ]
    },
    "cloc_exclude": [
        "data/knowledge_article.xml",
        "static/src/js/my_tour.js",
    ],
    'license': 'OPL-1',
    'author': 'Thrive S.A.',
    'images': ['images/main.png'],
}
