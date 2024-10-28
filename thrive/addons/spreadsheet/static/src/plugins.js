/** @thrive-module */

import { CorePlugin, UIPlugin } from "@thrive/o-spreadsheet";

/**
 * An o-spreadsheet core plugin with access to all custom Thrive plugins
 * @type {import("@spreadsheet").ThriveCorePluginConstructor}
 **/
export const ThriveCorePlugin = CorePlugin;

/**
 * An o-spreadsheet UI plugin with access to all custom Thrive plugins
 * @type {import("@spreadsheet").ThriveUIPluginConstructor}
 **/
export const ThriveUIPlugin = UIPlugin;
