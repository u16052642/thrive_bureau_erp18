import csv
import io

from thrive import models, fields, _
from thrive.exceptions import UserError


class AccountBatchPayment(models.Model):
    _inherit = 'account.batch.payment'

    country_code = fields.Char(
        string="Country Code",
        related='journal_id.country_code',
    )

    def generate_pay_order(self):
        journal = self.journal_id
        if not journal.enet_template_field_ids:
            raise UserError(_("Please configure the bank template in the %s Journal to generate the csv file.", journal.name))
        attachment = self.env['ir.attachment'].create({
            'name': f"{self.name}_payorder.csv",
            'raw': self.get_csv_data(),
            'res_model': 'account.batch.payment',
            'res_id': self.id,
            'can_be_deleted': False
        })

        self.message_post(
            subject=_("Payorder CSV file"),
            body=_("Payorder has been generated by %s", self.env.user.name),
            attachment_ids=[attachment.id])

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'type': 'success',
                'sticky': False,
                'message': _('Payorder has been generated successfully!.'),
                'next': {'type': 'ir.actions.act_window_close'},
            },
        }

    def get_csv_data(self):
        template_fields = self.journal_id.enet_template_field_ids.sorted('sequence')
        header = template_fields.mapped('label')
        field_paths = template_fields.mapped(lambda field: field.field_name or '')
        rows = [
            self._get_value_from_field_path(payment_record, field_paths)
            for payment_record in self.payment_ids
        ]
        with io.StringIO() as csv_output:
            csv_writer = csv.writer(csv_output)
            csv_writer.writerow(header)
            csv_writer.writerows(rows)
            return csv_output.getvalue()

    def _get_value_from_field_path(self, payment, fields_path):
        values = []
        for field_path in fields_path:
            if field_path:
                field_value = payment
                for part in field_path.split('.'):
                    if isinstance(field_value, models.Model):
                        field_value = field_value[part] if part in field_value._fields else ''
                    else:
                        field_value = ''
                        break
                values.append(field_value or '')
            else:
                values.append('')
        return values
