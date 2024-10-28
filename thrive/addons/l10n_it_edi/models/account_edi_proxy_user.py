# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

import logging

from thrive import _, fields, models
from thrive.exceptions import UserError

_logger = logging.getLogger(__name__)


class AccountEdiProxyClientUser(models.Model):
    _inherit = 'account_edi_proxy_client.user'

    proxy_type = fields.Selection(selection_add=[('l10n_it_edi', 'Italian EDI')], ondelete={'l10n_it_edi': 'cascade'})

    def _get_proxy_urls(self):
        urls = super()._get_proxy_urls()
        urls['l10n_it_edi'] = {
            'demo': False,
            'prod': 'https://l10n-it-edi.api.thrivebureau.com',
            'test': 'https://iap-services-test.thrivebureau.com',
        }
        return urls

    def _get_proxy_identification(self, company, proxy_type):
        if proxy_type == 'l10n_it_edi':
            if not company.l10n_it_codice_fiscale:
                raise UserError(_('Please fill your codice fiscale to be able to receive invoices from FatturaPA'))
            return company.partner_id._l10n_it_edi_normalized_codice_fiscale()
        return super()._get_proxy_identification(company, proxy_type)
