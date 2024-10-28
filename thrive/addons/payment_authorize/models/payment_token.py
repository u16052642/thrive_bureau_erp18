# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

import logging
import pprint

from thrive import _, fields, models
from thrive.exceptions import UserError

from .authorize_request import AuthorizeAPI

_logger = logging.getLogger(__name__)


class PaymentToken(models.Model):
    _inherit = 'payment.token'

    authorize_profile = fields.Char(
        string="Authorize.Net Profile ID",
        help="The unique reference for the partner/token combination in the Authorize.net backend.")
