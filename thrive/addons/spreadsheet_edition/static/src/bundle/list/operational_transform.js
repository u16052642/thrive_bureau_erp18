/** @thrive-module */

import * as spreadsheet from "@thrive/o-spreadsheet";
const { otRegistry } = spreadsheet.registries;

otRegistry
    .addTransformation(
        "INSERT_THRIVE_LIST",
        ["INSERT_THRIVE_LIST", "DUPLICATE_THRIVE_LIST"],
        transformNewListCommand
    )
    .addTransformation(
        "DUPLICATE_THRIVE_LIST",
        ["INSERT_THRIVE_LIST", "DUPLICATE_THRIVE_LIST"],
        transformNewListCommand
    )
    .addTransformation(
        "REMOVE_THRIVE_LIST",
        ["RENAME_THRIVE_LIST", "UPDATE_THRIVE_LIST_DOMAIN", "UPDATE_THRIVE_LIST"],
        (toTransform, executed) => {
            if (toTransform.listId === executed.listId) {
                return undefined;
            }
            return toTransform;
        }
    )
    .addTransformation(
        "REMOVE_THRIVE_LIST",
        ["RE_INSERT_THRIVE_LIST", "DUPLICATE_THRIVE_LIST"],
        (toTransform, executed) => {
            if (toTransform.id === executed.listId) {
                return undefined;
            }
            return toTransform;
        }
    );

function transformNewListCommand(toTransform) {
    const idKey = "newListId" in toTransform ? "newListId" : "id";
    return {
        ...toTransform,
        [idKey]: (parseInt(toTransform[idKey], 10) + 1).toString(),
    };
}
