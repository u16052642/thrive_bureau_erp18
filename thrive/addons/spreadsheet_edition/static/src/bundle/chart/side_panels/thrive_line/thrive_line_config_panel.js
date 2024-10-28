/** @thrive-module */

import { CommonThriveChartConfigPanel } from "../common/config_panel";
import { _t } from "@web/core/l10n/translation";
import { components } from "@thrive/o-spreadsheet";

const { Checkbox } = components;

export class ThriveLineChartConfigPanel extends CommonThriveChartConfigPanel {
    static template = "spreadsheet_edition.ThriveLineChartConfigPanel";
    static components = {
        ...CommonThriveChartConfigPanel.components,
        Checkbox,
    };

    get stackedLabel() {
        return _t("Stacked linechart");
    }

    get cumulativeLabel() {
        return _t("Cumulative data");
    }

    onUpdateStacked(stacked) {
        this.props.updateChart(this.props.figureId, {
            stacked,
        });
    }
    onUpdateCumulative(cumulative) {
        this.props.updateChart(this.props.figureId, {
            cumulative,
        });
    }
}
