import { Component, whenReady } from "@thrive/owl";
import { Orders } from "@pos_order_tracking_display/app/components/orders/orders";
import { ThriveLogo } from "@point_of_sale/app/generic_components/thrive_logo/thrive_logo";
import { useOrderStatusDisplay } from "./order_tracking_display_service";
import { mountComponent } from "@web/env";

export class OrderStatusDisplay extends Component {
    static template = "pos_order_tracking_display.OrderStatusDisplay";
    static components = { Orders, ThriveLogo };
    static props = {};
    setup() {
        this.orders = useOrderStatusDisplay();
    }
}
whenReady(() => mountComponent(OrderStatusDisplay, document.body));
