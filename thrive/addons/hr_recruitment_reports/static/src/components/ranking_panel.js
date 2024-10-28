/** @thrive-module **/

import { Component } from "@thrive/owl";

export default class RankingPanel extends Component {
    static template = "hr_recruitment_reports.RankingPanel";
    static props = {
        ranked_list: Object,
    };
}
