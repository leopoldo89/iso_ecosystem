from odoo import api, models, fields


class AzioneCorrettiva(models.Model):

    _name = 'azione.correttiva'

    name = fields.Char()
    descrizione = fields.Char()
    anno = fields.Integer()
    data_apertura = fields.Date()
    importanza = fields.Text()
    riscontri = fields.Text()
    commento_finale = fields.Char()
    chiusura_ac = fields.Boolean()

    # relazioni ad altre entita
    processo_id = fields.Many2one('processo.iso')
    audit_id = fields.Many2one('processo.audit')
    audit_da_creare_id = fields.Many2one('processo.audit')