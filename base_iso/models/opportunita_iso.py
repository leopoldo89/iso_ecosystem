from odoo import api, models, fields


class OpportunitaIso(models.Model):

    _name = 'opportunita.iso'
    _inherit = ['risk.opportunity.base', 'mail.thread', 'mail.activity.mixin']

    opportunita_identificata = fields.Text()

    # campi tempistica, vantaggio, priorità
    tvp_entro_il = fields.Date()
    tvp_vantaggio = fields.Html()
    tvp_vantaggio_economico = fields.Html()
    tvp_currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id, required=True)
    tvp_valore = fields.Monetary(currency_field='tvp_currency_id')
    tvp_priorita = fields.Html()
    tvp_indicatore_priorita = fields.Selection(selection=[('bassa', 'Bassa'), ('media', 'Media'), ('alta', 'Alta')])
    tvp_note = fields.Html()

    # relazioni ad altre entita
    processo_id = fields.Many2one('processo.iso')
    audit_id = fields.Many2one('processo.audit')
