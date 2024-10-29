# -*- coding: utf-8 -*-

from thrive.modules.registry import Registry

def migrate(cr, version):
    registry = Registry(cr.dbname)
    from thrive.addons.account.models.chart_template import migrate_set_tags_and_taxes_updatable
    migrate_set_tags_and_taxes_updatable(cr, registry, 'l10n_ch')
