
from odoo import api, models, fields


class MaintenanceEquipment(models.Model):

    _inherit = 'maintenance.equipment'

    internal_reference = fields.Char()
    barcode = fields.Char()
