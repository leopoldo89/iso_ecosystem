from odoo import api, models, fields


class RischioIso(models.Model):

    _name = 'rischio.iso'
    _inherit = ['risk.opportunity.base', 'mail.thread', 'mail.activity.mixin']

    rischio_identificato = fields.Text()

    #  campi frequenza, danno, urgenza/priorita
    fdu_attuale_frequenza = fields.Html()
    fdu_danno_potenziale = fields.Html()
    fdu_azioni_mitiganti = fields.Html()
    fdu_azioni_risolutive = fields.Html()
    fdu_identificatione_priorita = fields.Html()
    fdu_note_frequenza = fields.Html()

    # relazioni ad altre entita
    processo_id = fields.Many2one('processo.iso')
    audit_id = fields.Many2one('processo.audit')
    riesame_direzione_id = fields.Many2one('riesame.direzione')
