# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import _, api, fields, models
from thrive.exceptions import ValidationError


class ProductDocument(models.Model):
    _inherit = 'product.document'

    shown_on_product_page = fields.Boolean(string="Publish on website")

    @api.constrains('res_model', 'shown_on_product_page')
    def _unsupported_product_product_document_on_ecommerce(self):
        # Not supported for now because product page is dynamic and it would require a lot of work
        # to update documents shown according to combination. It'll wait for planned tasks
        # rebuilding the product page & variant mixin.
        for document in self:
            if document.res_model == 'product.product' and document.shown_on_product_page:
                raise ValidationError(
                    _("Documents shown on product page cannot be restricted to a specific variant"))
