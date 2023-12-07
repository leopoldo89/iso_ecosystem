from odoo import api, models, fields


class EvidenzaDocumentale(models.Model):

    _name = 'evidenza.documentale'

    date = fields.Date()
    description = fields.Text()
    attachment = fields.Binary('Document', copy=False, attachment=True)
    attachment_name = fields.Char()
    note = fields.Text()

    # campi relazionali
    equipment_id = fields.Many2one('maintenance.equipment')
    request_operation_id = fields.Many2one('maintenance.request.operation')
    audit_id = fields.Many2one('processo.audit')

