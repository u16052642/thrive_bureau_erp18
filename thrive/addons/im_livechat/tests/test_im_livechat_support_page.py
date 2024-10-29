# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

import thrive
from thrive.tests import HttpCase

@thrive.tests.tagged('-at_install', 'post_install')
class TestImLivechatSupportPage(HttpCase):
    def test_load_modules(self):
        """Checks that all javascript modules load correctly on the livechat support page"""

        # Give some time to the assets to load to prevent fetch
        # interrupt errors then ensures all the assets are loaded.
        check_js_modules = """
            thrive.livechatReady.then(() => {
                const { missing, failed, unloaded } = thrive.loader.findErrors();
                if ([missing, failed, unloaded].some(arr => arr.length)) {
                    console.error("Couldn't load all JS modules.", JSON.stringify({ missing, failed, unloaded }));
                } else {
                    console.log("test successful");
                }
                Object.assign(console, {
                    log: () => {},
                    error: () => {},
                    warn: () => {},
                });
            })
        """
        self.browser_js("/im_livechat/support/1", code=check_js_modules)