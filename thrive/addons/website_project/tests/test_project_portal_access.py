# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from re import search

from thrive.tests import HttpCase

from thrive.addons.mail.controllers.thread import ThreadController
from thrive.addons.project.tests.test_project_sharing import TestProjectSharingCommon
from thrive.addons.website.tools import MockRequest


class TestProjectPortalAccess(TestProjectSharingCommon, HttpCase):
    def test_post_chatter_as_portal_user(self):
        message = self.get_project_share_link()
        share_link = str(message.body.split('href="')[1].split('">')[0])
        match = search(r"access_token=([^&]+)&amp;pid=([^&]+)&amp;hash=([^&]*)", share_link)
        access_token, pid, _hash = match.groups()

        with self.with_user('chell'), MockRequest(self.env, path=share_link):
            ThreadController().mail_message_post(
                thread_model='project.task',
                thread_id=self.task_no_collabo.id,
                post_data={'body': '(-b ±√[b²-4ac]) / 2a'},
                token=access_token,
                pid=pid,
                hash=_hash,
            )

        self.assertTrue(
            self.env['mail.message'].sudo().search([
                ('author_id', '=', self.user_portal.partner_id.id),
            ])
        )
