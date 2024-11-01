# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

import contextlib
import requests
from lxml import etree
from markupsafe import Markup
from hashlib import md5
from urllib import parse

from thrive import api, fields, models
from thrive.addons.account_peppol.tools.demo_utils import handle_demo
from thrive.addons.account.models.company import PEPPOL_LIST

TIMEOUT = 10
NON_PEPPOL_FORMAT = (False, 'facturx', 'oioubl_201', 'ciusro')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    invoice_sending_method = fields.Selection(
        selection_add=[('peppol', 'by Peppol')],
    )

    peppol_verification_state = fields.Selection(
        selection=[
            ('not_verified', 'Not verified yet'),
            ('not_valid', 'Not valid'),  # does not exist on Peppol at all
            ('not_valid_format', 'Cannot receive this format'),  # registered on Peppol but cannot receive the selected document type
            ('valid', 'Valid'),
        ],
        string='Peppol endpoint verification',
        company_dependent=True,
    )
    is_peppol_edi_format = fields.Boolean(compute='_compute_is_peppol_edi_format')

    # -------------------------------------------------------------------------
    # HELPERS
    # -------------------------------------------------------------------------

    def _log_verification_state_update(self, company, old_value, new_value):
        # log the update of the peppol verification state
        # we do this instead of regular tracking because of the customized message
        # and because we want to log the change for every company in the db
        if old_value == new_value:
            return

        peppol_verification_state_field = self._fields['peppol_verification_state']
        selection_values = dict(peppol_verification_state_field.selection)
        old_label = selection_values[old_value] if old_value else False  # get translated labels
        new_label = selection_values[new_value] if new_value else False

        body = Markup("""
            <ul>
                <li>
                    <span class='o-mail-Message-trackingOld me-1 px-1 text-muted fw-bold'>{old}</span>
                    <i class='o-mail-Message-trackingSeparator fa fa-long-arrow-right mx-1 text-600'/>
                    <span class='o-mail-Message-trackingNew me-1 fw-bold text-info'>{new}</span>
                    <span class='o-mail-Message-trackingField ms-1 fst-italic text-muted'>({field})</span>
                    <span class='o-mail-Message-trackingCompany ms-1 fst-italic text-muted'>({company})</span>
                </li>
            </ul>
        """).format(
            old=old_label,
            new=new_label,
            field=peppol_verification_state_field.string,
            company=company.display_name,
        )
        self._message_log(body=body)

    @api.model
    def _get_participant_info(self, edi_identification):
        hash_participant = md5(edi_identification.lower().encode()).hexdigest()
        endpoint_participant = parse.quote_plus(f"iso6523-actorid-upis::{edi_identification}")
        peppol_user = self.env.company.sudo().account_edi_proxy_client_ids.filtered(lambda user: user.proxy_type == 'peppol')
        edi_mode = peppol_user and peppol_user.edi_mode or 'prod'
        sml_zone = 'acc.edelivery' if edi_mode == 'test' else 'edelivery'
        smp_url = f"http://B-{hash_participant}.iso6523-actorid-upis.{sml_zone}.tech.ec.europa.eu/{endpoint_participant}"

        try:
            response = requests.get(smp_url, timeout=TIMEOUT)
        except requests.exceptions.ConnectionError:
            return None
        if response.status_code != 200:
            return None
        return etree.fromstring(response.content)

    @api.model
    def _check_peppol_participant_exists(self, participant_info, edi_identification, check_company=False):
        participant_identifier = participant_info.findtext('{*}ParticipantIdentifier')
        service_metadata = participant_info.find('.//{*}ServiceMetadataReference')
        service_href = ''
        if service_metadata is not None:
            service_href = service_metadata.attrib.get('href', '')

        if edi_identification != participant_identifier or 'hermes-belgium' in service_href:
            # all Belgian companies are pre-registered on hermes-belgium, so they will
            # technically have an existing SMP url but they are not real Peppol participants
            return False

        if check_company:
            # if we are only checking company's existence on the network, we don't care about what documents they can receive
            if not service_href:
                return True

            access_point_contact = True
            with contextlib.suppress(requests.exceptions.RequestException, etree.XMLSyntaxError):
                response = requests.get(service_href, timeout=TIMEOUT)
                if response.status_code == 200:
                    access_point_info = etree.fromstring(response.content)
                    access_point_contact = access_point_info.findtext('.//{*}TechnicalContactUrl') or access_point_info.findtext('.//{*}TechnicalInformationUrl')
            return access_point_contact

        return True

    def _check_document_type_support(self, participant_info, ubl_cii_format):
        service_references = participant_info.findall(
            '{*}ServiceMetadataReferenceCollection/{*}ServiceMetadataReference'
        )
        document_type = self.env['account.edi.xml.ubl_21']._get_customization_ids()[ubl_cii_format]
        for service in service_references:
            if document_type in parse.unquote_plus(service.attrib.get('href', '')):
                return True
        return False

    def _update_peppol_state_per_company(self, vals=None):
        partners = self.env['res.partner']
        if vals is None:
            partners = self.filtered(lambda p: all([p.peppol_eas, p.peppol_endpoint, p.is_ubl_format, p.country_code in PEPPOL_LIST]))
        elif {'peppol_eas', 'peppol_endpoint', 'invoice_edi_format'}.intersection(vals.keys()):
            partners = self.filtered(lambda p: p.country_code in PEPPOL_LIST)

        all_companies = None
        for partner in partners.sudo():
            if partner.company_id:
                partner.with_company(partner.company_id).button_account_peppol_check_partner_endpoint()
                continue

            if all_companies is None:
                all_companies = self.env['res.company'].sudo().search([])

            for company in all_companies:
                partner.with_company(company).button_account_peppol_check_partner_endpoint()

    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------

    @api.depends_context('company')
    @api.depends('invoice_edi_format')
    def _compute_is_peppol_edi_format(self):
        for partner in self:
            partner.is_peppol_edi_format = partner.invoice_edi_format not in NON_PEPPOL_FORMAT

    # -------------------------------------------------------------------------
    # LOW-LEVEL METHODS
    # -------------------------------------------------------------------------

    def write(self, vals):
        res = super().write(vals)
        self._update_peppol_state_per_company(vals=vals)
        return res

    def create(self, vals_list):
        res = super().create(vals_list)
        if res:
            res._update_peppol_state_per_company()
        return res

    # -------------------------------------------------------------------------
    # BUSINESS ACTIONS
    # -------------------------------------------------------------------------

    @handle_demo
    def button_account_peppol_check_partner_endpoint(self):
        """ A basic check for whether a participant is reachable at the given
        Peppol participant ID - peppol_eas:peppol_endpoint (ex: '9999:test')
        The SML (Service Metadata Locator) assigns a DNS name to each peppol participant.
        This DNS name resolves into the SMP (Service Metadata Publisher) of the participant.
        The DNS address is of the following form:
        - "http://B-" + hexstring(md5(lowercase(ID-VALUE))) + "." + ID-SCHEME + "." + SML-ZONE-NAME + "/" + url_encoded(ID-SCHEME + "::" + ID-VALUE)
        (ref:https://peppol.helger.com/public/locale-en_US/menuitem-docs-doc-exchange)
        """
        self.ensure_one()

        old_value = self.peppol_verification_state
        if (
            not (self.peppol_eas and self.peppol_endpoint)
            or self.with_company(self.company_id).invoice_edi_format in NON_PEPPOL_FORMAT
        ):
            self.peppol_verification_state = False
        else:
            edi_identification = f"{self.peppol_eas}:{self.peppol_endpoint}".lower()
            participant_info = self._get_participant_info(edi_identification)
            if participant_info is None:
                self.peppol_verification_state = 'not_valid'
            else:
                is_participant_on_network = self._check_peppol_participant_exists(participant_info, edi_identification)
                if is_participant_on_network:
                    is_valid_format = self._check_document_type_support(participant_info, self.with_company(self.company_id).invoice_edi_format)
                    if is_valid_format:
                        self.peppol_verification_state = 'valid'
                        self.with_company(self.company_id).invoice_sending_method = 'peppol'
                    else:
                        self.peppol_verification_state = 'not_valid_format'
                else:
                    self.peppol_verification_state = 'not_valid'

        self._log_verification_state_update(self.env.company, old_value, self.peppol_verification_state)
        return False
