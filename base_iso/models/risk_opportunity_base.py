from odoo import api, models, fields


class RiskOpportunityIso(models.Model):
    _name = 'risk.opportunity.base'

    # campi anagrafica
    data = fields.Date()
    name = fields.Char(string="Cod. interno")
    anno = fields.Integer()
    tipo = fields.Selection(selection=[('interno', 'Interno'), ('esterno', 'Esterno')])
    gruppo_anagrafica_ids = fields.One2many('gruppo.lavoro.iso', 'risk_opp_id', domain=[('tipologia_gruppo', '=', 'ro_anagrafica')])


    # campi analisi ed indentificazione
    air_area_attivita = fields.Text()
    air_situazione_attuale = fields.Html()
    air_potenzionale_situazione_futura = fields.Html()

    # campi obiettivi da perseguire
    op_descrizione = fields.Html()
    op_quantificazione = fields.Html()
    op_documentazione_ids = fields.One2many('evidenza.documentale', 'risk_opp_id', domain=[('sezione_modello', '=', 'ro_obiettivi')])
    op_tempistica_prevista = fields.Text()
    op_responsabile_id = fields.Many2one('hr.employee')
    op_gruppo_ids = fields.One2many('gruppo.lavoro.iso', 'risk_opp_id', domain=[('tipologia_gruppo', '=', 'ro_obiettivi')])

    # campi azioni da intraprendere
    ai_attivita_azioni = fields.Html()
    ai_tempistica_azioni = fields.Html()
    ai_supporti_azioni = fields.Html()
    ai_responsabile_id = fields.Many2one('hr.employee')
    ai_gruppo_ids = fields.One2many('gruppo.lavoro.iso', 'risk_opp_id', domain=[('tipologia_gruppo', '=', 'ro_azioni')])
    ai_note = fields.Html()

    # campi risorse necessarie
    rn_descrizione = fields.Html()
    rn_quantificazione_budget = fields.Html()
    rn_supporti_esterni = fields.Html()
    rn_responsabile_id = fields.Many2one('hr.employee')
    rn_gruppo_ids = fields.One2many('gruppo.lavoro.iso', 'risk_opp_id', domain=[('tipologia_gruppo', '=', 'ro_risorse')])
    rn_note = fields.Html()

    # campi piani di attuazione
    pa_attivita_da_svolgere = fields.Html()
    pa_data_dal = fields.Date()
    pa_data_al = fields.Date()
    pa_obiettivi = fields.Html()
    pa_responsabile_id = fields.Many2one('hr.employee')
    pa_gruppo_ids = fields.One2many('gruppo.lavoro.iso', 'risk_opp_id', domain=[('tipologia_gruppo', '=', 'ro_piano')])
    pa_note = fields.Html()

    # campi evidenza ed efficacia
    ee_attivita_svolte = fields.Html()
    ee_start_at = fields.Date()
    ee_responsabile_id = fields.Many2one('hr.employee')
    ee_gruppo_ids = fields.One2many('gruppo.lavoro.iso', 'risk_opp_id', domain=[('tipologia_gruppo', '=', 'ro_efficacia')])
    ee_documentazione_ids = fields.One2many('evidenza.documentale', 'risk_opp_id', domain=[('sezione_modello', '=', 'ro_efficacia')])
    validazione_finale = fields.Html()
    validatore_interno = fields.Many2one('hr.employee')
    ee_end_at = fields.Date()



