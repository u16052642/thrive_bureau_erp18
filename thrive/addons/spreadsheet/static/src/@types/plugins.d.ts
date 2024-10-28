declare module "@spreadsheet" {
    import { CommandResult, CorePlugin, UIPlugin } from "@thrive/o-spreadsheet";
    import { CommandResult as CR } from "@spreadsheet/o_spreadsheet/cancelled_reason";
    type ThriveCommandResult = CommandResult | typeof CR;

    export interface ThriveCorePlugin extends CorePlugin {
        getters: ThriveCoreGetters;
        dispatch: ThriveCoreDispatch;
        allowDispatch(command: AllCoreCommand): string | string[];
        beforeHandle(command: AllCoreCommand): void;
        handle(command: AllCoreCommand): void;
    }

    export interface ThriveCorePluginConstructor {
        new (config: unknown): ThriveCorePlugin;
    }

    export interface ThriveUIPlugin extends UIPlugin {
        getters: ThriveGetters;
        dispatch: ThriveDispatch;
        allowDispatch(command: AllCommand): string | string[];
        beforeHandle(command: AllCommand): void;
        handle(command: AllCommand): void;
    }

    export interface ThriveUIPluginConstructor {
        new (config: unknown): ThriveUIPlugin;
    }
}
