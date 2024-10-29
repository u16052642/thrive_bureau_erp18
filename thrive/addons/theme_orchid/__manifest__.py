{
    'name': 'Orchid Theme',
    'description': 'Orchid Theme - Flowers, Beauty',
    'category': 'Theme/Retail',
    'summary': 'Florist, Gardens, Flowers, Nature, Green, Beauty, Stores',
    'sequence': 230,
    'version': '3.0.0',
    'depends': ['theme_common'],
    'data': [
        'data/generate_primary_template.xml',
        'data/ir_asset.xml',
        'views/images.xml',

        'views/snippets/s_cta_box.xml',
        'views/snippets/s_cover.xml',
        'views/snippets/s_cards_grid.xml',
        'views/snippets/s_striped_top.xml',
        'views/snippets/s_card_offset.xml',
        'views/snippets/s_text_image.xml',
        'views/snippets/s_title.xml',
        'views/snippets/s_motto.xml',
        'views/snippets/s_image_text.xml',
        'views/snippets/s_image_punchy.xml',
        'views/snippets/s_image_title.xml',
        'views/snippets/s_images_wall.xml',
        'views/snippets/s_images_mosaic.xml',
        'views/snippets/s_three_columns.xml',
        'views/snippets/s_image_text_overlap.xml',
        'views/snippets/s_quotes_carousel.xml',
        'views/snippets/s_carousel_intro.xml',
        'views/snippets/s_quotes_carousel_minimal.xml',
        'views/snippets/s_features_wall.xml',
        'views/snippets/s_call_to_action.xml',
        'views/snippets/s_freegrid.xml',
        'views/snippets/s_company_team_shapes.xml',
        'views/snippets/s_company_team_basic.xml',
        'views/snippets/s_numbers.xml',
        'views/snippets/s_pricelist_boxed.xml',
        'views/snippets/s_process_steps.xml',
        'views/snippets/s_media_list.xml',
        'views/snippets/s_framed_intro.xml',
        'views/snippets/s_product_catalog.xml',
        'views/snippets/s_unveil.xml',
        'views/snippets/s_quadrant.xml',
        'views/snippets/s_numbers_showcase.xml',
        'views/snippets/s_key_benefits.xml',
        'views/snippets/s_image_hexagonal.xml',
        'views/snippets/s_striped_center_top.xml',
        'views/snippets/s_key_images.xml',
        'views/snippets/s_kickoff.xml',
        'views/snippets/s_intro_pill.xml',
        'views/snippets/s_big_number.xml',
        'views/snippets/s_wavy_grid.xml',
        'views/snippets/s_shape_image.xml',
        'views/snippets/s_references.xml',
        'views/snippets/s_empowerment.xml',
        'views/new_page_template.xml',
    ],
    'images': [
        'static/description/orchid_description.jpg',
        'static/description/orchid_screenshot.jpg',
    ],
    'images_preview_theme': {
        'website.s_cover_default_image': '/theme_orchid/static/src/img/snippets/s_parallax.jpg',
    },
    'configurator_snippets': {
        'homepage': ['s_kickoff', 's_key_images', 's_process_steps', 's_freegrid', 's_image_text_overlap', 's_company_team_basic', 's_title', 's_images_wall', 's_references'],
    },
    'new_page_templates': {
        'about': {
            'personal': ['s_text_cover', 's_image_text', 's_text_block_h2', 's_numbers', 's_features', 's_call_to_action'],
        },
        'landing': {
            '1': ['s_banner', 's_features', 's_masonry_block', 's_call_to_action', 's_references', 's_quotes_carousel'],
            '2': ['s_cover', 's_text_image', 's_text_block_h2', 's_three_columns_landing_1', 's_call_to_action'],
            '3': ['s_text_cover', 's_text_block_h2', 's_three_columns', 's_showcase', 's_color_blocks_2', 's_quotes_carousel', 's_call_to_action'],
        },
        'services': {
            '2': ['s_text_cover', 's_image_text', 's_text_image', 's_image_text_2nd', 's_call_to_action'],
        },
    },
    'license': 'LGPL-3',
    'live_test_url': 'https://theme-orchid.thrivebureau.com',
    'assets': {
        'website.assets_editor': [
            'theme_orchid/static/src/js/tour.js',
        ],
    }
}