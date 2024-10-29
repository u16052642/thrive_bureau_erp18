# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.


from thrive import models, fields, _


class SaleCommissionReport(models.Model):
    _name = "sale.commission.report"
    _description = "Sales Commission Report"
    _order = 'id'
    _auto = False

    target_id = fields.Many2one('sale.commission.plan.target', "Period", readonly=True)
    target_amount = fields.Monetary("Target Amount", readonly=True, currency_field='currency_id')
    plan_id = fields.Many2one('sale.commission.plan', "Commission Plan", readonly=True)
    user_id = fields.Many2one('res.users', "Sales Person", readonly=True)
    team_id = fields.Many2one('crm.team', "Sales Team", readonly=True)
    achieved = fields.Monetary("Achieved", readonly=True, currency_field='currency_id')
    achieved_rate = fields.Float("Achieved Rate", readonly=True)
    commission = fields.Monetary("Commission", readonly=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', "Currency", readonly=True)
    company_id = fields.Many2one('res.company', string='Company', readonly=True)
    payment_date = fields.Date("Payment Date", readonly=True)
    forecast_id = fields.Many2one('sale.commission.plan.target.forecast', 'fc')
    forecast = fields.Monetary("Forecast", readonly=True, currency_field='currency_id')

    def action_achievement_detail(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "sale.commission.achievement.report",
            "name": _('Commission Detail: %(name)s', name=self.target_id.name),
            "views": [[self.env.ref('sale_commission.sale_achievement_report_view_list').id, "list"]],
            "context": {'commission_user_ids': self.user_id.ids, 'commission_team_ids': self.team_id.ids},
            "domain": [('target_id', '=', self.target_id.id), ('user_id', '=', self.user_id.id), ('team_id', '=', self.team_id.id)],
        }

    def write(self, values):
        # /!\ Do not call super as the table doesn't exist
        if 'forecast' in values:
            amount = values['forecast']
            for line in self:
                if line.forecast_id:
                    line.forecast_id.amount = amount
                else:
                    line.forecast_id = self.env['sale.commission.plan.target.forecast'].create({
                        'target_id': line.target_id.id,
                        'amount': amount,
                        'plan_id': line.plan_id.id,
                        'user_id': line.user_id.id,
                    })
            # Update the field's cache otherwise the field reset to the original value on the field
            self.env.cache._set_field_cache(self, self._fields.get('forecast')).update(dict.fromkeys(self.ids, amount))
        return True

    @property
    def _table_query(self):
        users = self.env.context.get('commission_user_ids', [])
        if users:
            users = self.env['res.users'].browse(users).exists()
        teams = self.env.context.get('commission_team_ids', [])
        if teams:
            teams = self.env['crm.team'].browse(teams).exists()
        return f"""
WITH {self.env['sale.commission.achievement.report']._commission_lines_query(users=users, teams=teams)},
achievement AS (
    SELECT
        ROW_NUMBER() OVER (ORDER BY MAX(era.date_to) DESC, cl.user_id) AS id,
        era.id AS target_id,
        cl.plan_id AS plan_id,
        cl.user_id AS user_id,
        MIN(cl.team_id) AS team_id,
        cl.company_id AS company_id,
        GREATEST(SUM(achieved), 0) AS achieved,
        CASE
            WHEN MAX(era.amount) > 0 THEN GREATEST(SUM(achieved), 0) / MAX(era.amount)
            ELSE 0
        END AS achieved_rate,
        cl.currency_id AS currency_id,
        MAX(era.amount) AS amount,
        MAX(era.date_to) AS payment_date,
        MAX(scpf.id) AS forecast_id,
        MAX(scpf.amount) AS forecast
    FROM commission_lines cl
    JOIN sale_commission_plan_target era
        ON cl.plan_id = era.plan_id
        AND cl.date >= era.date_from
        AND cl.date <= era.date_to
    LEFT JOIN sale_commission_plan_target_forecast scpf
        ON (scpf.target_id = era.id AND cl.user_id = scpf.user_id)
    GROUP BY
        era.id,
        cl.plan_id,
        cl.user_id,
        cl.company_id,
        cl.currency_id
), target_com AS (
    SELECT
        amount AS before,
        target_rate AS rate_low,
        LEAD(amount) OVER (PARTITION BY plan_id ORDER BY target_rate) AS amount,
        LEAD(target_rate) OVER (PARTITION BY plan_id ORDER BY target_rate) AS rate_high,
        plan_id
    FROM sale_commission_plan_target_commission scpta
    JOIN sale_commission_plan scp ON scp.id = scpta.plan_id
    WHERE scp.type = 'target'
), achievement_target AS (
    SELECT
        a.id,
        a.target_id,
        a.plan_id,
        a.user_id,
        a.team_id,
        a.company_id,
        a.payment_date,
        a.currency_id,
        a.achieved,
        a.achieved_rate,
        a.amount AS target_amount,
        a.forecast,
        a.forecast_id,
        CASE
            WHEN tc.before IS NULL THEN a.achieved
            WHEN tc.rate_high IS NULL THEN tc.before
            ELSE tc.before + (tc.amount - tc.before) * (a.achieved_rate - tc.rate_low) / (tc.rate_high - tc.rate_low)
        END AS commission
    FROM achievement a
    LEFT JOIN target_com tc ON (
        tc.plan_id = a.plan_id AND
        tc.rate_low <= a.achieved_rate AND
        (tc.rate_high IS NULL OR tc.rate_high > a.achieved_rate)
    )
)
SELECT * FROM achievement_target
"""