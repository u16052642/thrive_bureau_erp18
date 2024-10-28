/** @thrive-module **/
// @ts-check

import { helpers } from "@thrive/o-spreadsheet";

const { getFunctionsFromTokens } = helpers;

/**
 * @typedef {import("@thrive/o-spreadsheet").Token} Token
 * @typedef  {import("@spreadsheet/helpers/thrive_functions_helpers").ThriveFunctionDescription} ThriveFunctionDescription
 */

/**
 * @param {Token[]} tokens
 * @returns {number}
 */
export function getNumberOfAccountFormulas(tokens) {
    return getFunctionsFromTokens(tokens, ["THRIVE.BALANCE", "THRIVE.CREDIT", "THRIVE.DEBIT"]).length;
}

/**
 * Get the first Account function description of the given formula.
 *
 * @param {Token[]} tokens
 * @returns {ThriveFunctionDescription | undefined}
 */
export function getFirstAccountFunction(tokens) {
    return getFunctionsFromTokens(tokens, ["THRIVE.BALANCE", "THRIVE.CREDIT", "THRIVE.DEBIT"])[0];
}
