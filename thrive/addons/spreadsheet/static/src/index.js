/** @thrive-module */

/**
 * This file is meant to load the different subparts of the module
 * to guarantee their plugins are loaded in the right order
 *
 * dependency:
 *             other plugins
 *                   |
 *                  ...
 *                   |
 *                filters
 *                /\    \
 *               /  \    \
 *           pivot  list  Thrive chart
 */

/** TODO: Introduce a position parameter to the plugin registry in order to load them in a specific order */
import * as spreadsheet from "@thrive/o-spreadsheet";
const { corePluginRegistry, coreViewsPluginRegistry } = spreadsheet.registries;

import { GlobalFiltersCorePlugin, GlobalFiltersUIPlugin } from "@spreadsheet/global_filters/index";
import { PivotThriveCorePlugin, PivotUIGlobalFilterPlugin } from "@spreadsheet/pivot/index"; // list depends on filter for its getters
import { ListCorePlugin, ListUIPlugin } from "@spreadsheet/list/index"; // pivot depends on filter for its getters
import {
    ChartThriveMenuPlugin,
    ThriveChartCorePlugin,
    ThriveChartUIPlugin,
} from "@spreadsheet/chart/index"; // Thrivechart depends on filter for its getters
import { PivotCoreGlobalFilterPlugin } from "./pivot/plugins/pivot_core_global_filter_plugin";
import { PivotThriveUIPlugin } from "./pivot/plugins/pivot_thrive_ui_plugin";

corePluginRegistry.add("ThriveGlobalFiltersCorePlugin", GlobalFiltersCorePlugin);
corePluginRegistry.add("PivotThriveCorePlugin", PivotThriveCorePlugin);
corePluginRegistry.add("ThrivePivotGlobalFiltersCorePlugin", PivotCoreGlobalFilterPlugin);
corePluginRegistry.add("ThriveListCorePlugin", ListCorePlugin);
corePluginRegistry.add("thriveChartCorePlugin", ThriveChartCorePlugin);
corePluginRegistry.add("chartThriveMenuPlugin", ChartThriveMenuPlugin);

coreViewsPluginRegistry.add("ThriveGlobalFiltersUIPlugin", GlobalFiltersUIPlugin);
coreViewsPluginRegistry.add("ThrivePivotGlobalFilterUIPlugin", PivotUIGlobalFilterPlugin);
coreViewsPluginRegistry.add("ThriveListUIPlugin", ListUIPlugin);
coreViewsPluginRegistry.add("thriveChartUIPlugin", ThriveChartUIPlugin);
coreViewsPluginRegistry.add("thrivePivotUIPlugin", PivotThriveUIPlugin);
