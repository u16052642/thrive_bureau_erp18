/** @thrive-module **/

import { markup, whenReady, validate } from "@thrive/owl";
import { browser } from "@web/core/browser/browser";
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { session } from "@web/session";
import { TourPointer } from "../tour_pointer/tour_pointer";
import { createPointerState } from "./tour_pointer_state";
import { tourState } from "./tour_state";
import { TourInteractive } from "./tour_interactive";
import { TourAutomatic } from "./tour_automatic";
import { callWithUnloadCheck } from "./tour_utils";
import {
    TOUR_RECORDER_ACTIVE_LOCAL_STORAGE_KEY,
    TourRecorder,
} from "@web_tour/tour_service/tour_recorder/tour_recorder";
import { redirect } from "@web/core/utils/urls";

const StepSchema = {
    id: { type: [String], optional: true },
    content: { type: [String, Object], optional: true }, //allow object(_t && markup)
    debugHelp: { type: String, optional: true },
    isActive: { type: Array, element: String, optional: true },
    run: { type: [String, Function, Boolean], optional: true },
    timeout: {
        optional: true,
        validate(value) {
            return value >= 0 && value <= 60000;
        },
    },
    tooltipPosition: {
        optional: true,
        validate(value) {
            return ["top", "bottom", "left", "right"].includes(value);
        },
    },
    trigger: { type: String },
    //ONLY IN DEBUG MODE
    pause: { type: Boolean, optional: true },
    break: { type: Boolean, optional: true },
};

const TourSchema = {
    checkDelay: { type: Number, optional: true },
    name: { type: String, optional: true },
    saveAs: { type: String, optional: true },
    rainbowManMessage: { type: [String, Boolean, Function], optional: true },
    sequence: { type: Number, optional: true },
    steps: Function,
    test: { type: Boolean, optional: true },
    url: { type: String, optional: true },
    wait_for: { type: [Function, Object], optional: true },
};

registry.category("web_tour.tours").addValidation(TourSchema);
const userMenuRegistry = registry.category("user_menuitems");

