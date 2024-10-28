{
    'name': 'Fossil Fuel Trading',
    'version': '1.0',
    'category': 'Supply Chain',
    'description': """
        The module specializes in trading coal and petroleum products, acquiring them from international
        suppliers or local vendors and reselling them to customers. They have a unique quality-checking
        method during the procurement process, defining specific parameters in the GRN and Delivery stages
        to ensure product quality.
    """,
    'depends': [
        'account_asset',
        'base_automation',
        'calendar',
        'knowledge',
        'purchase_product_matrix',
        'quality_control_worksheet',
        'sale_product_matrix',
        'stock_delivery',
        'stock_dropshipping',
        'stock_landed_costs',
        'web_studio',
    ],
    'data': [
        'data/res_config_settings.xml',
        'data/base_automation.xml',
        'data/ir_actions_server.xml',
        'data/ir_attachment_pre.xml',
        'data/ir_model.xml',
        'data/ir_model_fields.xml',
        'data/ir_ui_view.xml',
        'data/ir_actions_act_window.xml',
        'data/ir_model_access.xml',
        'data/ir_rule.xml',
        'data/product_category.xml',
        'data/worksheet_template.xml',
        'data/product_template.xml',
        'data/product_attribute.xml',
        'data/product_attribute_value.xml',
        'data/product_template_attribute_line.xml',
        'data/product_template_attribute_value.xml',
        'data/product_product.xml',
        'data/knowledge_cover.xml',
        'data/knowledge_article.xml',
        'data/knowledge_article_favorite.xml',
        'data/mail_message.xml',
        'data/quality_point.xml',
        'data/ir_model_data.xml',
        'data/knowledge_tour.xml',
    ],
    'demo': [
        'demo/res_partner.xml',
        'demo/product_supplierinfo.xml',
        'demo/stock_lot.xml',
        'demo/purchase_order.xml',
        'demo/purchase_order_line.xml',
        'demo/purchase_order_post.xml',
        'demo/sale_order.xml',
        'demo/sale_order_line.xml',
        'demo/sale_order_post.xml',
    ],
    'license': 'OPL-1',
    'assets': {
        'web.assets_backend': [
            'coal_petroleum/static/src/js/my_tour.js',
        ]
    },
    'author': 'Thrive S.A.',
    "cloc_exclude": [
        "data/knowledge_article.xml",
        "static/src/js/my_tour.js",
    ],
    'images': ['images/main.png'],
}
