/** @thrive-module */

import { IrMenuSelector } from "@spreadsheet_edition/bundle/ir_menu_selector/ir_menu_selector";
import { Domain } from "@web/core/domain";
import { DomainSelector } from "@web/core/domain_selector/domain_selector";
import { DomainSelectorDialog } from "@web/core/domain_selector_dialog/domain_selector_dialog";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { components } from "@thrive/o-spreadsheet";

import { Component, onWillStart, onWillUpdateProps } from "@thrive/owl";
const { Section } = components;

export class CommonThriveChartConfigPanel extends Component {
    static template = "spreadsheet_edition.CommonThriveChartConfigPanel";
    static components = { IrMenuSelector, DomainSelector, Section };
    static props = {
        figureId: String,
        definition: Object,
        updateChart: Function,
        canUpdateChart: Function,
    };

    setup() {
        this.dialog = useService("dialog");
        const loadData = async (figureId) => {
            const dataSource = this.env.model.getters.getChartDataSource(figureId);
            this.modelDisplayName = await dataSource.getModelLabel();
        };
        onWillStart(() => loadData(this.props.figureId));
        onWillUpdateProps((nextProps) => loadData(nextProps.figureId));
    }

    get model() {
        const definition = this.env.model.getters.getChartDefinition(this.props.figureId);
        return definition.metaData.resModel;
    }

    get domain() {
        const definition = this.env.model.getters.getChartDefinition(this.props.figureId);
        return new Domain(definition.searchParams.domain).toString();
    }

    onNameChanged(title) {
        const definition = {
            ...this.env.model.getters.getChartDefinition(this.props.figureId),
            title,
        };
        this.env.model.dispatch("UPDATE_CHART", {
            id: this.props.figureId,
            sheetId: this.env.model.getters.getFigureSheetId(this.props.figureId),
            definition,
        });
    }

    /**
     * Get the last update date, formatted
     *
     * @returns {string} date formatted
     */
    getLastUpdate() {
        const dataSource = this.env.model.getters.getChartDataSource(this.props.figureId);
        const lastUpdate = dataSource.lastUpdate;
        if (lastUpdate) {
            return new Date(lastUpdate).toLocaleTimeString();
        }
        return _t("never");
    }

    openDomainEdition() {
        this.dialog.add(DomainSelectorDialog, {
            resModel: this.model,
            domain: new Domain(this.domain).toString(),
            isDebugMode: !!this.env.debug,
            onConfirm: (domain) => {
                const definition = this.env.model.getters.getChartDefinition(this.props.figureId);
                const updatedDefinition = {
                    ...definition,
                    searchParams: {
                        ...definition.searchParams,
                        domain: new Domain(domain).toJson(),
                    },
                };
                this.env.model.dispatch("UPDATE_CHART", {
                    id: this.props.figureId,
                    sheetId: this.env.model.getters.getFigureSheetId(this.props.figureId),
                    definition: updatedDefinition,
                });
            },
        });
    }

    get thriveMenuId() {
        const menu = this.env.model.getters.getChartThriveMenu(this.props.figureId);
        return menu ? menu.id : undefined;
    }
    /**
     * @param {number | undefined} thriveMenuId
     */
    updateThriveLink(thriveMenuId) {
        if (!thriveMenuId) {
            this.env.model.dispatch("LINK_THRIVE_MENU_TO_CHART", {
                chartId: this.props.figureId,
                thriveMenuId: undefined,
            });
            return;
        }
        const menu = this.env.model.getters.getIrMenu(thriveMenuId);
        this.env.model.dispatch("LINK_THRIVE_MENU_TO_CHART", {
            chartId: this.props.figureId,
            thriveMenuId: menu.xmlid || menu.id,
        });
    }
}
