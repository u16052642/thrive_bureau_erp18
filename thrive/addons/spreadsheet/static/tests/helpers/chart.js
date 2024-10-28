import { animationFrame } from "@thrive/hoot-mock";

import * as spreadsheet from "@thrive/o-spreadsheet";
import { createModelWithDataSource } from "@spreadsheet/../tests/helpers/model";
const uuidGenerator = new spreadsheet.helpers.UuidGenerator();

/**
 * @typedef {import("@thrive/o-spreadsheet").Model} Model
 * @typedef {import("@spreadsheet").ThriveSpreadsheetModel} ThriveSpreadsheetModel
 */

/**
 *
 * @param {Model} model
 * @param {string} type
 * @param {import("@spreadsheet/chart/thrive_chart/thrive_chart").ThriveChartDefinition} definition
 */
export function insertChartInSpreadsheet(
    model,
    type = "thrive_bar",
    definition = getChartDefinition(type)
) {
    model.dispatch("CREATE_CHART", {
        sheetId: model.getters.getActiveSheetId(),
        id: definition.id,
        position: {
            x: 10,
            y: 10,
        },
        definition,
    });
}
/**
 *
 * @param {Object} params
 * @param {function} [params.definition]
 * @param {function} [params.mockRPC]
 * @param {string} [params.type]
 * @param {import("./data").ServerData} [params.serverData]
 *
 * @returns { Promise<{ model: ThriveSpreadsheetModel, env: Object }>}
 */
export async function createSpreadsheetWithChart(params = {}) {
    const model = await createModelWithDataSource(params);

    insertChartInSpreadsheet(model, params.type, params.definition);

    const env = model.config.custom.env;
    env.model = model;
    await animationFrame();
    return { model, env };
}

function getChartDefinition(type) {
    return {
        metaData: {
            groupBy: ["foo", "bar"],
            measure: "__count",
            order: null,
            resModel: "partner",
        },
        searchParams: {
            comparison: null,
            context: {},
            domain: [],
            groupBy: [],
            orderBy: [],
        },
        stacked: true,
        title: { text: "Partners" },
        background: "#FFFFFF",
        legendPosition: "top",
        verticalAxisPosition: "left",
        dataSourceId: uuidGenerator.uuidv4(),
        id: uuidGenerator.uuidv4(),
        type,
    };
}
