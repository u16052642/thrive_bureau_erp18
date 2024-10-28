# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import fields, models


class FleetVehicleState(models.Model):
    _inherit = 'fleet.vehicle.state'

    hide_in_offer = fields.Boolean()
