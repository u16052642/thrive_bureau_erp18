# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive.addons.website_helpdesk_forum.controllers.website_forum import WebsiteForumHelpdesk


class WebsiteSlidesForumHelpdesk(WebsiteForumHelpdesk):

    def get_template_xml_id(self):
        return "website_helpdesk_slides_forum.helpdesk_forums"
