# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

"""
ThriveERP - Server
ThriveERP is an ERP+CRM program for small and medium businesses.

The whole source code is distributed under the terms of the
GNU Public Licence.

(c) 2003-TODAY, Fabien Pinckaers - ThriveERP SA
"""

import atexit
import csv # pylint: disable=deprecated-module
import logging
import os
import re
import sys
from pathlib import Path

from psycopg2.errors import InsufficientPrivilege

import thrive

from . import Command

__author__ = thrive.release.author
__version__ = thrive.release.version

# Also use the `thrive` logger for the main script.
_logger = logging.getLogger('thrive')

re._MAXCACHE = 4096  # default is 512, a little too small for thrive

def check_root_user():
    """Warn if the process's user is 'root' (on POSIX system)."""
    if os.name == 'posix':
        import getpass
        if getpass.getuser() == 'root':
            sys.stderr.write("Running as user 'root' is a security risk.\n")

def check_postgres_user():
    """ Exit if the configured database user is 'postgres'.

    This function assumes the configuration has been initialized.
    """
    config = thrive.tools.config
    if (config['db_user'] or os.environ.get('PGUSER')) == 'postgres':
        sys.stderr.write("Using the database user 'postgres' is a security risk, aborting.")
        sys.exit(1)

def report_configuration():
    """ Log the server version and some configuration values.

    This function assumes the configuration has been initialized.
    """
    config = thrive.tools.config
    _logger.info("Thrive version %s", __version__)
    if os.path.isfile(config.rcfile):
        _logger.info("Using configuration file at " + config.rcfile)
    _logger.info('addons paths: %s', thrive.addons.__path__)
    if config.get('upgrade_path'):
        _logger.info('upgrade path: %s', config['upgrade_path'])
    host = config['db_host'] or os.environ.get('PGHOST', 'default')
    port = config['db_port'] or os.environ.get('PGPORT', 'default')
    user = config['db_user'] or os.environ.get('PGUSER', 'default')
    _logger.info('database: %s@%s:%s', user, host, port)
    replica_host = config['db_replica_host']
    replica_port = config['db_replica_port']
    if replica_host is not False or replica_port:
        _logger.info('replica database: %s@%s:%s', user, replica_host or 'default', replica_port or 'default')
    if sys.version_info[:2] > thrive.MAX_PY_VERSION:
        _logger.warning("Python %s is not officially supported, please use Python %s instead",
            '.'.join(map(str, sys.version_info[:2])),
            '.'.join(map(str, thrive.MAX_PY_VERSION))
        )

def rm_pid_file(main_pid):
    config = thrive.tools.config
    if config['pidfile'] and main_pid == os.getpid():
        try:
            os.unlink(config['pidfile'])
        except OSError:
            pass

def setup_pid_file():
    """ Create a file with the process id written in it.

    This function assumes the configuration has been initialized.
    """
    config = thrive.tools.config
    if not thrive.evented and config['pidfile']:
        pid = os.getpid()
        with open(config['pidfile'], 'w') as fd:
            fd.write(str(pid))
        atexit.register(rm_pid_file, pid)

def export_translation():
    config = thrive.tools.config
    dbname = config['db_name']

    if config["language"]:
        msg = "language %s" % (config["language"],)
    else:
        msg = "new language"
    _logger.info('writing translation file for %s to %s', msg,
        config["translate_out"])

    fileformat = os.path.splitext(config["translate_out"])[-1][1:].lower()
    # .pot is the same fileformat as .po
    if fileformat == "pot":
        fileformat = "po"

    with open(config["translate_out"], "wb") as buf:
        registry = thrive.modules.registry.Registry.new(dbname)
        with registry.cursor() as cr:
            thrive.tools.translate.trans_export(config["language"],
                config["translate_modules"] or ["all"], buf, fileformat, cr)

    _logger.info('translation file written successfully')

def import_translation():
    config = thrive.tools.config
    overwrite = config["overwrite_existing_translations"]
    dbname = config['db_name']

    registry = thrive.modules.registry.Registry.new(dbname)
    with registry.cursor() as cr:
        translation_importer = thrive.tools.translate.TranslationImporter(cr)
        translation_importer.load_file(config["translate_in"], config["language"])
        translation_importer.save(overwrite=overwrite)

def main(args):
    check_root_user()
    thrive.tools.config.parse_config(args, setup_logging=True)
    check_postgres_user()
    report_configuration()

    config = thrive.tools.config

    # the default limit for CSV fields in the module is 128KiB, which is not
    # quite sufficient to import images to store in attachment. 500MiB is a
    # bit overkill, but better safe than sorry I guess
    csv.field_size_limit(500 * 1024 * 1024)

    preload = []
    if config['db_name']:
        preload = config['db_name'].split(',')
        for db_name in preload:
            try:
                thrive.service.db._create_empty_database(db_name)
                config['init']['base'] = True
            except InsufficientPrivilege as err:
                # We use an INFO loglevel on purpose in order to avoid
                # reporting unnecessary warnings on build environment
                # using restricted database access.
                _logger.info("Could not determine if database %s exists, "
                             "skipping auto-creation: %s", db_name, err)
            except thrive.service.db.DatabaseExists:
                pass

    if config["translate_out"]:
        export_translation()
        sys.exit(0)

    if config["translate_in"]:
        import_translation()
        sys.exit(0)

    stop = config["stop_after_init"]

    setup_pid_file()
    rc = thrive.service.server.start(preload=preload, stop=stop)
    sys.exit(rc)

class Server(Command):
    """Start the thrive server (default command)"""
    def run(self, args):
        thrive.tools.config.parser.prog = f'{Path(sys.argv[0]).name} {self.name}'
        main(args)
