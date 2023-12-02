from odoo import api, models, fields


# class HrEmployeeSkill(models.Model):
#     _inherit = 'hr.employee.skill'
#     requested_skill_leveò_id = fields.Many2one('hr.skill.level')

class QualificaDipendente(models.Model):
    _name = 'hr.employee.qualification'
    _inherit = ['mail.thread', 'mail.activity.mixin']



    # campi anagrafica
    employee_id = fields.Many2one('hr.employee')
    tipo_qualifica = fields.Selection(selection=[('iniziale', 'Iniziale'), ('periodica', 'Periodica')])
    data_qualifica = fields.Date()
    data_prev_qualifica = fields.Date()
    funzione_aziendale_id = fields.Many2one('hr.job', related='employee_id.job_id')
    verifier_employee_id = fields.Many2one('hr.employee')


    # campi valutazione
    valutazione_finale = fields.Selection(selection=[('basso', 'Basso'), ('sufficiente', 'Sufficiente'),
                                                     ('medio', 'Medio'), ('alto', 'Alto')])
    note_finali = fields.Html()
    richieste_partner = fields.Html()
    data_next_qualifica = fields.Date()

    formazione_pianificata = fields.Char()
    entro_il = fields.Date()
    ingaggiabile = fields.Boolean()


