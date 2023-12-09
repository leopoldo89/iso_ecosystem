from odoo import api, models, fields

class ProcessoIsoRnc(models.Model):

    _name = 'processo.iso.coinvolto'
    processo_id = fields.Many2one('processo.iso')
    tipo = fields.Selection(selection=[('primario', 'Primario'), ('supporto', 'Supporto'), ('sistema', 'Sistema')])
    quality_alert_id = fields.Many2one('quality.alert')
    azione_correttiva_id = fields.Many2one('azione.correttiva')

class RapportoNonconformitaAlert(models.Model):

    _inherit = 'quality.alert'

    # campi angrafica
    tipo = fields.Selection([('interna', 'Interna'), ('esterna', 'Esterna')])
    richiesta_interna_id = fields.Many2one('hr.employee')
    richiesta_esterna_id = fields.Many2one('res.partner')
    rilevata_il = fields.Date()
    nc_data = fields.Datetime(string="NC del")
    autorizzata_da = fields.Many2one('hr.employee')
    apertura_rdq = fields.Boolean()
    data_apertura = fields.Date()
    urgenza = fields.Selection(selection=[('bassa', 'Bassa'), ('media', 'Media'), ('alta', 'Alta')])
    processi_coinvolti_ids = fields.One2many('processo.iso.coinvolto', 'quality_alert_id')
    nc_data_risoluzione = fields.Datetime()
    # todo far diventare questo campo una tabella perchè può essere risolta sia da interni che da esterni contemporaneamente
    nc_risolta_da = fields.Many2one('hr.employee')
    validata_da = fields.Many2one('hr.employee') # la validazione invece è sempre interna
    chiusura_rdq = fields.Boolean()

    # campi descrizione
    imputato_a = fields.Selection(selection=[('dependente', 'Dipendente'), ('cliente', 'Cliente'), ('fornitore', 'Fornitore')])
    imputato_employee_id = fields.Many2one('hr.employee')
    imputato_partner_id = fields.Many2one('res.partner')
    nc_tipologia = fields.Selection([('interna', 'Interna'), ('esterna', 'Esterna')])
    classe = fields.Selection([('applicazione', 'Applicazione'), ('Documentazione', 'documentazione')])
    documentazione_supporto_ids = fields.One2many('evidenza.documentale', 'quality_alert_id',
                                                  domain=[('sezione_modello', '=', 'rnc_descrizione')])
    note_descrizione = fields.Html()

    # campi analisi
    cosa_successo = fields.Html()
    cause_individuate = fields.Html()
    azioni_da_intraprendere = fields.Html()
    entro_il = fields.Date()
    gravita = fields.Selection(selection=[('bassa', 'Bassa'), ('media', 'Media'), ('alta', 'Alta')])
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id, required=True)
    nc_costo = fields.Monetary(currency_field="currency_id")

    # campi trattamento
    nc_gruppo_ids = fields.One2many('gruppo.lavoro.iso', 'quality_alert_id')
    azioni_correttive_ids = fields.One2many('azione.correttiva', 'quality_alert_id')
    esito_finale = fields.Html()
    documentazione_chiusura_ids = fields.One2many('evidenza.documentale', 'quality_alert_id',
                                                  domain=[('sezione_modello', '=', 'rnc_trattamento')])

    # relazioni ad altre entita
    qualification_id = fields.Many2one('res.partner.qualification')
    satisfaction_id = fields.Many2one('res.partner.satisfaction')
    employee_qualification_id = fields.Many2one('hr.employee.qualification')
    employee_formazione_qualification_id = fields.Many2one('hr.employee.qualification')
    processo_id = fields.Many2one('processo.iso')
    audit_id = fields.Many2one('processo.audit')