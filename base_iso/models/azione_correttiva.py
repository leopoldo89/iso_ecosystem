from odoo import api, models, fields


class AzioneCorrettivaProposta(models.Model):

    _name = 'azione.correttiva.proposta'

    name = fields.Char(string='Titolo')
    descrizione = fields.Text()
    employee_id = fields.Many2one('hr.employee')
    data_fine = fields.Date()
    azione_correttiva_id = fields.Many2one('azione.correttiva')


class AzioneCorrettivaSoluzione(models.Model):
    _name = 'azione.correttiva.soluzione'

    name = fields.Char(string='Titolo')
    data = fields.Date()
    attivita_da_svolgere = fields.Html()
    incaricato_employee_id = fields.Many2one('hr.employee')
    entro_il = fields.Date()
    risorse = fields.Text()
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id, required=True)
    budget = fields.Monetary(currency_field="currency_id")

    azione_correttiva_id = fields.Many2one('azione.correttiva')


class AzioneCorrettiva(models.Model):

    _name = 'azione.correttiva'

    # campi anagrafica
    name = fields.Char(string="N° AC")
    richiesta_employee_id = fields.Many2one('hr.employee')
    richiesta_il = fields.Date()
    descrizione = fields.Text()
    rdq_gruppo_ids = fields.One2many('gruppo.lavoro.iso', 'azione_correttiva_id', domain=[('tipologia_gruppo', '=', 'ac_anagrafica')])
    apertura_ac = fields.Boolean()
    data_apertura = fields.Date()
    importanza = fields.Selection(selection=[('bassa', 'Bassa'), ('media', 'Media'), ('alta', 'Alta')])
    processi_coinvolti_ids = fields.One2many('processo.iso.coinvolto', 'azione_correttiva_id')
    ac_data_risoluzione = fields.Datetime()
    # todo far diventare questo campo una tabella perchè può essere risolta sia da interni che da esterni contemporaneamente
    ac_risolta_da = fields.Many2one('hr.employee')
    validata_da = fields.Many2one('hr.employee')  # la validazione invece è sempre interna
    chiusura_ac = fields.Boolean()

    # campi rnc/documentazioni
    non_conformita_ids = fields.Many2many('quality.alert')
    documentazione_rnc_ids = fields.One2many('evidenza.documentale', 'azione_correttiva_id',
                                                  domain=[('sezione_modello', '=', 'ac_documentazione')])

    # campi descrizione eventi
    descrizione_fatti = fields.Html()
    valutazioni_iniziali = fields.Html()

    # campi azioni correttive
    azioni_gruppo_ids = fields.One2many('gruppo.lavoro.iso', 'azione_correttiva_id',
                                     domain=[('tipologia_gruppo', '=', 'ac_azioni')])
    proposte_ids = fields.One2many('azione.correttiva.proposta', 'azione_correttiva_id')
    soluzione_ids = fields.One2many('azione.correttiva.soluzione', 'azione_correttiva_id')

    # campi evidenze-soluzioni-esiti-validazione
    esito_finale = fields.Html()
    documentazione_supporto_ids = fields.One2many('evidenza.documentale', 'azione_correttiva_id',
                                             domain=[('sezione_modello', '=', 'ac_supporto')])
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id, required=True)
    consuntivo_costi = fields.Monetary(currency_field="currency_id")
    documentazione_chiusura_ids = fields.One2many('evidenza.documentale', 'azione_correttiva_id',
                                             domain=[('sezione_modello', '=', 'ac_chiusura')])

    anno = fields.Integer()

    riscontri = fields.Text()

    # relazioni ad altre entita
    processo_id = fields.Many2one('processo.iso')
    audit_id = fields.Many2one('processo.audit')
    audit_da_creare_id = fields.Many2one('processo.audit')
    quality_alert_id = fields.Many2one('quality.alert')