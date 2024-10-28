# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive.http import request
from thrive.tools import file_open
from thrive.addons.web.controllers import webmanifest


class WebManifest(webmanifest.WebManifest):

    def _get_service_worker_content(self):
        body = super()._get_service_worker_content()

        # Add notification support to the service worker if user but no public
        if request.env.user._is_internal():
            with file_open('mail/static/src/service_worker.js') as f:
                body += f.read()

        return body
