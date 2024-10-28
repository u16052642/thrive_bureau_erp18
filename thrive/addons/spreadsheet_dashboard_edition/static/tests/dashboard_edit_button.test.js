import { patchWithCleanup, getMockEnv, onRpc } from "@web/../tests/web_test_helpers";
import { animationFrame } from "@thrive/hoot-mock";
import { expect, test, getFixture, describe } from "@thrive/hoot";
import { click } from "@thrive/hoot-dom";
import { createSpreadsheetDashboard } from "@spreadsheet_dashboard/../tests/helpers/dashboard_action";
import { defineSpreadsheetDashboardModels } from "@spreadsheet_dashboard/../tests/helpers/data";

describe.current.tags("desktop");
defineSpreadsheetDashboardModels();

test("Clicking 'Edit' icon navigates to dashboard edit view", async function () {
    patchWithCleanup(thrive, { debug: true });
    const action = {
        type: "ir.actions.client",
        tag: "action_edit_dashboard",
        params: {
            spreadsheet_id: 1,
        },
    };
    await createSpreadsheetDashboard({
        mockRPC: async function (route, args) {
            if (args.method === "action_edit_dashboard" && args.model === "spreadsheet.dashboard") {
                expect.step("action_edit_dashboard");
                return action;
            }
        },
    });
    const env = getMockEnv();
    patchWithCleanup(env.services.action, {
        doAction(action) {
            expect.step("doAction");
            expect(action.params.spreadsheet_id).toBe(1);
            expect(action.tag).toBe("action_edit_dashboard");
        },
    });
    click(".o_edit_dashboard");
    await animationFrame();
    expect.verifySteps(["action_edit_dashboard", "doAction"]);
});

test("User without edit permissions does not see the 'Edit' option on the dashboard (Debug mode ON)", async function () {
    patchWithCleanup(thrive, { debug: true });
    onRpc("has_group", async (route, args) => {
        return false;
    });
    await createSpreadsheetDashboard();
    expect(".o_edit_dashboard").toHaveCount(0);
});

test("User with edit permissions sees the 'Edit' option on the dashboard (Debug mode ON)", async function () {
    patchWithCleanup(thrive, { debug: true });
    onRpc("has_group", async (route, args) => {
        return true;
    });
    await createSpreadsheetDashboard();
    expect(
        getFixture().querySelector(".o_search_panel_category_value .o_edit_dashboard")
    ).toHaveCount(1);
});

test("User with edit permissions does not see the 'Edit' option on the dashboard (Debug mode OFF)", async function () {
    patchWithCleanup(thrive, { debug: false });
    onRpc("has_group", async (route, args) => {
        return true;
    });
    await createSpreadsheetDashboard();
    expect(".o_edit_dashboard").toHaveCount(0);
});
