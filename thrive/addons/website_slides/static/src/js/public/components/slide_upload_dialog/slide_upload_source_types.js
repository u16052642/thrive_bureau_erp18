/** @thrive-module **/

import { Component, useState } from "@thrive/owl";

export class SlideUploadSourceTypes extends Component {
    static props = {
        attributes: {
            type: Object,
            shape: {
                sourceTypeLabel: { type: String, optional: true },
                selectFileLabel: { type: String, optional: true },
                acceptedFiles: { type: String, optional: true },
                urlInputLabel: String,
                urlInputName: String,
            },
        },
        isLocalSource: Boolean,
        onClickSourceType: Function,
        onChangeFileInput: Function,
        onChangeUrl: Function,
    };
    static template = "website_slides.SlideUploadSourceTypes";

    setup() {
        this.state = useState({ url: "" });
    }
}
