import { SpreadsheetChildEnv as SSChildEnv } from "@thrive/o-spreadsheet";
import { Services } from "services";

declare module "@spreadsheet" {
    import { Model } from "@thrive/o-spreadsheet";

    export interface SpreadsheetChildEnv extends SSChildEnv {
        model: ThriveSpreadsheetModel;
        services: Services;
    }
}
