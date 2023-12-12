from odoo import api, models, fields


class GruppoLavoroIso(models.Model):
    _name = 'gruppo.lavoro.iso'

    employee_id = fields.Many2one('hr.employee')
    partner_id = fields.Many2one('res.partner')
    nome = fields.Char(compute="_compute_nome")
    job_id = fields.Char(compute="_compute_fa_id")
    incarico = fields.Text()

    # campo utile quando bisogna avere più tabelle O2M di evidenza documentale in uno stesso modello
    # serve per mettere un domain ai campi o2m
    tipologia_gruppo = fields.Selection(selection=[('ro_anagrafica', 'ro_anagrafica'),  ('ro_obiettivi', 'ro_obiettivi'),
                                                   ('ro_azioni', 'ro_azioni'), ('ro_risorse', 'ro_risorse'), ('ro_piano', 'ro_piano'),
                                                   ('ro_efficacia', 'ro_efficacia'), ('ac_anagrafica', 'ac_anagrafica'),
                                                   ('ac_azioni', ('ac_azioni'))])

    # campi relazionali
    risk_opp_id = fields.Many2one('risk.opportunity.base')
    quality_alert_id = fields.Many2one('quality.alert')
    azione_correttiva_id = fields.Many2one('azione.correttiva')
    project_id = fields.Many2one('project.project')
    project_obiettivo_id = fields.Many2one('project.obiettivo')

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.partner_id:
            self.employee_id = False
            self._compute_fa_id()
            self._compute_nome()

    @api.onchange('employee_id')
    def onchange_employee_id(self):
        if self.employee_id:
            self.partner_id = False
            self._compute_fa_id()
            self._compute_nome()
    def _compute_nome(self):
        for rec in self:
            if rec.employee_id:
                rec.nome = rec.employee_id.name
            if rec.partner_id:
                rec.nome = rec.partner_id.nome

    def _compute_fa_id(self):
        for rec in self:
            if rec.employee_id and rec.employee_id.job_id:
                rec.job_id = rec.employee_id.job_id.id
            if rec.partner_id:
                rec.job_id = rec.partner_id.job_id.id