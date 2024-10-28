/** @thrive-module **/

import { _t } from "@web/core/l10n/translation";
import { helpers, registries, EvaluationError } from "@thrive/o-spreadsheet";
import { sprintf } from "@web/core/utils/strings";

const { arg, toString, toNumber } = helpers;
const { functionRegistry } = registries;

//--------------------------------------------------------------------------
// Spreadsheet functions
//--------------------------------------------------------------------------

function assertListsExists(listId, getters) {
    if (!getters.isExistingList(listId)) {
        throw new EvaluationError(sprintf(_t('There is no list with id "%s"'), listId));
    }
}

const THRIVE_LIST = {
    description: _t("Get the value from a list."),
    args: [
        arg("list_id (string)", _t("ID of the list.")),
        arg("index (string)", _t("Position of the record in the list.")),
        arg("field_name (string)", _t("Name of the field.")),
    ],
    category: "Thrive",
    compute: function (listId, index, fieldName) {
        const id = toString(listId);
        const position = toNumber(index, this.locale) - 1;
        const _fieldName = toString(fieldName);
        assertListsExists(id, this.getters);
        return this.getters.getListCellValueAndFormat(id, position, _fieldName);
    },
    returns: ["NUMBER", "STRING"],
};

const THRIVE_LIST_HEADER = {
    description: _t("Get the header of a list."),
    args: [
        arg("list_id (string)", _t("ID of the list.")),
        arg("field_name (string)", _t("Name of the field.")),
    ],
    category: "Thrive",
    compute: function (listId, fieldName) {
        const id = toString(listId);
        const field = toString(fieldName);
        assertListsExists(id, this.getters);
        return this.getters.getListHeaderValue(id, field);
    },
    returns: ["NUMBER", "STRING"],
};

functionRegistry.add("THRIVE.LIST", THRIVE_LIST);
functionRegistry.add("THRIVE.LIST.HEADER", THRIVE_LIST_HEADER);
