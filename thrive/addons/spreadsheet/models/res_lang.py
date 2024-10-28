# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

from thrive import api, models

from thrive.addons.spreadsheet.utils.formatting import (
    strftime_format_to_spreadsheet_date_format,
    strftime_format_to_spreadsheet_time_format,
)


class Lang(models.Model):
    _inherit = "res.lang"

    @api.model
    def get_locales_for_spreadsheet(self):
        """Return the list of locales available for a spreadsheet."""
        langs = self.with_context(active_test=False).search([])

        spreadsheet_locales = [lang._thrive_lang_to_spreadsheet_locale() for lang in langs]
        return spreadsheet_locales

    @api.model
    def _get_user_spreadsheet_locale(self):
        """Convert the thrive lang to a spreadsheet locale."""
        lang = self._lang_get(self.env.user.lang)
        return lang._thrive_lang_to_spreadsheet_locale()

    def _thrive_lang_to_spreadsheet_locale(self):
        """Convert an thrive lang to a spreadsheet locale."""
        return {
            "name": self.name,
            "code": self.code,
            "thousandsSeparator": self.thousands_sep,
            "decimalSeparator": self.decimal_point,
            "dateFormat": strftime_format_to_spreadsheet_date_format(self.date_format),
            "timeFormat": strftime_format_to_spreadsheet_time_format(self.time_format),
            "formulaArgSeparator": ";" if self.decimal_point == "," else ",",
            "weekStart": int(self.week_start),
        }
