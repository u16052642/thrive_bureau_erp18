import { Component } from "@thrive/owl";

export class ThriveLogo extends Component {
    static template = "point_of_sale.ThriveLogo";
    static props = {
        class: { type: String, optional: true },
        style: { type: String, optional: true },
        monochrome: { type: Boolean, optional: true },
    };
    static defaultProps = {
        class: "",
        style: "",
        monochrome: false,
    };
}
