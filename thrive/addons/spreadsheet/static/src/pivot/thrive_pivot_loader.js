//@ts-check

import { EvaluationError, CellErrorType } from "@thrive/o-spreadsheet";
import { RPCError } from "@web/core/network/rpc";
import { KeepLast } from "@web/core/utils/concurrency";
import { LOADING_ERROR } from "@spreadsheet/data_sources/data_source";

/**
 * @typedef {import("@spreadsheet").ThriveFields} ThriveFields
 * @typedef {import("@spreadsheet/data_sources/thrive_data_provider").ThriveDataProvider} ThriveDataProvider
 */

export class ThrivePivotLoader {
    /**
     * @param {ThriveDataProvider} thriveDataProvider
     * @param {Function} load Function to fetch data
     */
    constructor(thriveDataProvider, load) {
        /** @private @type {ThriveDataProvider} */
        this.thriveDataProvider = thriveDataProvider;
        /** @protected */
        this.loadFn = load;

        /**
         * Last time that this dataSource has been updated
         */
        this.lastUpdate = undefined;

        /** @protected */
        this.concurrency = new KeepLast();
        /** @protected */
        this.loadPromise = undefined;
        /** @protected */
        this.isFullyLoaded = false;
        /** @protected */
        this._isValid = true;
        /** @protected */
        this.loadError = undefined;
    }

    /**
     * Load data in the model
     * @param {object} [options] options for fetching data
     * @param {boolean} [options.reload=false] Force the reload of the data
     *
     * @returns {Promise} Resolved when data are fetched.
     */
    async load(options) {
        if (options && options.reload) {
            this.thriveDataProvider.cancelPromise(this.loadPromise);
            this.loadPromise = undefined;
        }
        if (!this.loadPromise) {
            this.isFullyLoaded = false;
            this._isValid = true;
            this.loadError = undefined;
            this.loadPromise = this.concurrency
                .add(this.loadFn())
                .catch((e) => {
                    this._isValid = false;
                    this.loadError = Object.assign(
                        new EvaluationError(e instanceof RPCError ? e.data.message : e.message),
                        { cause: e }
                    );
                })
                .finally(() => {
                    this.lastUpdate = Date.now();
                    this.isFullyLoaded = true;
                });
            await this.thriveDataProvider.notifyWhenPromiseResolves(this.loadPromise);
        }
        return this.loadPromise;
    }

    /**
     * @param {string} model Technical name of the model
     * @returns {Promise<ThriveFields>} Fields of the model
     */
    async getFields(model) {
        return await this.thriveDataProvider.serverData.fetch(model, "fields_get");
    }
    /**
     * @param {string} model Technical name of the model
     * @returns {Promise<string>} Display name of the model
     */
    async getModelLabel(model) {
        const result = await this.thriveDataProvider.serverData.fetch(
            "ir.model",
            "display_name_for",
            [[model]]
        );
        return (result[0] && result[0].display_name) || "";
    }

    isValid() {
        return this.isFullyLoaded && this._isValid;
    }

    hasEverBeenLoaded() {
        return this.loadPromise !== undefined;
    }

    assertIsValid({ throwOnError } = { throwOnError: true }) {
        if (!this.isFullyLoaded) {
            this.load();
            if (throwOnError) {
                throw LOADING_ERROR;
            }
            return LOADING_ERROR;
        }
        if (!this.isValid()) {
            if (throwOnError) {
                throw this.loadError;
            }
            return { value: CellErrorType.GenericError, message: this.loadError.message };
        }
    }
}
