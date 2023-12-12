from odoo import api, models, fields


class ProjectObiettivo(models.Model):

    _name = 'project.obiettivo'

    project_id = fields.Many2one('project.project')
    name = fields.Char()
    descrizione = fields.Text()
    documentazione_ids = fields.One2many('evidenza.documentale', 'project_obiettivo_id')
    gruppo_lavoro_ids = fields.One2many('gruppo.lavoro.iso', 'project_obiettivo_id')
    budget_stimato = fields.Float()
    data_inizio = fields.Date()
    data_fine = fields.Date()

class ProjectProjectInherit(models.Model):

    _inherit = 'project.project'

    # campi anagrafica
    tipo_richiesta = fields.Selection([('interna', 'Interna'), ('esterna', 'Esterna')])
    codice_progetto = fields.Char()
    project_board_employee_ids = fields.Many2many('hr.employee')
    note_progetto = fields.Html()
    tipo_gestione_progetto = fields.Selection([('semplificata', 'Semplificata'), ('completa', 'Completa')])

    # campi info/dati
    rischi_ids = fields.Many2many('rischio.iso')
    opportunita_ids = fields.Many2many('opportunita.iso')
    audit_ids = fields.Many2many('processo.audit')
    processi_ids = fields.Many2many('processo.iso')
    documentazione_ids = fields.One2many('evidenza.documentale', 'project_id')

    # campi obiettivi risorse
    obiettivi_ids = fields.One2many('project.obiettivo', 'project_id')