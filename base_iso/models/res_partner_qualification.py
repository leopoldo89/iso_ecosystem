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

class RapportoNonconformita(models.Model):

    _name = 'rapporto.nonconformita'
    #todo eliminare




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
    note_finali = fields.Html()
    cliente_utilizzabile = fields.Boolean()
    data_validazione = fields.Date()
    qsm = fields.Boolean(help="Quality System Manager")
    valutazione_finale = fields.Selection(selection=[('ideale', '1 - Ideale (85%-100%)'),
                                                     ('valido', '2 - Valido (70%-84%)'),
                                                     ('discreto', '3 - Discreto (55%-69%)'),
                                                     ('critico', '4 - Critico (50%-55%)'),
                                                     ('non_utilizzare', '5 - Non Utilizzare (40%-49%)'),
                                                     ('depennare', '6 - Depennare (0%-39%)')])

    # campi approfondimenti
    richieste_cliente = fields.Html()

    # campi sezione dati finanziari
    fatturato_ids = fields.One2many('res.partner.qualification.fatturato', 'qualification_id')
    patrimonio_ids = fields.One2many('res.partner.qualification.patrimonio', 'qualification_id')
    data_costituzione = fields.Date()
    indici_solvibilita = fields.Char()
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id, required=True)
    rapporto_fatturato_addetto = fields.Monetary(currency_field="currency_id")
    valutazione_finanziaria_id = fields.Many2one('qualification.financial.evaluation')

    # campi Certificazioni
    certificazioni_ids = fields.One2many('qualification.certificate', 'qualification_id')

    # campi progettazione
    tipo_progrettazione = fields.Selection(selection=[('interna', 'Interna'), ('esterna', 'esterna'), ('assente', 'Assente')])
    famiglia_prodotto = fields.Boolean()
    disegno_tecnico = fields.Boolean()
    prototipizzazione = fields.Boolean()
    sala_testing = fields.Boolean()
    note_progettazione = fields.Html()

    # campi organizzazione
    addetti_annuali_ids = fields.One2many('qualification.addetti.annuali', 'qualification_id')
    produzione_annuale_ids = fields.One2many('qualification.produzione.annuale', 'qualification_id')
    note_organizzazione = fields.Html()

    # campi prodotti e servizi
    articoli_ids = fields.Many2many('product.product')

    # campi RNC
    rnc_from_date = fields.Date()
    rnc_to_date = fields.Date()
    non_conformita_ids = fields.One2many('quality.alert', 'qualification_id')

    #campi qualita
    q_manuale_presente = fields.Selection(selection=[('si', 'SI'), ('no', 'NO'), ('non_applicabile', 'Non applicabile')])
    q_iscrizione_albi = fields.Selection(selection=[('si', 'SI'), ('no', 'NO'), ('non_applicabile', 'Non applicabile')])
    q_pianificazione_vendite_acquisti = fields.Selection(selection=[('si', 'SI'), ('no', 'NO'), ('non_applicabile', 'Non applicabile')])
    q_organigramma = fields.Selection(selection=[('si', 'SI'), ('no', 'NO'), ('non_applicabile', 'Non applicabile')])
    q_documentazione_qualita = fields.Selection(selection=[('si', 'SI'), ('no', 'NO'), ('non_applicabile', 'Non applicabile')])
    q_totale_qualita = fields.Selection(selection=[('scarso', '1-Scarso'), ('sufficiente', '2- Suff'),
                                                   ('buono', '3-Buono'), ('alto', '4-Alto')])
    q_note = fields.Html()


    #campi gestione ordini
    ordini_presente_catalogo = fields.Selection(selection=[('si', 'SI'), ('no', 'NO'), ('non_applicabile', 'Non applicabile')])
    ordini_aggiornamenti = fields.Selection(selection=[('si', 'SI'), ('no', 'NO'), ('non_applicabile', 'Non applicabile')])
    ordini_riesame = fields.Selection(selection=[('si', 'SI'), ('no', 'NO'), ('non_applicabile', 'Non applicabile')])
    ordini_responsabile = fields.Selection(selection=[('si', 'SI'), ('no', 'NO'), ('non_applicabile', 'Non applicabile')])
    ordini_orienta_acquisti = fields.Selection(selection=[('si', 'SI'), ('no', 'NO'), ('non_applicabile', 'Non applicabile')])
    ordini_pianificazione_acquisti = fields.Selection(selection=[('si', 'SI'), ('no', 'NO'), ('non_applicabile', 'Non applicabile')])
    ordini_totale_area = fields.Selection(selection=[('scarso', '1-Scarso'), ('sufficiente', '2- Suff'),
                                                     ('buono', '3-Buono'), ('alto', '4-Alto')])
    ordini_note = fields.Html()


    # campi controlli e riesami
    cr_riesami_fornitura = fields.Selection(selection=[('si', 'SI'), ('no', 'NO'), ('non_applicabile', 'Non applicabile')])
    cr_responsabilita_riesame = fields.Selection(selection=[('si', 'SI'), ('no', 'NO'), ('non_applicabile', 'Non applicabile')])
    cr_personale_qualificato = fields.Selection(selection=[('si', 'SI'), ('no', 'NO'), ('non_applicabile', 'Non applicabile')])
    cr_gestione_modifiche = fields.Selection(selection=[('si', 'SI'), ('no', 'NO'), ('non_applicabile', 'Non applicabile')])
    cr_dati_collaudo = fields.Selection(selection=[('si', 'SI'), ('no', 'NO'), ('non_applicabile', 'Non applicabile')])
    cr_doc_riferibile = fields.Selection(selection=[('si', 'SI'), ('no', 'NO'), ('non_applicabile', 'Non applicabile')])
    cr_totale_riesami = fields.Selection(selection=[('scarso', '1-Scarso'), ('sufficiente', '2- Suff'),
                                                   ('buono', '3-Buono'), ('alto', '4-Alto')])
    cr_note = fields.Html()


    # campi consegne e logistica
    cl_piani_ritiro = fields.Selection(selection=[('si', 'SI'), ('no', 'NO'), ('non_applicabile', 'Non applicabile')])
    cl_organizz_trasporti = fields.Selection(selection=[('si', 'SI'), ('no', 'NO'), ('non_applicabile', 'Non applicabile')])
    cl_rispetto_accordi = fields.Selection(selection=[('si', 'SI'), ('no', 'NO'), ('non_applicabile', 'Non applicabile')])
    cl_conferme_ricezione = fields.Selection(selection=[('si', 'SI'), ('no', 'NO'), ('non_applicabile', 'Non applicabile')])
    cl_gestione_resi = fields.Selection(selection=[('si', 'SI'), ('no', 'NO'), ('non_applicabile', 'Non applicabile')])
    cl_totale_logistica = fields.Float()
    cl_note = fields.Html()




