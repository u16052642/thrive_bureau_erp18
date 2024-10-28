import { AbstractFigureClipboardHandler, registries } from "@thrive/o-spreadsheet";
const { clipboardHandlersRegistries } = registries;

class ThriveLinkClipboardHandler extends AbstractFigureClipboardHandler {
    copy(data) {
        const sheetId = this.getters.getActiveSheetId();
        const figure = this.getters.getFigure(sheetId, data.figureId);
        if (!figure) {
            throw new Error(`No figure for the given id: ${data.figureId}`);
        }
        if (figure.tag !== "chart") {
            return;
        }
        const thriveMenuId = this.getters.getChartThriveMenu(data.figureId);
        if (thriveMenuId) {
            return { thriveMenuId };
        }
    }
    paste(target, clippedContent, options) {
        if (!target.figureId || !clippedContent.thriveMenuId) {
            return;
        }
        const { figureId } = target;
        const { thriveMenuId } = clippedContent;
        this.dispatch("LINK_THRIVE_MENU_TO_CHART", {
            chartId: figureId,
            thriveMenuId: thriveMenuId.xmlid || thriveMenuId.id,
        });
    }
}

clipboardHandlersRegistries.figureHandlers.add("thrive_menu_link", ThriveLinkClipboardHandler);
