import { components } from "@thrive/o-spreadsheet";
import { THRIVE_AGGREGATORS } from "@spreadsheet/pivot/pivot_helpers";
const { PivotLayoutConfigurator } = components;

export class ThrivePivotLayoutConfigurator extends PivotLayoutConfigurator {
    setup() {
        super.setup(...arguments);
        this.AGGREGATORS = THRIVE_AGGREGATORS;
    }
}
