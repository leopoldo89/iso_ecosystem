from odoo import api, models, fields


class ProcessoAuditRequisito(models.Model):

    _name = 'processo.audit.requisito'

    name = fields.Char()
    note = fields.Text()
    audit_id = fields.Many2one('processo.audit')
    voto = fields.Selection(selection=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'),
                                       ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')])


class ProcessoAuditIndicatore(models.Model):

    _name = 'processo.audit.indicatore'

    audit_id = fields.Many2one('processo.audit')
    indicatore_aggiuntivo = fields.Boolean()
    indicatore_id = fields.Many2one('processo.iso.indicatore')
    tipo_valore_previsto = fields.Selection(selection=[('percentuale', 'Percentuale'),
                                                       ('valore_numerico', 'Valore Numerico')])
    previsto = fields.Float()
    valore_riscontrato = fields.Float()
    note = fields.Text()
    valutazione = fields.Selection(selection=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'),
                                              ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')])


class ProcessoAuditInfoCollabortatore(models.Model):

    _name = 'processo.audit.info.collaboratore'


    audit_id = fields.Many2one('processo.audit')
    employee_id = fields.Many2one('hr.employee')
    # todo rivedere il tipo di questo campo
    argomento = fields.Text()
    entro_il = fields.Date()
    efficacia = fields.Selection(selection=[('buona', 'Buona'), ('media', 'Media'), ('alta', 'Alta')], default="media")
    tutor_interno = fields.Many2one('hr.employee')
    fatta_il = fields.Date()


class ProcessoAudit(models.Model):

    _name = 'processo.audit'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # campi anagrafica
    name = fields.Char()

    processo_id = fields.Many2one('processo.iso')  # relazione a processo
    inizio_periodo = fields.Date()
    fine_periodo = fields.Date()
    data_audit = fields.Date()
    tipo_audit = fields.Selection([('programmato', 'Programmato'), ('straordinanio', 'Straordinario')])
    audit_precedente_id = fields.Many2one('processo.audit')
    data_audit_precedente = fields.Date(related="audit_precedente_id.data_audit")
    auditor_interno_id = fields.Many2one('hr.employee')
    auditor_esterno_id = fields.Many2one('res.partner')
    campo_applicazione = fields.Html()
    valutazione_finale_indicatori = fields.Float()
    note_finali = fields.Html()
    validatore_finale = fields.Many2one('hr.employee')
    validazione = fields.Selection([('programmato', 'Programmato'), ('straordinanio', 'Straordinario')])
    data_prossimo_audit = fields.Date()

    # campi info
    non_conformita_ids = fields.One2many('quality.alert', 'audit_id')
    azioni_correttive_ids = fields.One2many('azione.correttiva', 'audit_id')
    rischi_ids = fields.One2many('rischio.iso', 'audit_id')
    opportunita_ids = fields.One2many('opportunita.iso', 'audit_id')

    #  bcampi attività dell'audit
    requisiti_ids = fields.One2many('processo.audit.requisito', 'audit_id')
    indicatori_ids = fields.One2many('processo.audit.indicatore', 'audit_id')
    documentazione_ids = fields.One2many('evidenza.documentale', 'audit_id')

    # campi esito e validazione
    miglioramenti = fields.Html()
    fa_da_informare_ids = fields.One2many('processo.audit.info.collaboratore', 'audit_id')
    ac_da_creare_ids = fields.One2many('azione.correttiva', 'audit_da_creare_id')

    @api.onchange('processo_id')
    def onchange_processo_id(self):
        if self.processo_id:
            lines = []
            for indicatore in self.processo_id.indicatori_ids:
                lines.append((0,0, {
                    'indicatore_id': indicatore.id,
                    'tipo_valore_previsto': indicatore.tipo_valore_previsto,
                    'previsto': indicatore.valore_previsto
                }))
            self.indicatori_ids = lines

            lines = []
            processi_coinvolti_rnc = self.env['processo.iso.coinvolto'].search([('processo_id', '=', self.processo_id.id)])
            for processo_coinvolto in processi_coinvolti_rnc:
                if processo_coinvolto.quality_alert_id:
                    lines.append((4, processo_coinvolto.quality_alert_id.id))
            self.non_conformita_ids = lines


