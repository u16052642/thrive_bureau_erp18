/** @thrive-module */

import * as spreadsheet from "@thrive/o-spreadsheet";
import { ThrivePivot } from "@spreadsheet/pivot/thrive_pivot";
import { patch } from "@web/core/utils/patch";
const { helpers } = spreadsheet;
const { formatValue } = helpers;

/**
 * @typedef {import("@thrive/o-spreadsheet").PivotDomain} PivotDomain
 */

patch(ThrivePivot.prototype, {
    /**
     * High level method computing the formatted result of PIVOT.HEADER functions.
     *
     * @param {PivotDomain} domain
     */
    getPivotHeaderFormattedValue(domain) {
        const { value, format } = this.getPivotHeaderValueAndFormat(domain);
        if (typeof value === "string") {
            return value;
        }
        const locale = this.getters.getLocale();
        return formatValue(value, { format, locale });
    },
});
