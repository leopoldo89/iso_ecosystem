from odoo import api, models, fields


class ResPartnerFatturato(models.Model):
    _name = 'res.partner.qualification.fatturato'

    anno = fields.Integer()
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id, required=True)
    fatturato = fields.Monetary(currency_field="currency_id")
    qualification_id = fields.Many2one('res.partner.qualification')


class ResPartnerPatrimonio(models.Model):
    _name = 'res.partner.qualification.patrimonio'

    anno = fields.Integer()
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id, required=True)
    patrimonio = fields.Monetary(currency_field="currency_id")
    qualification_id = fields.Many2one('res.partner.qualification')


class QualificationFinancialEvaluation(models.Model):
    _name = 'qualification.financial.evaluation'

    name = fields.Char()


class QualificationCertificate(models.Model):
    _name = 'qualification.certificate'

    numero_norma = fields.Char()
    titolo_norma = fields.Char()
    validita = fields.Date()
    ente_certificazione = fields.Char()
    attachment = fields.Binary('Document', copy=False, attachment=True)
    attachment_name = fields.Char()
    qualification_id = fields.Many2one('res.partner.qualification')


class QualificationAddettiAnnuali(models.Model):
    _name = 'qualification.addetti.annuali'

    anno = fields.Integer()
    amministrazione = fields.Integer()
    commerciale = fields.Integer()
    produzione = fields.Integer()
    ufficio_tecnico = fields.Integer()
    logistica = fields.Integer()
    totale_addetti = fields.Integer(compute="_compute_numero_addetti")
    qualification_id = fields.Many2one('res.partner.qualification')

    def _compute_numero_addetti(self):
        for rec in self:
            rec.totale_addetti = rec.amministrazione + rec.commerciale + rec.produzione + rec.ufficio_tecnico + rec.logistica


class QualificationProduzioneAnnuale(models.Model):

    _name = 'qualification.produzione.annuale'

    anno = fields.Integer()
    reparto = fields.Char()
    percentuale = fields.Float()
    descrizione = fields.Text()
    qualification_id = fields.Many2one('res.partner.qualification')



class QualificaCliente(models.Model):
    _name = 'res.partner.qualification'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # campi anagrafica
    name = fields.Char()
    partner_id = fields.Many2one('res.partner')
    tipo_qualifica = fields.Selection(selection=[('iniziale', 'Iniziale'), ('periodica', 'Periodica')])
    data_qualifica = fields.Date()
    lead_auditor_ids = fields.Many2many('hr.employee')
    addetto_cliente = fields.Many2one('res.partner')
    periodicita = fields.Selection(selection=[('3_mesi', '3 Mesi'),
                                                  ('6_mesi', '6 Mesi'),
                                                  ('12_mesi', '12 Mesi'),
                                                  ('24_mesi', '24 Mesi')])

    # campi valutazione
    valutazione_finale = fields.Html()
    cliente_utilizzabile = fields.Boolean()
    data_validazione = fields.Date()
    qsm = fields.Boolean(help="Quality System Manager")

    # campi sezione dati finanziari
    fatturato_ids = fields.One2many('res.partner.qualification.fatturato', 'qualification_id')
    patrimonio_ids = fields.One2many('res.partner.qualification.patrimonio', 'qualification_id')
    anno_costituzione = fields.Integer()
    indici_solvibilita = fields.Text()
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id, required=True)
    rapporto_fatturato_addetto = fields.Monetary(currency_field="currency_id")
    valutazione_finanziaria_id = fields.Many2one('qualification.financial.evaluation')

    # campi Certificazioni
    certificazioni_ids = fields.One2many('qualification.certificate', 'qualification_id')

    # campi progettazione
    tipo_progrettazione = fields.Selection(selection=[('interna', 'Interna'),
                                                      ('esterna', 'esterna'),
                                                      ('assente', 'Assente')])
    famiglia_prodotto = fields.Boolean()
    disegno_tecnico = fields.Boolean()
    prototipizzazione = fields.Boolean()
    sala_testing = fields.Boolean()
    note_progettazione = fields.Boolean()

    # campi organizzazione
    addetti_annuali_ids = fields.One2many('qualification.addetti.annuali', 'qualification_id')
    produzione_annuale_ids = fields.One2many('qualification.produzione.annuale', 'qualification_id')
    note_organizzazione = fields.Html()

    # campi prodotti e servizi
    articoli_ids = fields.Many2many('product.product')
