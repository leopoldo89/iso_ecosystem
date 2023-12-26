from odoo import models, api, fields


class SiglaCollaboratore(models.Model):

    _name = 'sigla.collaboratore'

    name = fields.Char()

class FunzioniSvolte(models.Model):

    _name = 'hr.job.svolta'

    job_id = fields.Many2one('hr.job', required=1)
    sigla_fa = fields.Char(related='job_id.sigla_fa')
    livello_gerarchia = fields.Selection(selection=[("1", "1°"), ("2", "2°"), ("3", "3°"), ("4", "4°"), ("5", "5°")],
                                         related='job_id.livello_gerarchia')
    superiorie_id = fields.Many2one('hr.employee')
    employee_id = fields.Many2one('hr.employee')

    def name_get(self):
        result = []
        for fa_svolta in self:
            result.append((fa_svolta.id, fa_svolta.job_id.name))
        return result


class HrEmployee(models.Model):

    _inherit = 'hr.employee'
    sigla_collaboratore_id = fields.Many2one('sigla.collaboratore')
    data_assunzione = fields.Date()
    fa_svolte_ids = fields.One2many('hr.job.svolta', 'employee_id')
    department_ids = fields.Many2many('hr.department')

