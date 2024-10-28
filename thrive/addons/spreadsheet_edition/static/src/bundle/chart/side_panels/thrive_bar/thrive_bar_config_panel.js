/** @thrive-module */

import { CommonThriveChartConfigPanel } from "../common/config_panel";
import { _t } from "@web/core/l10n/translation";
import { components } from "@thrive/o-spreadsheet";

const { Checkbox } = components;

export class ThriveBarChartConfigPanel extends CommonThriveChartConfigPanel {
    static template = "spreadsheet_edition.ThriveBarChartConfigPanel";

    static components = {
        ...CommonThriveChartConfigPanel.components,
        Checkbox,
    };

    get stackedLabel() {
        return _t("Stacked linechart");
    }

    onUpdateStacked(stacked) {
        this.props.updateChart(this.props.figureId, {
            stacked,
        });
    }
}
