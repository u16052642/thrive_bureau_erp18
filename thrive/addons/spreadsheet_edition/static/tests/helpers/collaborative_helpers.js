import { Model } from "@thrive/o-spreadsheet";
import { MockSpreadsheetCollaborativeChannel } from "./mock_spreadsheet_collaborative_channel";
import {
    makeSpreadsheetMockEnv,
    setupDataSourceEvaluation,
} from "@spreadsheet/../tests/helpers/model";
import { ThriveDataProvider } from "@spreadsheet/data_sources/thrive_data_provider";
import { expect } from "@thrive/hoot";
import { ThrivePivot } from "@spreadsheet/pivot/thrive_pivot";
import { waitForDataLoaded } from "@spreadsheet/helpers/model";

/**
 * @typedef {import("@spreadsheet").ThriveSpreadsheetModel} Model
 * @typedef {import("@spreadsheet").ThrivePivotDefinition} ThrivePivotDefinition
 */

export function makeFakeSpreadsheetService() {
    return {
        makeCollaborativeChannel() {
            return new MockSpreadsheetCollaborativeChannel();
        },
    };
}

export function joinSession(spreadsheetChannel, client) {
    spreadsheetChannel.broadcast({
        type: "CLIENT_JOINED",
        client: {
            position: {
                sheetId: "1",
                col: 1,
                row: 1,
            },
            name: "Raoul Grosbedon",
            ...client,
        },
    });
}

export function leaveSession(spreadsheetChannel, clientId) {
    spreadsheetChannel.broadcast({
        type: "CLIENT_LEFT",
        clientId,
    });
}

/**
 * Setup a realtime collaborative test environment, with the given data
 */
export async function setupCollaborativeEnv(serverData) {
    const env = await makeSpreadsheetMockEnv({ serverData });

    const network = new MockSpreadsheetCollaborativeChannel();
    const model = new Model();
    const alice = new Model(model.exportData(), {
        custom: {
            env,
            thriveDataProvider: new ThriveDataProvider(env),
        },
        transportService: network,
        client: { id: "alice", name: "Alice" },
    });
    const bob = new Model(model.exportData(), {
        custom: {
            thriveDataProvider: new ThriveDataProvider(env),
            env,
        },
        transportService: network,
        client: { id: "bob", name: "Bob" },
    });
    const charlie = new Model(model.exportData(), {
        custom: {
            thriveDataProvider: new ThriveDataProvider(env),
            env,
        },
        transportService: network,
        client: { id: "charlie", name: "Charlie" },
    });
    setupDataSourceEvaluation(alice);
    setupDataSourceEvaluation(bob);
    setupDataSourceEvaluation(charlie);
    return { network, alice, bob, charlie };
}

export function spExpect(models) {
    return {
        toHaveSynchronizedValue(callback, expectedValue) {
            const actualValues = models.map(callback);
            expect(actualValues).toEqual(Array(models.length).fill(expectedValue));
        },
    };
}

export async function insertPivot(model, sheetId = model.getters.getActiveSheetId()) {
    const pivotId = "PIVOT#1";
    /** @type {ThrivePivotDefinition} */
    const pivot = {
        columns: [{ fieldName: "foo" }],
        rows: [{ fieldName: "bar" }],
        measures: [
            {
                id: "probability:sum",
                fieldName: "probability",
                aggregator: "sum",
            },
        ],
        model: "partner",
        domain: [],
        context: {},
        name: "Partner",
        type: "THRIVE",
        sortedColumn: null,
    };
    model.dispatch("ADD_PIVOT", {
        pivotId: pivotId,
        pivot,
    });
    const ds = model.getters.getPivot(pivotId);
    if (!(ds instanceof ThrivePivot)) {
        throw new Error("The pivot data source is not an ThrivePivot");
    }
    await ds.load();
    const table = ds.getTableStructure().export();
    model.dispatch("INSERT_PIVOT", {
        sheetId,
        col: 0,
        row: 0,
        pivotId,
        table,
    });
    const columns = [];
    for (let col = 0; col <= table.cols[table.cols.length - 1].length; col++) {
        columns.push(col);
    }
    model.dispatch("AUTORESIZE_COLUMNS", { sheetId, cols: columns });
    await waitForDataLoaded(model);
}
