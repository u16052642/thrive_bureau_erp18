/** @thrive-module **/

import { Component, useState } from "@thrive/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { _t } from "@web/core/l10n/translation";

export class InputDialog extends Component {
    static components = { Dialog };
    static props = {
        close: Function, // injected by the dialog service
        body: String,
        inputType: { type: String, optional: true },
        inputValue: { type: [String, Number], optional: true },
        confirm: { type: Function, optional: true },
        title: { type: String, optional: true },
    };
    static template = "spreadsheet_edition.InputDialog";

    setup() {
        this.state = useState({
            inputValue: this.props.inputValue,
            error: "",
        });
    }

    get defaultTitle() {
        return _t("Thrive Spreadsheet");
    }

    confirm() {
        const convertedValue = this.convertInputValue(this.state.inputValue);

        if (this.props.inputType === "number" && isNaN(convertedValue)) {
            this.state.error = _t("Please enter a valid number.");
            return;
        }

        this.props.close();
        this.props.confirm?.(convertedValue);
    }

    convertInputValue(value) {
        if (this.props.inputType === "number") {
            return parseInt(value, 10);
        }
        return value;
    }
}
