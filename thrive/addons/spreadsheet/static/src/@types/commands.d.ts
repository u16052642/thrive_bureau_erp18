import { FieldMatching } from "./global_filter.d";
import {
    CorePlugin,
    UIPlugin,
    DispatchResult,
    CommandResult,
    AddPivotCommand,
    UpdatePivotCommand,
    CancelledReason,
} from "@thrive/o-spreadsheet";
import * as ThriveCancelledReason from "@spreadsheet/o_spreadsheet/cancelled_reason";

type CoreDispatch = CorePlugin["dispatch"];
type UIDispatch = UIPlugin["dispatch"];
type CoreCommand = Parameters<CorePlugin["allowDispatch"]>[0];
type Command = Parameters<UIPlugin["allowDispatch"]>[0];

// TODO look for a way to remove this and use the real import * as ThriveCancelledReason
type ThriveCancelledReason = string;

declare module "@spreadsheet" {
    interface ThriveCommandDispatcher {
        dispatch<T extends ThriveCommandTypes, C extends Extract<ThriveCommand, { type: T }>>(
            type: {} extends Omit<C, "type"> ? T : never
        ): ThriveDispatchResult;
        dispatch<T extends ThriveCommandTypes, C extends Extract<ThriveCommand, { type: T }>>(
            type: T,
            r: Omit<C, "type">
        ): ThriveDispatchResult;
    }

    interface ThriveCoreCommandDispatcher {
        dispatch<T extends ThriveCoreCommandTypes, C extends Extract<ThriveCoreCommand, { type: T }>>(
            type: {} extends Omit<C, "type"> ? T : never
        ): ThriveDispatchResult;
        dispatch<T extends ThriveCoreCommandTypes, C extends Extract<ThriveCoreCommand, { type: T }>>(
            type: T,
            r: Omit<C, "type">
        ): ThriveDispatchResult;
    }

    interface ThriveDispatchResult extends DispatchResult {
        readonly reasons: (CancelledReason | ThriveCancelledReason)[];
        isCancelledBecause(reason: CancelledReason | ThriveCancelledReason): boolean;
    }

    type ThriveCommandTypes = ThriveCommand["type"];
    type ThriveCoreCommandTypes = ThriveCoreCommand["type"];

    type ThriveDispatch = UIDispatch & ThriveCommandDispatcher["dispatch"];
    type ThriveCoreDispatch = CoreDispatch & ThriveCoreCommandDispatcher["dispatch"];

    // CORE

    export interface ExtendedAddPivotCommand extends AddPivotCommand {
        pivot: ExtendedPivotCoreDefinition;
    }

    export interface ExtendedUpdatePivotCommand extends UpdatePivotCommand {
        pivot: ExtendedPivotCoreDefinition;
    }

    export interface AddThreadCommand {
        type: "ADD_COMMENT_THREAD";
        threadId: number;
        sheetId: string;
        col: number;
        row: number;
    }

    export interface EditThreadCommand {
        type: "EDIT_COMMENT_THREAD";
        threadId: number;
        sheetId: string;
        col: number;
        row: number;
        isResolved: boolean;
    }

    export interface DeleteThreadCommand {
        type: "DELETE_COMMENT_THREAD";
        threadId: number;
        sheetId: string;
        col: number;
        row: number;
    }

    // this command is deprecated. use UPDATE_PIVOT instead
    export interface UpdatePivotDomainCommand {
        type: "UPDATE_THRIVE_PIVOT_DOMAIN";
        pivotId: string;
        domain: Array;
    }

    export interface AddGlobalFilterCommand {
        type: "ADD_GLOBAL_FILTER";
        filter: CmdGlobalFilter;
        [string]: any; // Fields matching
    }

    export interface EditGlobalFilterCommand {
        type: "EDIT_GLOBAL_FILTER";
        filter: CmdGlobalFilter;
        [string]: any; // Fields matching
    }

    export interface RemoveGlobalFilterCommand {
        type: "REMOVE_GLOBAL_FILTER";
        id: string;
    }

    export interface MoveGlobalFilterCommand {
        type: "MOVE_GLOBAL_FILTER";
        id: string;
        delta: number;
    }

    // UI

    export interface RefreshAllDataSourcesCommand {
        type: "REFRESH_ALL_DATA_SOURCES";
    }

    export interface SetGlobalFilterValueCommand {
        type: "SET_GLOBAL_FILTER_VALUE";
        id: string;
        value: any;
        displayNames?: string[];
    }

    export interface SetManyGlobalFilterValueCommand {
        type: "SET_MANY_GLOBAL_FILTER_VALUE";
        filters: { filterId: string; value: any }[];
    }

    export interface ClearGlobalFilterValueCommand {
        type: "CLEAR_GLOBAL_FILTER_VALUE";
        id: string;
    }

    type ThriveCoreCommand =
        | ExtendedAddPivotCommand
        | ExtendedUpdatePivotCommand
        | UpdatePivotDomainCommand
        | AddThreadCommand
        | DeleteThreadCommand
        | EditThreadCommand
        | AddGlobalFilterCommand
        | EditGlobalFilterCommand
        | RemoveGlobalFilterCommand
        | MoveGlobalFilterCommand;

    export type AllCoreCommand = ThriveCoreCommand | CoreCommand;

    type ThriveLocalCommand =
        | RefreshAllDataSourcesCommand
        | SetGlobalFilterValueCommand
        | SetManyGlobalFilterValueCommand
        | ClearGlobalFilterValueCommand;

    type ThriveCommand = ThriveCoreCommand | ThriveLocalCommand;

    export type AllCommand = ThriveCommand | Command;
}
