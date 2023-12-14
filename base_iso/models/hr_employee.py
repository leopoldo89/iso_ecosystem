from odoo import models, api, fields


class SiglaCollaboratore(models.Model):

    _name = 'sigla.collaboratore'

    name = fields.Char()

class HrEmployee(models.Model):

    _inherit = 'hr.employee'
    sigla_collaboratore_id = fields.Many2one('sigla.collaboratore')
    data_assunzione = fields.Date()
    fa_secondaria_ids = fields.Many2many('hr.job')

