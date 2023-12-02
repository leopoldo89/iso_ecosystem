from odoo import api, models, fields

class QualificaCliente(models.Model):
    _name = 'res.partner.satisfaction'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # campi anagrafica
    partner_id = fields.Many2one('res.partner')
    data_verifica = fields.Date()
    lead_auditor_ids = fields.Many2many('hr.employee')
    tipo_verifica = fields.Selection(selection=[('Meeting', 'Meeting'), ('videocall', 'VideoCall'),
                                                ('call', 'Call'), ('questionario', 'Questionario'),
                                                ('analisi_risultanze', 'Analisi su risultanze')])
    addetto_vendite_id = fields.Many2one('res.partner')
    periodicita = fields.Selection(selection=[('3_mesi', '3 Mesi'),
                                                  ('6_mesi', '6 Mesi'),
                                                  ('12_mesi', '12 Mesi'),
                                                  ('24_mesi', '24 Mesi')])


    # campi valutazione
    totale_valutazione = fields.Selection(selection=[('scarso', '1-Scarso'), ('sufficiente', '2- Suff'),
                                                     ('buono', '3-Buono'), ('alto', '4-Alto')])
    puntualita = fields.Selection(selection=[('scarso', '1-Scarso'), ('sufficiente', '2- Suff'),
                                                     ('buono', '3-Buono'), ('alto', '4-Alto')])
    servizio_fornito = fields.Selection(selection=[('scarso', '1-Scarso'), ('sufficiente', '2- Suff'),
                                                     ('buono', '3-Buono'), ('alto', '4-Alto')])
    assistenza_post_vendita = fields.Selection(selection=[('scarso', '1-Scarso'), ('sufficiente', '2- Suff'),
                                                     ('buono', '3-Buono'), ('alto', '4-Alto')])
    supporto_tecnico = fields.Selection(selection=[('scarso', '1-Scarso'), ('sufficiente', '2- Suff'),
                                                     ('buono', '3-Buono'), ('alto', '4-Alto')])
    amministrazione = fields.Selection(selection=[('scarso', '1-Scarso'), ('sufficiente', '2- Suff'),
                                                     ('buono', '3-Buono'), ('alto', '4-Alto')])
    note_finali = fields.Html()
    richieste_partner = fields.Html()
    data_next_audit = fields.Date()


    # campi RNC
    rnc_filter_data_da = fields.Date()
    rnc_filter_data_a = fields.Date()
    non_conformita_ids = fields.One2many('quality.alert', 'satisfaction_id')
