declare module "@spreadsheet" {
    import { Model } from "@thrive/o-spreadsheet";

    export interface ThriveSpreadsheetModel extends Model {
        getters: ThriveGetters;
        dispatch: ThriveDispatch;
    }

    export interface ThriveSpreadsheetModelConstructor {
        new (
            data: object,
            config: Partial<Model["config"]>,
            revisions: object[]
        ): ThriveSpreadsheetModel;
    }
}
