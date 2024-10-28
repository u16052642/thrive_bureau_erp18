/** @thrive-module **/

import { Dialog } from "@web/core/dialog/dialog";
import { Component } from "@thrive/owl";

export class SaleActionHelperDialog extends Component {
    static components = { Dialog };
    static template = "sale.SaleActionHelperDialog";
    static props = {
        url: String,
        close: Function,
    };
}
