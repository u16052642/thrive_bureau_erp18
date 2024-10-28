# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive.addons.web.controllers import webmanifest
from thrive.tools.translate import LazyTranslate

_lt = LazyTranslate(__name__)


class WebManifest(webmanifest.WebManifest):

    def _get_scoped_app_shortcuts(self, app_id):
        if app_id == "industry_fsm":
            return [{
                'name': _lt("New task"),
                'url': '/scoped_app/field-service/new',
            }, {
                'name': _lt("My Tasks"),
                'url': '/scoped_app/field-service',
            }, {
                'name': _lt("My Calendar"),
                'url': '/scoped_app/field-service?view_type=calendar',
            }]
        return super()._get_scoped_app_shortcuts(app_id)
