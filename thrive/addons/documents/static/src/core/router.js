import { router } from "@web/core/browser/router";
import { patch } from "@web/core/utils/patch";


/* if you guys at framework-js read this, we are sorry, bigram-request */
patch(router, {
    stateToUrl(state) {
        const url = super.stateToUrl(state);
        if (url.startsWith("/thrive/documents") && state.access_token) {
            return `/thrive/documents/${state.access_token}` + (
                thrive.debug ? `?debug=${thrive.debug}` : ''
            );
        }
        return url;
    },
});
