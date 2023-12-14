from odoo import api, models, fields


class RiesameNotaEnte(models.Model):

    _name = 'riesame.nota.ente'

    riesame_direzione_id = fields.Many2one('riesame.direzione')
    rnc_racc_cons = fields.Text()
    data = fields.Date()
    descrizione = fields.Text()
    azione_correttiva = fields.Text()


class RiesameObiettivo(models.Model):

    _name = 'riesame.obiettivo'
    riesame_direzione_id = fields.Many2one('riesame.direzione')
    name = fields.Char()
    descrizione = fields.Text()
    entro_il = fields.Date()
    addetto_id = fields.Many2one('hr.employee')
    risorse = fields.Html()
    note_finali = fields.Html()
    conclusa_il = fields.Date()
    attachment = fields.Binary('Document', copy=False, attachment=True)
    attachment_name = fields.Char()


class RiesameParteInteressata(models.Model):

    _name = 'riesame.parte.interessata'

    riesame_direzione_id = fields.Many2one('riesame.direzione')
    nome = fields.Char()
    rilevanza = fields.Selection(selection=[('basso', 'Basso'), ('sufficiente', 'Sufficiente'),
                                                     ('medio', 'Medio'), ('alto', 'Alto')])


class RiesameRisorsaUmana(models.Model):

    _name = 'riesame.risorsa.umana'

    riesame_direzione_id = fields.Many2one('riesame.direzione')
    descrizione = fields.Html()
    funziona_aziendale_id = fields.Many2one('hr.job')
    entro_il = fields.Date()
    budget = fields.Float()
    responsabile_employee_id = fields.Many2one('hr.employee')


class RiesameRisorsaMateriale(models.Model):

    _name = 'riesame.risorsa.materiale'

    riesame_direzione_id = fields.Many2one('riesame.direzione')
    data = fields.Date()
    descrizione = fields.Html()
    budget = fields.Float()
    urgenza = fields.Selection(selection=[('basso', 'Basso'), ('sufficiente', 'Sufficiente'),
                                            ('medio', 'Medio'), ('alto', 'Alto')])
    entro_il = fields.Date()
    responsabile_employee_id = fields.Many2one('hr.employee')


class RiesameOutput(models.Model):

    _name = 'riesame.output'

    riesame_direzione_id = fields.Many2one('riesame.direzione')
    descrizione = fields.Char()
    entro_il = fields.Date()
    addetto_id = fields.Many2one('hr.employee')
    risorse = fields.Html()
    tipo_output = fields.Selection(selection=[('miglioramenti_sqg', 'miglioramenti_sqg'),
                                              ('miglioramenti_operativi', 'miglioramenti_operativi'), ('investimenti_futuri', 'investimenti_futuri')])


class RiesameDirezione(models.Model):

    _name = 'riesame.direzione'

    # campi anagrafica
    name = fields.Char(string="N° Riesame")
    data_inizio = fields.Date()
    lead_auditor_id = fields.Many2one('hr.employee')
    riesame_gruppo_ids = fields.One2many('gruppo.lavoro.iso', 'riesame_direzione_id', domain=[('tipologia_gruppo', '=', 'rd_anagrafica')])
    data_fine = fields.Date()

    # campi revisione ddq
    rddq_documentazione_ids = fields.One2many('evidenza.documentale', 'riesame_direzione_id',
                                              domain=[('sezione_modello', '=', 'rd_revisione_ddq')])
    rddq_note = fields.Html()

    # campi riesame precedente
    rp_riesame_precedente_id = fields.Many2one('riesame.direzione')
    rp_relazione_precedente = fields.Binary(copy=False, attachment=True, related="rp_riesame_precedente_id.rp_audit_ente_document")
    rp_audit_ente_document_filename = fields.Char()
    rp_audit_ente_document = fields.Binary(copy=False, attachment=True)
    rp_note_ente_ids = fields.One2many('riesame.nota.ente', 'riesame_direzione_id')
    rp_note_indirizzi = fields.Html()

    # campi non conformità
    nc_sistema_ids = fields.Many2many('quality.alert', relation='riesame_nc_sistema', column1='riesame_id', column2='nc_sistema_id')
    nc_interne_ids = fields.Many2many('quality.alert', relation='riesame_nc_interne', column1='riesame_id', column2='nc_interna_id')
    nc_esterne_ids = fields.Many2many('quality.alert', relation='riesame_nc_esterne', column1='riesame_id', column2='nc_esterna_id')

    # campi audit di processo
    ap_note = fields.Html()
    ap_audit_ids = fields.Many2many('processo.audit')

    # campi obiettivi precedenti
    # todo mettere related a riesame precedente
    obiettivi_precedenti_ids = fields.Many2many('riesame.obiettivo')

    # campi contesto
    co_indirizzi_finalita = fields.Html()
    co_parte_interessata_ids = fields.One2many('riesame.parte.interessata', 'riesame_direzione_id')
    co_fattori_interni = fields.Html()
    co_fattori_esterni = fields.Html()
    co_evoluzioni_mercato = fields.Html()

    # campi rischi opportunità
    ro_rischi_ids = fields.One2many('rischio.iso', 'riesame_direzione_id')
    ro_opportunita_ids = fields.One2many('opportunita.iso', 'riesame_direzione_id')

    # campi risorse umane
    ru_descrizione = fields.Html()
    ru_formazione_svolta_ids = fields.Many2many('employee.scheda.valutazione', relation='riesame_scheda_valutazione',
                                                column1='riesame_id', column2='scheda_valutazione')
    ru_formazione_futura_ids = fields.Many2many('employee.scheda.valutazione', relation='riesame_scheda_valutazione_futura',
                                                column1='riesame_id', column2='scheda_valutazione_futura')
    ru_risorse_umane_ids = fields.One2many('riesame.risorsa.umana', 'riesame_direzione_id')
    ru_note = fields.Html()

    # campi risorse materiali
    rm_descrizione = fields.Html()
    rm_risorse_materiali_ids = fields.One2many('riesame.risorsa.materiale', 'riesame_direzione_id')
    rm_note = fields.Html()

    # campi soddisfazione cliente
    sc_descrizione = fields.Html()
    sc_soddisfazioni_ids = fields.One2many('res.partner.satisfaction', 'riesame_direzione_id')
    sc_note = fields.Html()

    # campi output
    o_output_sqg_ids = fields.One2many('riesame.output', 'riesame_direzione_id',
                                       domain=[('tipo_output', '=', 'miglioramenti_sqg')])
    o_output_operativi_ids = fields.One2many('riesame.output', 'riesame_direzione_id',
                                             domain=[('tipo_output', '=', 'miglioramenti_operativi')])
    o_output_investimenti_ids = fields.One2many('riesame.output', 'riesame_direzione_id',
                                             domain=[('tipo_output', '=', 'investimenti_futuri')])

    # campi obiettivi prossimo riesame
    obiettivi_futuri_ids = fields.One2many('riesame.obiettivo', 'riesame_direzione_id')

    # campi valutazioni finali
    vf_note = fields.Html()
    vf_validazione_gruppo_ids = fields.One2many('gruppo.lavoro.iso', 'riesame_direzione_id',
                                                domain=[('tipologia_gruppo', '=', 'rd_valutazione')])
    vf_prossimo_riesame = fields.Date()


