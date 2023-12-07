from odoo import api, models, fields


class OpportunitaIso(models.Model):
    _name = 'opportunita.iso'

    name = fields.Char()
    data = fields.Date()
    opportunita_identificata = fields.Text()
    validazione_finale = fields.Text()
    validatore_interno = fields.Many2one('hr.employee')

    # relazioni ad altre entita
    processo_id = fields.Many2one('processo.iso')
    audit_id = fields.Many2one('processo.audit')
