import { defineMenus, makeMockEnv } from "@web/../tests/web_test_helpers";
import { describe, expect, test } from "@thrive/hoot";

import { Model } from "@thrive/o-spreadsheet";
import { createBasicChart } from "@spreadsheet/../tests/helpers/commands";
import { createSpreadsheetWithChart } from "@spreadsheet/../tests/helpers/chart";
import { defineSpreadsheetModels } from "../../helpers/data";

const chartId = "uuid1";

describe.current.tags("headless");
defineMenus([
    {
        id: "root",
        children: [1, 2],
        name: "root",
        appID: "root",
    },
    {
        id: 1,
        children: [],
        name: "test menu 1",
        xmlid: "documents_spreadsheet.test.menu",
        appID: 1,
        actionID: "menuAction",
    },
    {
        id: 2,
        children: [],
        name: "test menu 2",
        xmlid: "documents_spreadsheet.test.menu2",
        appID: 1,
        actionID: "menuAction2",
    },
]);

defineSpreadsheetModels();

test("Links between charts and ir.menus are correctly imported/exported", async function () {
    const env = await makeMockEnv();
    const model = new Model({}, { custom: { env } });
    createBasicChart(model, chartId);
    model.dispatch("LINK_THRIVE_MENU_TO_CHART", {
        chartId,
        thriveMenuId: 1,
    });
    const exportedData = model.exportData();
    expect(exportedData.chartThriveMenusReferences[chartId]).toBe(1, {
        message: "Link to thrive menu is exported",
    });
    const importedModel = new Model(exportedData, { custom: { env } });
    const chartMenu = importedModel.getters.getChartThriveMenu(chartId);
    expect(chartMenu.id).toBe(1, { message: "Link to thrive menu is imported" });
});

test("Can undo-redo a LINK_THRIVE_MENU_TO_CHART", async function () {
    const env = await makeMockEnv();
    const model = new Model({}, { custom: { env } });
    createBasicChart(model, chartId);
    model.dispatch("LINK_THRIVE_MENU_TO_CHART", {
        chartId,
        thriveMenuId: 1,
    });
    expect(model.getters.getChartThriveMenu(chartId).id).toBe(1);
    model.dispatch("REQUEST_UNDO");
    expect(model.getters.getChartThriveMenu(chartId)).toBe(undefined);
    model.dispatch("REQUEST_REDO");
    expect(model.getters.getChartThriveMenu(chartId).id).toBe(1);
});

test("link is removed when figure is deleted", async function () {
    const env = await makeMockEnv();
    const model = new Model({}, { custom: { env } });
    createBasicChart(model, chartId);
    model.dispatch("LINK_THRIVE_MENU_TO_CHART", {
        chartId,
        thriveMenuId: 1,
    });
    expect(model.getters.getChartThriveMenu(chartId).id).toBe(1);
    model.dispatch("DELETE_FIGURE", {
        sheetId: model.getters.getActiveSheetId(),
        id: chartId,
    });
    expect(model.getters.getChartThriveMenu(chartId)).toBe(undefined);
});

test("Links of Thrive charts are duplicated when duplicating a sheet", async function () {
    const { model } = await createSpreadsheetWithChart({ type: "thrive_pie" });
    const sheetId = model.getters.getActiveSheetId();
    const secondSheetId = "mySecondSheetId";
    const chartId = model.getters.getChartIds(sheetId)[0];
    model.dispatch("DUPLICATE_SHEET", { sheetId, sheetIdTo: secondSheetId });
    const newChartId = model.getters.getChartIds(secondSheetId)[0];
    expect(model.getters.getChartThriveMenu(newChartId)).toEqual(
        model.getters.getChartThriveMenu(chartId)
    );
});

test("Links of standard charts are duplicated when duplicating a sheet", async function () {
    const env = await makeMockEnv();
    const model = new Model({}, { custom: { env } });
    const sheetId = model.getters.getActiveSheetId();
    const secondSheetId = "mySecondSheetId";
    createBasicChart(model, chartId);
    model.dispatch("LINK_THRIVE_MENU_TO_CHART", {
        chartId,
        thriveMenuId: 1,
    });
    model.dispatch("DUPLICATE_SHEET", { sheetId, sheetIdTo: secondSheetId });
    const newChartId = model.getters.getChartIds(secondSheetId)[0];
    expect(model.getters.getChartThriveMenu(newChartId)).toEqual(
        model.getters.getChartThriveMenu(chartId)
    );
});
