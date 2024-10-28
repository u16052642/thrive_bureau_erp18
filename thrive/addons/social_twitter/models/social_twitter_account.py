# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import models, fields


class SocialTwitterAccount(models.Model):
    _name = 'social.twitter.account'
    _description = 'Social X Account'

    name = fields.Char('Name')
    description = fields.Char('Description')
    twitter_id = fields.Char('X ID')
    image = fields.Binary('Image')

    twitter_searched_by_id = fields.Many2one('social.account', 'Searched by')
