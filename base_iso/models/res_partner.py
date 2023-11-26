from odoo import models, api, fields

class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    certificazione_iso = fields.Char()
