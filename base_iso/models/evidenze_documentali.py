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
    risk_opp_id = fields.Many2one('risk.opportunity.base')

    # campo utile quando bisogna avere più tabelle O2M di evidenza documentale in uno stesso modello
    # serve per mettere un domain ai campi o2m
    sezione_modello = fields.Selection(selection=[('ro_obiettivi', 'ro_obiettivi'), ('ro_efficacia', 'ro_efficacia')])
