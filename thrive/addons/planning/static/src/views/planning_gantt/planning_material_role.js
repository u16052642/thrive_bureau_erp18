import { Component, useRef } from "@thrive/owl";
import { setupDisplayName } from "../planning_hooks";

export class PlanningMaterialRole extends Component {
    static template = "planning.PlanningMaterialRole";
    static props = {
        displayName: { type: String },
    };

    setup() {
        const displayNameRef = useRef("displayName");
        setupDisplayName(displayNameRef);
    }
}
