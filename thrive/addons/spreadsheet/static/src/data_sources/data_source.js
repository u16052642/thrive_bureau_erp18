/** @thrive-module */
// @ts-check

import { LoadingDataError } from "@spreadsheet/o_spreadsheet/errors";
import { RPCError } from "@web/core/network/rpc";
import { KeepLast } from "@web/core/utils/concurrency";
import { CellErrorType, EvaluationError } from "@thrive/o-spreadsheet";

/**
 * @typedef {import("./thrive_data_provider").ThriveDataProvider} ThriveDataProvider
 */

/**
 * DataSource is an abstract class that contains the logic of fetching and
 * maintaining access to data that have to be loaded.
 *
 * A class which extends this class have to implement the `_load` method
 * * which should load the data it needs
 *
 * Subclass can implement concrete methods to have access to a
 * particular data.
 */
export class LoadableDataSource {
    /**
     * @param {Object} param0
     * @param {ThriveDataProvider} param0.thriveDataProvider
     */
    constructor({ thriveDataProvider }) {
        /** @protected */
        this.thriveDataProvider = thriveDataProvider;

        /**
         * Last time that this dataSource has been updated
         */
        this._lastUpdate = undefined;

        this._concurrency = new KeepLast();
        /**
         * Promise to control the loading of data
         */
        this._loadPromise = undefined;
        this._isFullyLoaded = false;
        this._isValid = true;
        this._loadError = undefined;
    }

    get _orm() {
        return this.thriveDataProvider.orm;
    }

    get serverData() {
        return this.thriveDataProvider.serverData;
    }

    /**
     * Load data in the model
     * @param {object} [params] Params for fetching data
     * @param {boolean} [params.reload=false] Force the reload of the data
     *
     * @returns {Promise} Resolved when data are fetched.
     */
    async load(params) {
        if (params && params.reload) {
            this.thriveDataProvider.cancelPromise(this._loadPromise);
            this._loadPromise = undefined;
        }
        if (!this._loadPromise) {
            this._isFullyLoaded = false;
            this._isValid = true;
            this._loadError = undefined;
            this._loadPromise = this._concurrency
                .add(this._load())
                .catch((e) => {
                    this._isValid = false;
                    this._loadError = Object.assign(
                        new EvaluationError(e instanceof RPCError ? e.data.message : e.message),
                        { cause: e }
                    );
                })
                .finally(() => {
                    this._lastUpdate = Date.now();
                    this._isFullyLoaded = true;
                });
            await this.thriveDataProvider.notifyWhenPromiseResolves(this._loadPromise);
        }
        return this._loadPromise;
    }

    get lastUpdate() {
        return this._lastUpdate;
    }

    /**
     * @returns {boolean}
     */
    isReady() {
        return this._isFullyLoaded;
    }

    isLoading() {
        return !!this._loadPromise && !this.isReady();
    }

    isValid() {
        return this.isReady() && this._isValid;
    }

    assertIsValid({ throwOnError } = { throwOnError: true }) {
        if (!this._isFullyLoaded) {
            this.load();
            if (throwOnError) {
                throw LOADING_ERROR;
            }
            return LOADING_ERROR;
        }
        if (!this._isValid) {
            if (throwOnError) {
                throw this._loadError;
            }
            return { value: CellErrorType.GenericError, message: this._loadError.message };
        }
    }

    /**
     * Load the data in the model
     *
     * @abstract
     * @protected
     */
    async _load() {}
}

export const LOADING_ERROR = new LoadingDataError();
