import { describe, expect, getFixture, test } from "@thrive/hoot";
import { dblclick } from "@thrive/hoot-dom";
import { animationFrame } from "@thrive/hoot-mock";
import { createSpreadsheetDashboard } from "@spreadsheet_dashboard/../tests/helpers/dashboard_action";
import {
    defineSpreadsheetDashboardModels,
    getDashboardServerData,
} from "@spreadsheet_dashboard/../tests/helpers/data";
import { contains } from "@web/../tests/web_test_helpers";

describe.current.tags("mobile");
defineSpreadsheetDashboardModels();

test("is empty with no figures", async () => {
    await createSpreadsheetDashboard();
    const fixture = getFixture();
    expect(".o_mobile_dashboard").toHaveCount(1);
    const content = fixture.querySelector(".o_mobile_dashboard");
    expect(content.innerText.split("\n")).toEqual([
        "Dashboard CRM 1",
        "Only chart figures are displayed in small screens but this dashboard doesn't contain any",
    ]);
});

test("with no available dashboard", async () => {
    const serverData = getDashboardServerData();
    serverData.models["spreadsheet.dashboard"].records = [];
    serverData.models["spreadsheet.dashboard.group"].records = [];
    await createSpreadsheetDashboard({ serverData });
    const fixture = getFixture();
    const content = fixture.querySelector(".o_mobile_dashboard");
    expect(content.innerText).toBe("No available dashboard");
});

test("displays figures in first sheet", async () => {
    const figure = {
        tag: "chart",
        height: 500,
        width: 500,
        x: 100,
        y: 100,
        data: {
            type: "line",
            dataSetsHaveTitle: false,
            dataSets: [{ dataRange: "A1" }],
            legendPosition: "top",
            verticalAxisPosition: "left",
            title: { text: "" },
        },
    };
    const spreadsheetData = {
        sheets: [
            {
                id: "sheet1",
                figures: [{ ...figure, id: "figure1" }],
            },
            {
                id: "sheet2",
                figures: [{ ...figure, id: "figure2" }],
            },
        ],
    };
    const serverData = getDashboardServerData();
    serverData.models["spreadsheet.dashboard.group"].records = [
        {
            published_dashboard_ids: [789],
            id: 1,
            name: "Chart",
        },
    ];
    serverData.models["spreadsheet.dashboard"].records = [
        {
            id: 789,
            name: "Spreadsheet with chart figure",
            json_data: JSON.stringify(spreadsheetData),
            spreadsheet_data: JSON.stringify(spreadsheetData),
            dashboard_group_id: 1,
        },
    ];
    await createSpreadsheetDashboard({ serverData });
    expect(".o-chart-container").toHaveCount(1);
});

test("double clicking on a figure doesn't open the side panel", async () => {
    const figure = {
        tag: "chart",
        height: 500,
        width: 500,
        x: 100,
        y: 100,
        data: {
            type: "line",
            dataSetsHaveTitle: false,
            dataSets: [{ dataRange: "A1" }],
            legendPosition: "top",
            verticalAxisPosition: "left",
            title: { text: "" },
        },
    };
    const spreadsheetData = {
        sheets: [
            {
                id: "sheet1",
                figures: [{ ...figure, id: "figure1" }],
            },
        ],
    };
    const serverData = getDashboardServerData();
    serverData.models["spreadsheet.dashboard.group"].records = [
        {
            published_dashboard_ids: [789],
            id: 1,
            name: "Chart",
        },
    ];
    serverData.models["spreadsheet.dashboard"].records = [
        {
            id: 789,
            name: "Spreadsheet with chart figure",
            json_data: JSON.stringify(spreadsheetData),
            spreadsheet_data: JSON.stringify(spreadsheetData),
            dashboard_group_id: 1,
        },
    ];
    await createSpreadsheetDashboard({ serverData });
    await contains(".o-chart-container").focus();
    await dblclick(".o-chart-container");
    await animationFrame();
    expect(".o-chart-container").toHaveCount(1);
    expect(".o-sidePanel").toHaveCount(0);
});

test("can switch dashboard", async () => {
    await createSpreadsheetDashboard();
    const fixture = getFixture();
    expect(fixture.querySelector(".o_search_panel_summary").innerText).toBe("Dashboard CRM 1");
    await contains(".o_search_panel_current_selection").click();
    const dashboardElements = [...document.querySelectorAll("section header.list-group-item")];
    expect(dashboardElements[0].classList.contains("active")).toBe(true);
    expect(dashboardElements.map((el) => el.innerText)).toEqual([
        "Dashboard CRM 1",
        "Dashboard CRM 2",
        "Dashboard Accounting 1",
    ]);
    await contains(dashboardElements[1]).click();
    expect(fixture.querySelector(".o_search_panel_summary").innerText).toBe("Dashboard CRM 2");
});

test("can go back from dashboard selection", async () => {
    await createSpreadsheetDashboard();
    const fixture = getFixture();
    expect(".o_mobile_dashboard").toHaveCount(1);
    expect(fixture.querySelector(".o_search_panel_summary").innerText).toBe("Dashboard CRM 1");
    await contains(".o_search_panel_current_selection").click();
    await contains(document.querySelector(".o_mobile_search_button")).click();
    expect(fixture.querySelector(".o_search_panel_summary").innerText).toBe("Dashboard CRM 1");
});
