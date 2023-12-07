from odoo import api, models, fields


class RischioIso(models.Model):
    _name = 'rischio.iso'

    name = fields.Char()
    data = fields.Date()
    rischio_identificato = fields.Text()
    validazione_finale = fields.Text()
    validatore_interno = fields.Many2one('hr.employee')

    # relazioni ad altre entita
    processo_id = fields.Many2one('processo.iso')
    audit_id = fields.Many2one('processo.audit')
