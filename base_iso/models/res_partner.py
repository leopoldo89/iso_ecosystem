from odoo import models, api, fields

class TipoProduzione(models.Model):

    _name = 'tipo.produzione'

    name = fields.Char()

class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    # campi cliente
    funzione_aziendale_id = fields.Many2one('hr.job')
    reparto_id = fields.Many2one('hr.department')
    qualification_ids = fields.One2many('res.partner.qualification', 'partner_id')

    # campi fornitore
    tipo_produzione_ids = fields.Many2many('tipo.produzione')