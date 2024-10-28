/** @thrive-module */
// @ts-check

import { helpers } from "@thrive/o-spreadsheet";

const { getFunctionsFromTokens } = helpers;

/** @typedef {import("@thrive/o-spreadsheet").Token} Token */

/**
 * Parse a spreadsheet formula and detect the number of LIST functions that are
 * present in the given formula.
 *
 * @param {Token[]} tokens
 *
 * @returns {number}
 */
export function getNumberOfListFormulas(tokens) {
    return getFunctionsFromTokens(tokens, ["THRIVE.LIST", "THRIVE.LIST.HEADER"]).length;
}

/**
 * Get the first List function description of the given formula.
 *
 * @param {Token[]} tokens
 *
 * @returns {import("../helpers/thrive_functions_helpers").ThriveFunctionDescription|undefined}
 */
export function getFirstListFunction(tokens) {
    return getFunctionsFromTokens(tokens, ["THRIVE.LIST", "THRIVE.LIST.HEADER"])[0];
}