export const tourService = {
    // localization dependency to make sure translations used by tours are loaded
    dependencies: ["orm", "effect", "overlay", "localization"],
    start: async (_env, { orm, effect, overlay }) => {
        await whenReady();
        let toursEnabled = session?.tour_enabled;
        const tourRegistry = registry.category("web_tour.tours");
        const pointer = createPointerState();
        pointer.stop = () => {};

        userMenuRegistry.add("web_tour.tour_enabled", () => ({
            type: "switch",
            id: "web_tour.tour_enabled",
            description: _t("Onboarding"),
            callback: async () => {
                tourState.clear();
                toursEnabled = await orm.call("res.users", "switch_tour_enabled", [!toursEnabled]);
                browser.location.reload();
            },
            isChecked: toursEnabled,
            sequence: 30,
        }));

        function endTour({ name }) {
            // Used to signal the python test runner that the tour finished without error.
            browser.console.log("tour succeeded");
            // Used to see easily in the python console and to know which tour has been succeeded in suite tours case.
            const succeeded = `║ TOUR ${name} SUCCEEDED ║`;
            const msg = [succeeded];
            msg.unshift("╔" + "═".repeat(succeeded.length - 2) + "╗");
            msg.push("╚" + "═".repeat(succeeded.length - 2) + "╝");
            browser.console.log(`\n\n${msg.join("\n")}\n`);
            tourState.clear();
        }

        function getTourFromRegistry(tourName) {
            const tour = tourRegistry.getEntries().findLast(([n, t]) => t.saveAs == tourName) || [
                tourName,
                tourRegistry.get(tourName),
            ];

            return {
                ...tour[1],
                steps: tour[1].steps(),
                name: tour[0],
                wait_for: tour[1].wait_for || Promise.resolve(),
            };
        }

        async function getTourFromDB(tourName) {
            const tour = await orm.call("web_tour.tour", "get_tour_json_by_name", [tourName]);
            if (!tour) {
                throw new Error(`Tour '${tourName}' is not found in the database.`);
            }

            if (!tour.steps.length && tourRegistry.contains(tour.name)) {
                tour.steps = tourRegistry.get(tour.name).steps();
            }

            return tour;
        }

        function validateStep(step) {
            try {
                validate(step, StepSchema);
            } catch (error) {
                console.error(
                    `Error in schema for TourStep ${JSON.stringify(step, null, 4)}\n${
                        error.message
                    }`
                );
            }
        }

        async function startTour(tourName, options = {}) {
            pointer.stop();
            const tour = options.fromDB
                ? { name: tourName, url: options.url }
                : getTourFromRegistry(tourName);

            if (!session.is_public && !toursEnabled && options.mode === "manual") {
                toursEnabled = await orm.call("res.users", "switch_tour_enabled", [!toursEnabled]);
            }

            let tourConfig = {
                stepDelay: 0,
                keepWatchBrowser: false,
                mode: "auto",
                showPointerDuration: 0,
                debug: false,
                redirect: true,
            };

            tourConfig = Object.assign(tourConfig, options);
            tourState.setCurrentConfig(tourConfig);
            tourState.setCurrentTour(tour.name);
            tourState.setCurrentIndex(0);
            if (tourConfig.debug !== false) {
                // Starts the tour with a debugger to allow you to choose devtools configuration.
                // eslint-disable-next-line no-debugger
                debugger;
            }

            const willUnload = callWithUnloadCheck(() => {
                if (tour.url && tourConfig.startUrl != tour.url && tourConfig.redirect) {
                    redirect(tour.url);
                }
            });
            if (!willUnload) {
                resumeTour();
            }
        }

        async function resumeTour() {
            const tourName = tourState.getCurrentTour();
            const tourConfig = tourState.getCurrentConfig();

            let tour;
            if (tourConfig.fromDB) {
                tour = await getTourFromDB(tourName);
            } else if (tourRegistry.contains(tourName)) {
                tour = getTourFromRegistry(tourName);
            }

            if (!tour) {
                return;
            }

            tour.steps.forEach((step) => validateStep(step));
            pointer.stop = overlay.add(
                TourPointer,
                {
                    pointerState: pointer.state,
                    bounce: !(tourConfig.mode === "auto" && tourConfig.keepWatchBrowser),
                },
                {
                    sequence: 1100, // sequence based on bootstrap z-index values.
                }
            );

            if (tourConfig.mode === "auto") {
                new TourAutomatic(tour).start(pointer, () => {
                    pointer.stop();
                    endTour(tour);
                });
            } else {
                new TourInteractive(tour).start(pointer, async () => {
                    pointer.stop();
                    endTour(tour);
                    let message = tourConfig.rainbowManMessage || tour.rainbowManMessage;
                    if (message) {
                        message = window.DOMPurify.sanitize(tourConfig.rainbowManMessage);
                        effect.add({
                            type: "rainbow_man",
                            message: markup(message),
                        });
                    }

                    const nextTour = await orm.call("web_tour.tour", "consume", [tour.name]);
                    if (nextTour) {
                        startTour(nextTour.name, {
                            mode: "manual",
                            redirect: false,
                            rainbowManMessage: nextTour.rainbowManMessage,
                        });
                    }
                });
            }
        }

        function startTourRecorder() {
            if (!browser.localStorage.getItem(TOUR_RECORDER_ACTIVE_LOCAL_STORAGE_KEY)) {
                const remove = overlay.add(
                    TourRecorder,
                    {
                        onClose: () => {
                            remove();
                            browser.localStorage.removeItem(TOUR_RECORDER_ACTIVE_LOCAL_STORAGE_KEY);
                        },
                    },
                    { sequence: 99999 }
                );
            }
            browser.localStorage.setItem(TOUR_RECORDER_ACTIVE_LOCAL_STORAGE_KEY, "1");
        }

        if (!window.frameElement) {
            const paramsTourName = new URLSearchParams(browser.location.search).get("tour");
            if (paramsTourName) {
                startTour(paramsTourName, { mode: "manual", fromDB: true });
            }

            if (tourState.getCurrentTour()) {
                resumeTour();
            } else if (session.current_tour) {
                startTour(session.current_tour.name, {
                    mode: "manual",
                    redirect: false,
                    rainbowManMessage: session.current_tour.rainbowManMessage,
                });
            }

            if (
                browser.localStorage.getItem(TOUR_RECORDER_ACTIVE_LOCAL_STORAGE_KEY) &&
                !session.is_public
            ) {
                const remove = overlay.add(
                    TourRecorder,
                    {
                        onClose: () => {
                            remove();
                            browser.localStorage.removeItem(TOUR_RECORDER_ACTIVE_LOCAL_STORAGE_KEY);
                        },
                    },
                    { sequence: 99999 }
                );
            }
        }

        thrive.startTour = startTour;
        thrive.isTourReady = (tourName) => getTourFromRegistry(tourName).wait_for.then(() => true);

        return {
            startTour,
            startTourRecorder,
        };
    },
};

registry.category("services").add("tour_service", tourService);