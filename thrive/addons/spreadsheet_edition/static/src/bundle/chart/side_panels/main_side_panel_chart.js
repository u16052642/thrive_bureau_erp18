/** @thrive-module **/

import { patch } from "@web/core/utils/patch";
import * as spreadsheet from "@thrive/o-spreadsheet";
import { onWillUpdateProps } from "@thrive/owl";

const { chartSubtypeRegistry } = spreadsheet.registries;
const { ChartTypePicker } = spreadsheet.components;

/**
 * This patch is necessary to ensure that the chart type cannot be changed
 * between thrive charts and spreadsheet charts.
 */

patch(ChartTypePicker.prototype, {
    setup() {
        super.setup();
        this.updateChartTypeByCategories(this.props);
        onWillUpdateProps((nexProps) => this.updateChartTypeByCategories(nexProps));
    },

    /**
     * @param {boolean} isThrive
     */
    getChartTypes(isThrive) {
        const result = {};
        for (const key of chartSubtypeRegistry.getKeys()) {
            if ((isThrive && key.startsWith("thrive_")) || (!isThrive && !key.startsWith("thrive_"))) {
                result[key] = chartSubtypeRegistry.get(key).name;
            }
        }
        return result;
    },

    onTypeChange(type) {
        if (this.getChartDefinition(this.props.figureId).type.startsWith("thrive_")) {
            const newChartInfo = chartSubtypeRegistry.get(type);
            const definition = {
                verticalAxisPosition: "left",
                ...this.env.model.getters.getChartDefinition(this.props.figureId),
                ...newChartInfo.subtypeDefinition,
                type: newChartInfo.chartType,
            };
            this.env.model.dispatch("UPDATE_CHART", {
                definition,
                id: this.props.figureId,
                sheetId: this.env.model.getters.getActiveSheetId(),
            });
            this.closePopover();
        } else {
            super.onTypeChange(type);
        }
    },
    updateChartTypeByCategories(props) {
        const definition = this.env.model.getters.getChartDefinition(props.figureId);
        const isThrive = definition.type.startsWith("thrive_");
        const registryItems = chartSubtypeRegistry.getAll().filter((item) => {
            return isThrive
                ? item.chartType.startsWith("thrive_")
                : !item.chartType.startsWith("thrive_");
        });

        this.chartTypeByCategories = {};
        for (const chartInfo of registryItems) {
            if (this.chartTypeByCategories[chartInfo.category]) {
                this.chartTypeByCategories[chartInfo.category].push(chartInfo);
            } else {
                this.chartTypeByCategories[chartInfo.category] = [chartInfo];
            }
        }
    },
});
