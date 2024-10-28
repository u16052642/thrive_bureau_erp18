# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import http
from thrive.http import request
from thrive.tools import file_open, image_process
from thrive.addons.web.controllers import webmanifest


class WebManifest(webmanifest.WebManifest):

    def _get_scoped_app_icons(self, app_id):
        if app_id == "mrp_shop_floor":
            return [{
            'src': '/mrp_workorder/static/description/mrp_display_icon.svg',
            'sizes': 'any',
            'type': 'image/svg+xml'
            }]
        return super()._get_scoped_app_icons(app_id)

    @http.route()
    def scoped_app_icon_png(self, app_id):
        if app_id == "mrp_shop_floor":
            with file_open('mrp_workorder/static/description/mrp_display_icon.png', 'rb') as file:
                image = image_process(file.read(), size=(180, 180), expand=True, colorize=(255, 255, 255), padding=16)
            return request.make_response(image, headers=[('Content-Type', 'image/png')])
        return super().scoped_app_icon_png(app_id)
