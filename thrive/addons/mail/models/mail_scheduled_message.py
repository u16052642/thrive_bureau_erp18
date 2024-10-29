# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from collections import defaultdict
import json

from thrive import _, api, fields, models
from thrive.addons.mail.tools.discuss import Store
from thrive.exceptions import AccessError, UserError, ValidationError
from thrive.tools.misc import clean_context

import logging

_logger = logging.getLogger(__name__)


class ScheduledMessage(models.Model):
    """ Scheduled message model (holds post values generated by the composer to delay the
    posting of the message). Different from mail.message.schedule that posts the message but
    delays the notification process.

    Todo: when adding support for scheduling messages in mass_mail mode, could add a reference to
    the "parent" composer (by making 'mail.compose.message' not transient anymore). This reference
    could then be used to cancel every message scheduled "at the same time" (from one composer),
    and to get the static 'notification parameters' (mail_server_id, auto_delete,...) instead of
    duplicating them for each scheduled message.
    Currently as scheduling is allowed in monocomment only, we don't have duplicates and we only
    have static notification parameters, but some will become dynamic when adding mass_mail support
    such as 'email_from' and 'force_email_lang'.
    """
    _name = 'mail.scheduled.message'
    _description = 'Scheduled Message'

    # content
    subject = fields.Char('Subject')
    body = fields.Html('Contents', sanitize_style=True)
    scheduled_date = fields.Datetime('Scheduled Date', required=True)
    attachment_ids = fields.Many2many(
        'ir.attachment', 'scheduled_message_attachment_rel',
        'scheduled_message_id', 'attachment_id',
        string='Attachments')

    # related document
    model = fields.Char('Related Document Model', required=True)
    res_id = fields.Many2oneReference('Related Document Id', model_field='model', required=True)

    # origin
    author_id = fields.Many2one('res.partner', 'Author', required=True)

    # recipients
    partner_ids = fields.Many2many('res.partner', string='Recipients')

    # characteristics
    is_note = fields.Boolean('Is a note', default=False, help="If the message will be posted as a Note.")

    # notify parameters (email_from, mail_server_id, force_email_lang,...)
    notification_parameters = fields.Text('Notification parameters')

    @api.constrains('model')
    def _check_model(self):
        if not all(model in self.pool and issubclass(self.pool[model], self.pool['mail.thread']) for model in self.mapped("model")):
            raise ValidationError(_("A message cannot be scheduled on a model that does not have a mail thread."))

    @api.constrains('scheduled_date')
    def _check_scheduled_date(self):
        if any(scheduled_message.scheduled_date < fields.Datetime().now() for scheduled_message in self):
            raise ValidationError(_("A Scheduled Message cannot be scheduled in the past"))

    # ------------------------------------------------------
    # CRUD / ORM
    # ------------------------------------------------------

    @api.model_create_multi
    def create(self, vals_list):
        # make sure user can post on the related records
        for vals in vals_list:
            self._check(vals)

        # clean context to prevent usage of default_model and default_res_id
        scheduled_messages = super(ScheduledMessage, self.with_context(clean_context(self.env.context))).create(vals_list)
        # transfer attachments from composer to scheduled messages
        for scheduled_message in scheduled_messages:
            if attachments := scheduled_message.attachment_ids:
                attachments.filtered(
                    lambda a: a.res_model == 'mail.compose.message' and not a.res_id and a.create_uid.id == self.env.uid
                ).write({
                    'res_model': scheduled_message._name,
                    'res_id': scheduled_message.id,
                })
        # schedule cron trigger
        if scheduled_messages:
            self.env.ref('mail.ir_cron_post_scheduled_message')._trigger_list(
                set(scheduled_messages.mapped('scheduled_date'))
            )
        return scheduled_messages

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None):
        """ Override that add specific access rights to only get the ids of the messages
        that are scheduled on the records on which the user has mail_post (or read) access
        """
        if self.env.is_superuser():
            return super()._search(domain, offset, limit, order)

        # don't use the ORM to avoid cache pollution
        query = super()._search(domain, offset, limit, order)
        fnames_to_read = ['id', 'model', 'res_id']
        rows = self.env.execute_query(query.select(
            *[self._field_to_sql(self._table, fname) for fname in fnames_to_read],
        ))

        # group res_ids by model and determine accessible records
        model_ids = defaultdict(set)
        for __, model, res_id in rows:
            model_ids[model].add(res_id)

        allowed_ids = defaultdict(set)
        for model, res_ids in model_ids.items():
            records = self.env[model].browse(res_ids)
            operation = getattr(records, '_mail_post_access', 'write')
            if records.has_access(operation):
                allowed_ids[model] = set(records._filtered_access(operation)._ids)

        scheduled_messages = self.browse(
            msg_id
            for msg_id, res_model, res_id in rows
            if res_id in allowed_ids[res_model]
        )

        return scheduled_messages._as_query(order)

    def unlink(self):
        self._check()
        return super().unlink()

    def write(self, vals):
        # prevent changing the records on which the messages are scheduled
        if vals.get('model') or vals.get('res_id'):
            raise UserError(_('You are not allowed to change the target record of a scheduled message.'))
        # make sure user can write on the record the messages are scheduled on
        self._check()
        res = super().write(vals)
        if new_scheduled_date := vals.get('scheduled_date'):
            self.env.ref('mail.ir_cron_post_scheduled_message')._trigger(fields.Datetime.to_datetime(new_scheduled_date))
        return res

    # ------------------------------------------------------
    # Actions
    # ------------------------------------------------------

    def open_edit_form(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _("Edit Scheduled Note") if self.is_note else _("Edit Scheduled Message"),
            'res_model': self._name,
            'view_mode': 'form',
            'views': [[False, 'form']],
            'target': 'new',
            'res_id': self.id,
        }

    def post_message(self):
        self.ensure_one()
        if self.env.is_admin() or self.create_uid.id == self.env.uid:
            self._post_message()
        else:
            raise UserError(_("You are not allowed to send this scheduled message"))

    def _post_message(self, raise_exception=True):
        """ Post the scheduled messages.
            They are posted using their creator as user so that one can check that the creator has
            still post permission on the related record, and to allow for the attachments to be
            transferred to the messages (see _process_attachments_for_post in mail.thread)
            if raise_exception is set to False, the method will skip the posting of a message
            instead of raising an error. This is useful when scheduled messages are sent from
            the _post_messages_cron
        """
        notification_parameters_whitelist = self._notification_parameters_whitelist()
        for scheduled_message in self:
            message_creator = scheduled_message.create_uid
            try:
                scheduled_message.with_user(message_creator)._check()
            except AccessError:
                if raise_exception:
                    raise
                _logger.info("Posting of scheduled message %s failed: user %s cannot post on the record", scheduled_message.id, message_creator.id)
                continue
            self.env[scheduled_message.model].browse(scheduled_message.res_id).with_user(message_creator).message_post(
                attachment_ids=list(scheduled_message.attachment_ids.ids),
                author_id=scheduled_message.author_id.id,
                body=scheduled_message.body,
                partner_ids=list(scheduled_message.partner_ids.ids),
                subtype_xmlid='mail.mt_note' if scheduled_message.is_note else 'mail.mt_comment',
                **{k: v for k, v in json.loads(scheduled_message.notification_parameters or '{}').items() if k in notification_parameters_whitelist},
            )
        self.unlink()

    # ------------------------------------------------------
    # Business Methods
    # ------------------------------------------------------

    @api.model
    def _check(self, values=None):
        """ Restrict the access to a scheduled message.
            Access is based on the record on which the scheduled message will be posted to.
            :param values: dict with model and res_id on which to perform the check
        """
        if self.env.is_superuser():
            return True

        model_ids = defaultdict(set)
        # sudo as anyways we check access on the related records
        for scheduled_message in self.sudo():
            model_ids[scheduled_message.model].add(scheduled_message.res_id)
        if values:
            model_ids[values['model']].add(values['res_id'])

        for model, res_ids in model_ids.items():
            records = self.env[model].browse(res_ids)
            operation = getattr(records, '_mail_post_access', 'write')
            records.check_access(operation)

    @api.model
    def _notification_parameters_whitelist(self):
        """ Parameters that can be used when posting the scheduled messages.
        """
        return {
            'email_add_signature',
            'email_from',
            'email_layout_xmlid',
            'force_email_lang',
            'mail_activity_type_id',
            'mail_auto_delete',
            'mail_server_id',
            'message_type',
            'model_description',
            'reply_to',
            'reply_to_force_new',
            'subtype_id',
        }

    @api.model
    def _post_messages_cron(self, limit=50):
        """ Posts past-due scheduled messages.
        """
        domain = [('scheduled_date', '<=', fields.Datetime.now())]
        messages_to_post = self.search(domain, limit=limit)
        _logger.info("Posting %s scheduled messages", len(messages_to_post))
        messages_to_post._post_message()

        # restart cron if needed
        if self.search_count(domain, limit=1):
            self.env('mail.ir_cron_post_scheduled_message')._trigger()

    def _to_store(self, store: Store):
        for scheduled_message in self:
            data = scheduled_message._read_format(['body', 'is_note', 'scheduled_date', 'subject'])[0]
            data['attachment_ids'] = Store.many(scheduled_message.attachment_ids)
            data['author'] = Store.one(scheduled_message.author_id)
            store.add(scheduled_message, data)