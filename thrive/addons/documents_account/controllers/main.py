# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive.http import content_disposition, request, route
from thrive.tools import str2bool
from thrive.addons.documents.controllers.documents import ShareRoute


class AccountShareRoute(ShareRoute):

    @route()
    def documents_content(self, access_token, download=False):
        if str2bool(download):
            return super().documents_content(access_token)

        document = self._from_access_token(access_token, skip_log=True)
        is_public = request.env.user._is_public()
        if document.sudo(is_public).has_embedded_pdf:
            # TODO: cache the extracted pdf in the browser
            embedded_pdf = document.sudo(is_public)._extract_pdf_from_xml()
            headers = [
                ('Content-Type', 'application/pdf'),
                ('X-Content-Type-Options', 'nosniff'),
                ('Content-Length', len(embedded_pdf)),
                ('Content-Disposition', content_disposition(f"{document.name}.pdf")),
            ]
            return request.make_response(embedded_pdf, headers)

        return super().documents_content(access_token)
