import { makeSpreadsheetMockEnv } from "@spreadsheet/../tests/helpers/model";

export const makeDocumentsSpreadsheetMockEnv = async (params = {}) => {
    const env = await makeSpreadsheetMockEnv(params);
    env.services["document.document"].store.thrivebot = { userId: 1 };
    return env;
};
