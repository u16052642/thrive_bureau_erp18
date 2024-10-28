/** @thrive-module */
import * as spreadsheet from "@thrive/o-spreadsheet";

import { Component } from "@thrive/owl";
const { Menu } = spreadsheet;

export class FilterComponent extends Component {
    static template = "spreadsheet_edition.FilterComponent";
    static components = { Menu };
    static props = {};

    get activeFilter() {
        return this.env.model.getters.getActiveFilterCount();
    }

    toggleDropdown() {
        this.env.toggleSidePanel("GLOBAL_FILTERS_SIDE_PANEL");
    }
}
