from odoo import api, models, fields


class ProcessoIsoRnc(models.Model):

    _name = 'processo.iso.coinvolto'
    processo_id = fields.Many2one('processo.iso', required=True)
    tipo = fields.Selection(selection=[('primario', 'Primario'), ('supporto', 'Supporto'), ('sistema', 'Sistema')])
    quality_alert_id = fields.Many2one('quality.alert')
    azione_correttiva_id = fields.Many2one('azione.correttiva')


    def update_processo_iso(self, processo_id, old_processo_id, quality_alert_id):
        """funzione per prendere il processo coinvolto inserito nella rnc e
            collegare/scollegare dunque la rnc al processo iso"""

        # aggancio rnc a processo coinvolto
        if processo_id:
            nuovo_processo_id = self.env['processo.iso'].browse(processo_id)
            nuovo_processo_id.write({'non_conformita_ids': [(4, quality_alert_id)]})

        # scollego rnc da processo coinvolto
        if old_processo_id:
            old_processo_id = self.env['processo.iso'].browse(old_processo_id)
            old_processo_id.write({'non_conformita_ids': [(3, quality_alert_id)]})

    def write(self, vals):
        """modifico la relazione rnc-processo solo se è cambianto il processo_id del processo coinvolto"""

        for rec in self:
            new_processo_id = vals.get('processo_id', False)

            # modifica processo sgancio la rnc dal vecchio processo e la aggancio al nuovo
            if new_processo_id and rec.processo_id and rec.processo_id.id != new_processo_id and rec.quality_alert_id:
                rec.update_processo_iso(new_processo_id, rec.processo_id.id, rec.quality_alert_id.id)

        res = super(ProcessoIsoRnc, self).write(vals)
        return res

    @api.model_create_multi
    def create(self, vals_list):
        """creo un processo coinvolto significa che devo aggancianre la rnc al processo iso che sto aggiunendo"""

        created_records = super().create(vals_list)
        for rec in created_records:
            if rec.processo_id and rec.quality_alert_id:
                self.update_processo_iso(rec.processo_id.id, False, rec.quality_alert_id.id)

        return created_records

    def unlink(self):
        """eliminio la riga di processo coinvolto dunque bisogna sganciare la rnc dal processo sio"""

        for rec in self:
            rec.update_processo_iso(False, rec.processo_id.id, rec.quality_alert_id.id)
        return super(ProcessoIsoRnc, self).unlink()



class RapportoNonconformitaAlert(models.Model):

    _inherit = 'quality.alert'

    # campi angrafica
    tipo = fields.Selection([('interna', 'Interna'), ('esterna', 'Esterna'), ('sistema', 'Sistema')])
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
    imputato_a = fields.Selection(selection=[('dipendente', 'Dipendente'), ('cliente', 'Cliente'), ('fornitore', 'Fornitore')])
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

    # todo rimuovere perchè modificata la relazione da o2m a m2m
    # processo_id = fields.Many2one('processo.iso')
    # audit_id = fields.Many2one('processo.audit')

    @api.onchange('imputato_a')
    def onchange_imputato_a(self):
        for rec in self:
            if rec.imputato_a == 'cliente':
                return {'domain': {'imputato_partner_id': [('is_customer', '=', True)]}}
            if rec.imputato_a == 'fornitore':
                return {'domain': {'imputato_partner_id': [('is_supplier', '=', True)]}}