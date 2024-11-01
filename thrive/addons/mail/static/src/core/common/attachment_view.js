import {
    Component,
    onWillUpdateProps,
    onPatched,
    onWillUnmount,
    onMounted,
    useEffect,
    useRef,
    useState,
} from "@thrive/owl";

import { useBus, useService } from "@web/core/utils/hooks";
import { hidePDFJSButtons } from "@web/libs/pdfjs";

/**
 * @typedef {Object} Props
 * @property {number} threadId
 * @property {string} threadModel
 * @extends {Component<Props, Env>}
 */
export class AttachmentView extends Component {
    static template = "mail.AttachmentView";
    static components = {};
    static props = ["threadId", "threadModel"];

    setup() {
        super.setup();
        this.store = useState(useService("mail.store"));
        this.uiService = useService("ui");
        this.mailPopoutService = useService("mail.popout");
        this.iframeViewerPdfRef = useRef("iframeViewerPdf");
        this.state = useState({
            /** @type {import("models").Thread|undefined} */
            thread: undefined,
        });
        useEffect(() => {
            if (this.iframeViewerPdfRef.el) {
                hidePDFJSButtons(this.iframeViewerPdfRef.el);
            }
        });
        this.updateFromProps(this.props);
        onWillUpdateProps((props) => this.updateFromProps(props));

        useBus(this.uiService.bus, "resize", this.updatePopup);
        onMounted(this.updatePopup);
        onPatched(this.updatePopup);
        onWillUnmount(this.mailPopoutService.reset);
    }

    onClickNext() {
        const index = this.state.thread.attachmentsInWebClientView.findIndex((attachment) =>
            attachment.eq(this.state.thread.mainAttachment)
        );
        this.state.thread.setMainAttachmentFromIndex(
            index === this.state.thread.attachmentsInWebClientView.length - 1 ? 0 : index + 1
        );
    }

    onClickPrevious() {
        const index = this.state.thread.attachmentsInWebClientView.findIndex((attachment) =>
            attachment.eq(this.state.thread.mainAttachment)
        );
        this.state.thread.setMainAttachmentFromIndex(
            index === 0 ? this.state.thread.attachmentsInWebClientView.length - 1 : index - 1
        );
    }

    updateFromProps(props) {
        this.state.thread = this.store.Thread.insert({
            id: props.threadId,
            model: props.threadModel,
        });
    }

    popoutAttachment() {
        this.mailPopoutService.popout(this.__owl__.bdom.parentEl).focus();
    }

    updatePopup() {
        if (this.mailPopoutService.externalWindow) {
            this.mailPopoutService.popout(this.__owl__.bdom.parentEl, false);
        }
    }

    get displayName() {
        return this.state.thread.mainAttachment.filename;
    }
}
