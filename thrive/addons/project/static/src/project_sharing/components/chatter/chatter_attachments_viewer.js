/** @thrive-module */

import { Component } from "@thrive/owl";

export class ChatterAttachmentsViewer extends Component {
    static template = "project.ChatterAttachmentsViewer";
    static props = {
        attachments: Array,
        canDelete: { type: Boolean, optional: true },
        delete: { type: Function, optional: true },
    };
    static defaultProps = {
        delete: async () => {},
    };
}