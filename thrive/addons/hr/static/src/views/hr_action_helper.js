import { Component } from "@thrive/owl";

export class HrActionHelper extends Component {
    static template = "hr.EmployeeActionHelper";
    static props = { noContentTitle: { type: String }, noContentParagraph: { type: String } };
}
