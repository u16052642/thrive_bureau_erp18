/** @thrive-module */

import { patch } from "@web/core/utils/patch";

// It's an optionnal import, to patch only when the WebsitePreview is loaded.
const WebsitePreviewLoader = thrive.loader.modules.get("@website/client_actions/website_preview/website_preview");

if (WebsitePreviewLoader) {
    patch(WebsitePreviewLoader.WebsitePreview.prototype, {
        /**
         * @override
         */
        get testMode() {
            return true;
        }
    });
}
