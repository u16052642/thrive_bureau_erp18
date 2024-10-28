/** @thrive-module **/

import { Component } from "@thrive/owl";

export class NewContentRefreshBanner extends Component {
    static template = "social.NewContentRefreshBanner";
    static props = [
        "refreshRequired",
        "onClickRefresh",
    ];
}
