/** @thrive-module **/

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";

registry.category("web_tour.tours").add("knowledge_tour", {
    url: "/thrive",
    steps: () => [
        {
            trigger: '.o_app[data-menu-xmlid="knowledge.knowledge_menu_root"]',
            content: _t("Get on track and explore our recommendations for your Thrive usage here!"),
            position: "bottom",
            run: "click",
        },
    ],
});
