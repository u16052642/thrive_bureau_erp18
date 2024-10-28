# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive.addons.sale_subscription.controllers.product_configurator import (
    SaleSubscriptionProductConfiguratorController
)
from thrive.addons.website_sale.controllers.product_configurator import (
    WebsiteSaleProductConfiguratorController
)


class WebsiteSaleSubscriptionProductConfiguratorController(
    WebsiteSaleProductConfiguratorController, SaleSubscriptionProductConfiguratorController
):
    """ Even though this class is empty, this declaration is needed to ensure that
    `_get_basic_product_information` is called in `SaleSubscriptionProductConfiguratorController`
    first (to compute the price), and in `WebsiteSaleProductConfiguratorController` second (to apply
    taxes to the price).
    """
