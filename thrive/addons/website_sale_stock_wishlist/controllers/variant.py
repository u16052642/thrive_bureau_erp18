# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive.http import request, route

from thrive.addons.website_sale.controllers.variant import WebsiteSaleVariantController


class WebsiteSaleStockWishlistVariantController(WebsiteSaleVariantController):

    @route()
    def get_combination_info_website(self, *args, **kwargs):
        request.update_context(website_sale_stock_wishlist_get_wish=True)
        return super().get_combination_info_website(*args, **kwargs)
