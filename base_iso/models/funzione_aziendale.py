from odoo import fields, api, models
class HrJobQualifica(models.Model):

    _name = "hr.job.qualifica"

    name = fields.Char()
    riferimenti_legge = fields.Char()
    punteggio_minimo = fields.Char()
    note = fields.Text()
    job_id = fields.Many2one('hr.job')


class HrJobInherit(models.Model):

    _inherit = "hr.job"

    sigla_fa = fields.Char()
    livello_gerarchia = fields.Selection(selection=[("1", "1°"), ("2", "2°"), ("3", "3°"), ("4", "4°"), ("5", "5°")])
    risponde_a = fields.Many2one('hr.employee')
    responsible_employee_ids = fields.Many2many('hr.employee')
    parent_id = fields.Many2one('hr.job')
    child_ids = fields.One2many('hr.job', 'parent_id')

    qualifiche_ids = fields.One2many('hr.job.qualifica', 'job_id')
    skill_ids = fields.Many2many('hr.employee.skill', 'job_id')


class HrJobEmployee(models.Model):

    _inherit = "hr.employee"

    def name_get(self):
        result = []
        for employee in self:
            name = employee.name
            if employee.job_id:
                name += ' - ' + employee.job_id.name
            result.append((employee.id, name))
        return result

