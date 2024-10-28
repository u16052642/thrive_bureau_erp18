# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

import thrive.tests
from thrive.addons.gamification.tests.common import HttpCaseGamification


@thrive.tests.tagged('post_install', '-at_install')
class TestWebsiteProfile(HttpCaseGamification):
    def test_save_change_description(self):
        self.start_tour("/", 'website_profile_description', login="admin")
