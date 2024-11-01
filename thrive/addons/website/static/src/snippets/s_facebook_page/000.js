/** @thrive-module **/

import { _t } from "@web/core/l10n/translation";
import { pick } from "@web/core/utils/objects";
import { clamp } from "@web/core/utils/numbers";
import publicWidget from "@web/legacy/js/public/public_widget";
import { debounce } from "@web/core/utils/timing";
import { ObservingCookieWidgetMixin } from "@website/snippets/observing_cookie_mixin";

const FacebookPageWidget = publicWidget.Widget.extend(ObservingCookieWidgetMixin, {
    selector: '.o_facebook_page',
    disabledInEditableMode: false,

    /**
     * @override
     */
    start: function () {
        var def = this._super.apply(this, arguments);
        this.previousWidth = 0;

        const params = pick(this.$el[0].dataset, 'href', 'id', 'height', 'tabs', 'small_header', 'hide_cover');
        if (!params.href) {
            return def;
        }
        if (params.id) {
            params.href = `https://www.facebook.com/${params.id}`;
        }
        delete params.id;

        this._renderIframe(params);
        this.resizeObserver = new ResizeObserver(debounce(this._renderIframe.bind(this, params), 100));
        this.resizeObserver.observe(this.el.parentElement);

        return def;
    },
    /**
     * @override
     */
    destroy: function () {
        this._super.apply(this, arguments);
        if (this.iframeEl) {
            this.iframeEl.remove();
        }
        this.resizeObserver.disconnect();
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * Prepare iframe element & replace it with existing iframe.
     *
     * @private
     * @param {Object} params
    */
    _renderIframe(params) {
        this.options.wysiwyg && this.options.wysiwyg.thriveEditor.observerUnactive();

        params.width = clamp(Math.floor(this.$el.width()), 180, 500);
        if (this.previousWidth !== params.width) {
            this.previousWidth = params.width;
            const searchParams = new URLSearchParams(params);
            const src = "https://www.facebook.com/plugins/page.php?" + searchParams;
            this.iframeEl = Object.assign(document.createElement("iframe"), {
                width: params.width,
                height: params.height,
                css: {
                    border: "none",
                    overflow: "hidden",
                },
                scrolling: "no",
                frameborder: "0",
                allowTransparency: "true",
                "aria-label": _t("Facebook"),
            });
            this.el.replaceChildren(this.iframeEl);
            this._manageIframeSrc(this.el, src);
        }

        this.options.wysiwyg && this.options.wysiwyg.thriveEditor.observerActive();
    },
});

publicWidget.registry.facebookPage = FacebookPageWidget;

export default FacebookPageWidget;
