/** @thrive-module **/

import { clickOnEditAndWaitEditMode, registerWebsitePreviewTour } from "@website/js/tours/tour_utils";

registerWebsitePreviewTour("restricted_editor", {
    test: true,
    url: "/",
}, () => [
    ...clickOnEditAndWaitEditMode(),
]);