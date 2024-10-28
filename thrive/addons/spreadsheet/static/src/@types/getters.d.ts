import { CorePlugin, Model, UID } from "@thrive/o-spreadsheet";
import { ChartThriveMenuPlugin, ThriveChartCorePlugin, ThriveChartUIPlugin } from "@spreadsheet/chart";
import { CurrencyPlugin } from "@spreadsheet/currency/plugins/currency";
import { AccountingPlugin } from "addons/spreadsheet_account/static/src/plugins/accounting_plugin";
import { GlobalFiltersCorePlugin, GlobalFiltersUIPlugin } from "@spreadsheet/global_filters";
import { ListCorePlugin, ListUIPlugin } from "@spreadsheet/list";
import { IrMenuPlugin } from "@spreadsheet/ir_ui_menu/ir_ui_menu_plugin";
import { PivotThriveCorePlugin } from "@spreadsheet/pivot";
import { PivotCoreGlobalFilterPlugin } from "@spreadsheet/pivot/plugins/pivot_core_global_filter_plugin";

type Getters = Model["getters"];
type CoreGetters = CorePlugin["getters"];

/**
 * Union of all getter names of a plugin.
 *
 * e.g. With the following plugin
 * @example
 * class MyPlugin {
 *   static getters = [
 *     "getCell",
 *     "getCellValue",
 *   ] as const;
 *   getCell() { ... }
 *   getCellValue() { ... }
 * }
 * type Names = GetterNames<typeof MyPlugin>
 * // is equivalent to "getCell" | "getCellValue"
 */
type GetterNames<Plugin extends { getters: readonly string[] }> = Plugin["getters"][number];

/**
 * Extract getter methods from a plugin, based on its `getters` static array.
 * @example
 * class MyPlugin {
 *   static getters = [
 *     "getCell",
 *     "getCellValue",
 *   ] as const;
 *   getCell() { ... }
 *   getCellValue() { ... }
 * }
 * type MyPluginGetters = PluginGetters<typeof MyPlugin>;
 * // MyPluginGetters is equivalent to:
 * // {
 * //   getCell: () => ...,
 * //   getCellValue: () => ...,
 * // }
 */
type PluginGetters<Plugin extends { new (...args: unknown[]): any; getters: readonly string[] }> =
    Pick<InstanceType<Plugin>, GetterNames<Plugin>>;

declare module "@spreadsheet" {
    /**
     * Add getters from custom plugins defined in thrive
     */

    interface ThriveCoreGetters extends CoreGetters {}
    interface ThriveCoreGetters extends PluginGetters<typeof GlobalFiltersCorePlugin> {}
    interface ThriveCoreGetters extends PluginGetters<typeof ListCorePlugin> {}
    interface ThriveCoreGetters extends PluginGetters<typeof ThriveChartCorePlugin> {}
    interface ThriveCoreGetters extends PluginGetters<typeof ChartThriveMenuPlugin> {}
    interface ThriveCoreGetters extends PluginGetters<typeof IrMenuPlugin> {}
    interface ThriveCoreGetters extends PluginGetters<typeof PivotThriveCorePlugin> {}
    interface ThriveCoreGetters extends PluginGetters<typeof PivotCoreGlobalFilterPlugin> {}

    interface ThriveGetters extends Getters {}
    interface ThriveGetters extends ThriveCoreGetters {}
    interface ThriveGetters extends PluginGetters<typeof GlobalFiltersUIPlugin> {}
    interface ThriveGetters extends PluginGetters<typeof ListUIPlugin> {}
    interface ThriveGetters extends PluginGetters<typeof ThriveChartUIPlugin> {}
    interface ThriveGetters extends PluginGetters<typeof CurrencyPlugin> {}
    interface ThriveGetters extends PluginGetters<typeof AccountingPlugin> {}
}
