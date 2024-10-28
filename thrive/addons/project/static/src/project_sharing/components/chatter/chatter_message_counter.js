/** @thrive-module */

import { Component } from "@thrive/owl";

export class ChatterMessageCounter extends Component {
    static template = "project.ChatterMessageCounter";
    static props = {
        count: Number,
    };
}
