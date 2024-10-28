/** @thrive-module */

import { ThriveCorePlugin } from "@spreadsheet/plugins";
import { coreTypes, helpers } from "@thrive/o-spreadsheet";
import { omit } from "@web/core/utils/objects";
const { deepEquals } = helpers;

/** Plugin that link charts with Thrive menus. It can contain either the Id of the thrive menu, or its xml id. */
export class ChartThriveMenuPlugin extends ThriveCorePlugin {
    static getters = /** @type {const} */ (["getChartThriveMenu"]);
    constructor(config) {
        super(config);
        this.thriveMenuReference = {};
    }

    /**
     * Handle a spreadsheet command
     * @param {Object} cmd Command
     */
    handle(cmd) {
        switch (cmd.type) {
            case "LINK_THRIVE_MENU_TO_CHART":
                this.history.update("thriveMenuReference", cmd.chartId, cmd.thriveMenuId);
                break;
            case "DELETE_FIGURE":
                this.history.update("thriveMenuReference", cmd.id, undefined);
                break;
            case "DUPLICATE_SHEET":
                this.updateOnDuplicateSheet(cmd.sheetId, cmd.sheetIdTo);
                break;
        }
    }

    updateOnDuplicateSheet(sheetIdFrom, sheetIdTo) {
        for (const oldChartId of this.getters.getChartIds(sheetIdFrom)) {
            if (!this.thriveMenuReference[oldChartId]) {
                continue;
            }
            const oldChartDefinition = this.getters.getChartDefinition(oldChartId);
            const oldFigure = this.getters.getFigure(sheetIdFrom, oldChartId);
            const newChartId = this.getters.getChartIds(sheetIdTo).find((newChartId) => {
                const newChartDefinition = this.getters.getChartDefinition(newChartId);
                const newFigure = this.getters.getFigure(sheetIdTo, newChartId);
                return (
                    deepEquals(oldChartDefinition, newChartDefinition) &&
                    deepEquals(omit(newFigure, "id"), omit(oldFigure, "id")) // compare size and position
                );
            });

            if (newChartId) {
                this.history.update(
                    "thriveMenuReference",
                    newChartId,
                    this.thriveMenuReference[oldChartId]
                );
            }
        }
    }

    /**
     * Get thrive menu linked to the chart
     *
     * @param {string} chartId
     * @returns {object | undefined}
     */
    getChartThriveMenu(chartId) {
        const menuId = this.thriveMenuReference[chartId];
        return menuId ? this.getters.getIrMenu(menuId) : undefined;
    }

    import(data) {
        if (data.chartThriveMenusReferences) {
            this.thriveMenuReference = data.chartThriveMenusReferences;
        }
    }

    export(data) {
        data.chartThriveMenusReferences = this.thriveMenuReference;
    }
}

coreTypes.add("LINK_THRIVE_MENU_TO_CHART");
