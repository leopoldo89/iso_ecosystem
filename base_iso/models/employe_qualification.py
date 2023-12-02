from odoo import api, models, fields


class HrEmployeeSkill(models.Model):

    _inherit = 'hr.employee.skill'

    # campi per verifica competenze
    requested_skill_level_id = fields.Many2one('hr.skill.level')
    attestati = fields.Text()
    accettabile = fields.Boolean()
    da_formare = fields.Boolean()
    note = fields.Text()
    qualification_id = fields.Many2one('hr.employee.qualification')
    job_id = fields.Many2one('hr.job')

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

    # todo valutare se popolare in automatico questa tabella con i dati presi direttamente dall'employee_id
    hr_skill_ids = fields.One2many('hr.employee.skill', 'qualification_id')


    # campi RNC
    rnc_filter_data_da = fields.Date()
    rnc_filter_data_a = fields.Date()
    non_conformita_ids = fields.One2many('quality.alert', 'employee_qualification_id')


    # campi formazione
    rnc_filter_data_formazione_da = fields.Date()
    rnc_filter_data_formazione_a = fields.Date()
    formazione_non_conformita_ids = fields.One2many('quality.alert', 'employee_formazione_qualification_id')