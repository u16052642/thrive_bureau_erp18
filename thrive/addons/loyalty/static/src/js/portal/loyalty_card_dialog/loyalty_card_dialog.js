import { Component } from '@thrive/owl';
import { Dialog } from '@web/core/dialog/dialog';

export class PortalLoyaltyCardDialog extends Component {
    static components = { Dialog };
    static template = 'loyalty.portal_loyalty_card_dialog';
    static props = ['*'];

    setup() {
        this.csrf_token = thrive.csrf_token;
    }
}