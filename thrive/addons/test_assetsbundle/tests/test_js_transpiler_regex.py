# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive.tests import tagged
from thrive.tests.common import TransactionCase
from thrive.tools import URL_RE, THRIVE_MODULE_RE

@tagged('post_install', '-at_install')
class TestJsTranspiler(TransactionCase):

    def test_correct_THRIVE_MODULE_RE(self):
        cases = [
            '// @thrive-module',
            '//@thrive-module',
            '/* @thrive-module',
            '/** @thrive-module',
            '/*@thrive-module',
            '/**@thrive-module',
            '// @thrive-module alias=web.test',
            '/* @thrive-module  alias=web.test',
            '/** @thrive-module  alias=web.test',
            '/** @thrive-module  alias=web.test**/',
            '/* @thrive-module  alias=web.test ',
            '/* @thrive-module alias=web.test default=false',
            '/* @thrive-module alias=web.test default=false ',
            '/* @thrive-module alias=web.test default=false**/',
        ]

        for case in cases:
            assert THRIVE_MODULE_RE.match(case), "URL_RE is failing... >%s<" % case
            if "alias" in case:
                assert THRIVE_MODULE_RE.match(case).groupdict().get('alias'), "URL_RE is failing for alias... >%s<" % case
                assert THRIVE_MODULE_RE.match(case).groupdict().get('alias') == "web.test", "URL_RE does not get the right alias for ... >%s<" % case
            if "default" in case:
                assert THRIVE_MODULE_RE.match(case).groupdict().get('default'), "URL_RE is failing for default... >%s<" % case
                assert THRIVE_MODULE_RE.match(case).groupdict().get('default') == "false", "URL_RE does not get the right default for ... >%s<" % case

    def test_incorrect_THRIVE_MODULE_RE(self):
        cases = [
            '/* @thrive-module alias = web.test ',
            '/* @thrive-module alias= web.test',
            '/* @thrive-module alias = web.test default=false'
        ]

        for case in cases:
            assert not THRIVE_MODULE_RE.match(case).groupdict().get('alias'), "URL_RE should fail because of too much spaces but didn't... >%s<" % case

        cases = [
            '// @thrive-modulealias=web.test',
            '/* @thrive-module alias=web.testdefault=false',
        ]

        for case in cases:
            if "alias" in case and "default" in case:
                assert \
                    not THRIVE_MODULE_RE.match(case).groupdict().get('alias') \
                    or \
                    not THRIVE_MODULE_RE.match(case).groupdict().get('default'), "URL_RE should fail for alias and default... >%s<" % case
            elif "alias" in case:
                assert not THRIVE_MODULE_RE.match(case).groupdict().get('alias'), "URL_RE should fail for alias... >%s<" % case

    def test_correct_URL_RE(self):
        cases = [
            'web/static/src/js/file.js',
            '/web/static/src/js/file.js',
            '/web/other/static/src/js/file.js',
            '/web/other/static/src/file.js',
            '/web/other/static/tests/file.js',
            '/web/other/static/src/another/and/file.js',
            '/web/other-o/static/src/another/and/file.js',
            '/web-o/other-o/static/src/another/and/file.js',
        ]

        for case in cases:
            assert URL_RE.fullmatch(case), "URL RE failed... %s" % case

    def test_incorrect_URL_RE(self):
        cases = [
            'web/static/js/src/file.js',                          # src after js
            'web/static/js/file.js',                              # no src or tests folder
        ]

        for case in cases:
            assert not URL_RE.fullmatch(case), "URL RE should have failed... %s" % case
