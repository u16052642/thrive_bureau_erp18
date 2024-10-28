/** @thrive-module **/

import { Component } from "@thrive/owl";

export class PedalStatusButton extends Component {
   static template = "mrp_workorder_iot.PedalStatusButton";
   static props = {
      ...Component.props,
      pedalConnected: { type: Boolean },
      takeOwnership: { type: Function },
   };
}
