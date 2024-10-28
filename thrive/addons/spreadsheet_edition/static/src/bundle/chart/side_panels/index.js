/** @thrive-module */

import * as spreadsheet from "@thrive/o-spreadsheet";
import { CommonThriveChartConfigPanel } from "./common/config_panel";
import { ThriveBarChartConfigPanel } from "./thrive_bar/thrive_bar_config_panel";
import { ThriveLineChartConfigPanel } from "./thrive_line/thrive_line_config_panel";
import { ThriveChartWithAxisDesignPanel } from "./thrive_chart_with_axis/design_panel";
import { _t } from "@web/core/l10n/translation";

const { chartSidePanelComponentRegistry, chartSubtypeRegistry } = spreadsheet.registries;
const { PieChartDesignPanel } = spreadsheet.components;

chartSidePanelComponentRegistry
    .add("thrive_line", {
        configuration: ThriveLineChartConfigPanel,
        design: ThriveChartWithAxisDesignPanel,
    })
    .add("thrive_bar", {
        configuration: ThriveBarChartConfigPanel,
        design: ThriveChartWithAxisDesignPanel,
    })
    .add("thrive_pie", {
        configuration: CommonThriveChartConfigPanel,
        design: PieChartDesignPanel,
    });

chartSubtypeRegistry.add("thrive_line", {
    matcher: (definition) =>
        definition.type === "thrive_line" && !definition.stacked && !definition.fillArea,
    subtypeDefinition: { stacked: false, fillArea: false },
    displayName: _t("Line"),
    chartSubtype: "thrive_line",
    chartType: "thrive_line",
    category: "line",
    preview: "o-spreadsheet-ChartPreview.LINE_CHART",
});
chartSubtypeRegistry.add("thrive_stacked_line", {
    matcher: (definition) =>
        definition.type === "thrive_line" && definition.stacked && !definition.fillArea,
    subtypeDefinition: { stacked: true, fillArea: false },
    displayName: _t("Stacked Line"),
    chartSubtype: "thrive_stacked_line",
    chartType: "thrive_line",
    category: "line",
    preview: "o-spreadsheet-ChartPreview.STACKED_LINE_CHART",
});
chartSubtypeRegistry.add("thrive_area", {
    matcher: (definition) =>
        definition.type === "thrive_line" && !definition.stacked && definition.fillArea,
    subtypeDefinition: { stacked: false, fillArea: true },
    displayName: _t("Area"),
    chartSubtype: "thrive_area",
    chartType: "thrive_line",
    category: "area",
    preview: "o-spreadsheet-ChartPreview.AREA_CHART",
});
chartSubtypeRegistry.add("thrive_stacked_area", {
    matcher: (definition) =>
        definition.type === "thrive_line" && definition.stacked && definition.fillArea,
    subtypeDefinition: { stacked: true, fillArea: true },
    displayName: _t("Stacked Area"),
    chartSubtype: "thrive_stacked_area",
    chartType: "thrive_line",
    category: "area",
    preview: "o-spreadsheet-ChartPreview.STACKED_AREA_CHART",
});
chartSubtypeRegistry.add("thrive_bar", {
    matcher: (definition) => definition.type === "thrive_bar" && !definition.stacked,
    subtypeDefinition: { stacked: false },
    displayName: _t("Column"),
    chartSubtype: "thrive_bar",
    chartType: "thrive_bar",
    category: "column",
    preview: "o-spreadsheet-ChartPreview.COLUMN_CHART",
});
chartSubtypeRegistry.add("thrive_stacked_bar", {
    matcher: (definition) => definition.type === "thrive_bar" && definition.stacked,
    subtypeDefinition: { stacked: true },
    displayName: _t("Stacked Column"),
    chartSubtype: "thrive_stacked_bar",
    chartType: "thrive_bar",
    category: "column",
    preview: "o-spreadsheet-ChartPreview.STACKED_COLUMN_CHART",
});
chartSubtypeRegistry.add("thrive_pie", {
    displayName: _t("Pie"),
    chartSubtype: "thrive_pie",
    chartType: "thrive_pie",
    category: "pie",
    preview: "o-spreadsheet-ChartPreview.PIE_CHART",
});
