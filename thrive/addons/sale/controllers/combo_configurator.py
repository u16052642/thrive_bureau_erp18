# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from datetime import datetime

from thrive.http import Controller, request, route
from thrive.tools import groupby


class SaleComboConfiguratorController(Controller):

    @route('/sale/combo_configurator/get_data', type='json', auth='user')
    def sale_combo_configurator_get_data(
        self,
        product_tmpl_id,
        quantity,
        date,
        currency_id=None,
        company_id=None,
        pricelist_id=None,
        selected_combo_items=None,
        **kwargs,
    ):
        """ Return data about the specified combo product.

        :param int product_tmpl_id: The product for which to get data, as a `product.template` id.
        :param int quantity: The quantity of the product.
        :param str date: The date to use to compute prices.
        :param int|None currency_id: The currency to use to compute prices, as a `res.currency` id.
        :param int|None company_id: The company to use, as a `res.company` id.
        :param int|None pricelist_id: The pricelist to use to compute prices, as a
            `product.pricelist` id.
        :param list(dict) selected_combo_items: The selected combo items, in the following format:
            {
                'id': int,
                'no_variant_ptav_ids': list(int),
                'custom_ptavs': list({
                    'id': int,
                    'value': str,
                }),
            }
        :param dict kwargs: Locally unused data passed to `_get_combo_product_data` and
            `_get_combo_item_product_data`.
        :rtype: dict
        :return: A dict containing data about the combo product.
        """
        if company_id:
            request.update_context(allowed_company_ids=[company_id])
        product_template = request.env['product.template'].browse(product_tmpl_id)
        currency = request.env['res.currency'].browse(currency_id)
        pricelist = request.env['product.pricelist'].browse(pricelist_id)
        selected_combo_item_dict = {item['id']: item for item in selected_combo_items or []}

        return {
            **self._get_combo_product_data(
                product_template, quantity, date, currency, pricelist, **kwargs
            ),
            'combos': [{
                'id': combo.id,
                'name': combo.name,
                'combo_items': [{
                    'id': combo_item.id,
                    'extra_price': combo_item.extra_price,
                    'is_selected': combo_item.id in selected_combo_item_dict,
                    'product': self._get_combo_item_product_data(
                        combo_item.product_id,
                        selected_combo_item_dict.get(combo_item.id, {}),
                        **kwargs,
                    )
                } for combo_item in combo.combo_item_ids],
            } for combo in product_template.combo_ids.sudo()],
            'currency_id': currency_id,
        }

    @route('/sale/combo_configurator/get_price', type='json', auth='user')
    def sale_combo_configurator_get_price(
        self,
        product_tmpl_id,
        quantity,
        date,
        currency_id=None,
        company_id=None,
        pricelist_id=None,
        **kwargs,
    ):
        """ Return the price of the specified combo product.

        :param int product_tmpl_id: The product for which to get the price, as a `product.template`
            id.
        :param int quantity: The quantity of the product.
        :param str date: The date to use to compute the price.
        :param int|None currency_id: The currency to use to compute the price, as a `res.currency` id.
        :param int|None company_id: The company to use, as a `res.company` id.
        :param int|None pricelist_id: The pricelist to use to compute the price, as a
            `product.pricelist` id.
        :param dict kwargs: Locally unused data passed to `_get_product_price`.
        :rtype: float
        :return: The price of the combo product.
        """
        if company_id:
            request.update_context(allowed_company_ids=[company_id])
        product_template = request.env['product.template'].browse(product_tmpl_id)
        currency = request.env['res.currency'].browse(currency_id)
        pricelist = request.env['product.pricelist'].browse(pricelist_id)

        return self._get_combo_product_price(
            product_template, quantity, date, currency, pricelist, **kwargs
        )

    def _get_combo_product_data(
        self, product_template, quantity, date, currency, pricelist, **kwargs
    ):
        """ Return data about the specified combo product.

        :param product.template product_template: The product for which to get data.
        :param int quantity: The quantity of the product.
        :param str date: The date to use to compute prices.
        :param res.currency currency: The currency to use to compute prices.
        :param product.pricelist pricelist: The pricelist to use to compute prices.
        :param dict kwargs: Locally unused data passed to `_get_product_price`.
        :rtype: dict
        :return: A dict containing data about the specified product.
        """
        return {
            'product_tmpl_id': product_template.id,
            'display_name': product_template.display_name,
            'quantity': quantity,
            'price': self._get_combo_product_price(
                product_template, quantity, date, currency, pricelist, **kwargs
            ),
        }

    def _get_combo_product_price(
        self, product_template, quantity, date, currency, pricelist, **kwargs
    ):
        """ Return the specified combo product's price.

        :param product.template product_template: The product for which to get data.
        :param int quantity: The quantity of the product.
        :param str date: The date to use to compute prices.
        :param res.currency currency: The currency to use to compute prices.
        :param product.pricelist pricelist: The pricelist to use to compute prices.
        :param dict kwargs: Locally unused data passed to `_get_product_price`.
        :rtype: dict
        :return: The specified product's price.
        """
        return pricelist._get_product_price(
            product_template,
            quantity=quantity,
            currency=currency,
            date=datetime.fromisoformat(date),
            **kwargs,
        )

    def _get_combo_item_product_data(self, product, selected_combo_item, **kwargs):
        """ Return data about the specified combo item product.

        :param product.product product: The product for which to get data.
        :param dict selected_combo_item: The selected combo item, in the following format:
            {
                'id': int,
                'no_variant_ptav_ids': list(int),
                'custom_ptavs': list({
                    'id': int,
                    'value': str,
                }),
            }
        :param dict kwargs: Locally unused data passed to overrides.
        :rtype: dict
        :return: A dict containing data about the specified product.
        """
        return {
            'id': product.id,
            'product_tmpl_id': product.product_tmpl_id.id,
            'display_name': product.display_name,
            'ptals': self._get_ptals_data(product, selected_combo_item),
        }

    def _get_ptals_data(self, product, selected_combo_item):
        """ Return data about the PTALs of the specified product.

        :param product.product product: The product for which to get the PTALs.
        :param dict selected_combo_item: The selected combo item, in the following format:
            {
                'id': int,
                'no_variant_ptav_ids': list(int),
                'custom_ptavs': list({
                    'id': int,
                    'value': str,
                }),
            }
        :rtype: list(dict)
        :return: A list of dicts containing data about the specified product's PTALs.
        """
        variant_ptavs = product.product_template_attribute_value_ids
        no_variant_ptavs = request.env['product.template.attribute.value'].browse(
            selected_combo_item.get('no_variant_ptav_ids')
        )
        ptavs_by_ptal_id = dict(groupby(
            variant_ptavs + no_variant_ptavs, lambda ptav: ptav.attribute_line_id.id
        ))

        custom_ptavs = selected_combo_item.get('custom_ptavs', [])
        custom_value_by_ptav_id = {ptav['id']: ptav['value'] for ptav in custom_ptavs}

        return [{
            'id': ptal.id,
            'name': ptal.attribute_id.name,
            'create_variant': ptal.attribute_id.create_variant,
            'selected_ptavs': self._get_selected_ptavs_data(
                ptavs_by_ptal_id.get(ptal.id, []), custom_value_by_ptav_id
            ),
        } for ptal in product.attribute_line_ids]

    def _get_selected_ptavs_data(self, selected_ptavs, custom_value_by_ptav_id):
        """ Return data about the selected PTAVs of the specified product.

        :param list(product.template.attribute.value) selected_ptavs: The selected PTAVs.
        :param dict custom_value_by_ptav_id: A mapping from PTAV ids to custom values.
        :rtype: list(dict)
        :return: A list of dicts containing data about the specified PTAL's selected PTAVs.
        """
        return [{
            'id': ptav.id,
            'name': ptav.name,
            'price_extra': ptav.price_extra,
            'custom_value': custom_value_by_ptav_id.get(ptav.id),
        } for ptav in selected_ptavs]
