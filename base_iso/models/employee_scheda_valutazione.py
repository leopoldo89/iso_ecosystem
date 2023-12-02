from odoo import fields, api, models


class EmployeeSchedaValutazione(models.Model):

    _name = "employee.scheda.valutazione"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # campi anagrafica
    employee_id = fields.Many2one('hr.employee')
    deciso_da_employee_id = fields.Many2one('hr.employee')
    deciso_il = fields.Date()
    argomento_formazione = fields.Text()
    tipo = fields.Selection(selection=[('interno', 'Interno'), ('esterno', 'esterno'), ('autonomo', 'Autonomo')])
    tutor_interno_id = fields.Many2one('hr.employee')
    tutor_esterno_id = fields.Many2one('res.partner')
    entro_il = fields.Date()


    # campi fruizione
    f_iniziata_il = fields.Date()
    f_terminata_il = fields.Date()
    f_esito = fields.Html()
    f_attachment = fields.Binary('Document', copy=False, attachment=True)
    f_attachment_name = fields.Char()
    f_note = fields.Html()
    f_verificare_entro_il = fields.Date()


    # campi verifica/efficacia
    v_vericatore_interno_id = fields.Many2one('hr.employee')
    v_verificato_il = fields.Date()
    v_risultato = fields.Html()
    v_efficacia = fields.Html()
    v_valutazione = fields.Selection(selection=[('scarso', '1-Scarso'), ('sufficiente', '2- Suff'),
                                                   ('buono', '3-Buono'), ('alto', '4-Alto')])
    v_validato_da_id = fields.Many2one('hr.employee')
    v_riprendere_il = fields.Date()
    v_note_finali = fields.Html()



