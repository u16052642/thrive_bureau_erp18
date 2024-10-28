# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

# Updating mako environement in order to be able to use slug
try:
    from thrive.tools.rendering_tools import template_env_globals
    from thrive.http import request

    template_env_globals.update({
        'slug': lambda value: request.env['ir.http']._slug(value)  # noqa: PLW0108
    })
except ImportError:
    pass

from . import controllers
from . import models
from . import utils
from . import wizard
