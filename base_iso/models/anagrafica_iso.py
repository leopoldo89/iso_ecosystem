from odoo import models, api, fields

class AnagraficaIso(models.Model):
    _name = 'anagrafica.iso'

    nome = fields.Char()
    codice = fields.Integer()
    description = fields.Html()