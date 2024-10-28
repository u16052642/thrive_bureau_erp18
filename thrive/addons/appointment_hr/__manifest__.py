# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

{
    'name': "Employees on Appointments",
    'version': "1.0",
    'category': 'Services/Appointment',
    'sequence': 2140,
    'summary': "Manage Appointments with Employees",
    'website': 'https://www.thrivebureau.com/app/appointments',
    'description': """
Take into account the working schedule (sick leaves, part time, ...) of employees when scheduling appointments
--------------------------------------------------------------------------------------------------------------
""",
    'depends': ['appointment', 'hr'],
    'data': [
        'views/appointment_type_views.xml',
    ],
    'auto_install': True,
    'license': 'OEEL-1',
}
