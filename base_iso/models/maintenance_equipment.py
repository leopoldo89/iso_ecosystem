
from odoo import api, models, fields


class MaintenanceEquipmentTaratura(models.Model):

    _name = 'maintenance.equipment.taratura'

    name = fields.Char()
    description = fields.Char()

class MaintenanceEquipmentTaraturaValue(models.Model):

    _name = 'maintenance.equipment.taratura.value'

    taratura_id = fields.Many2one('maintenance.equipment.taratura')
    data_taratura = fields.Date()
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id, required=True)
    costo_totale = fields.Monetary(currency_field="currency_id")
    note = fields.Html()
    next_taratura_date = fields.Date()
    equipment_id = fields.Many2one('maintenance.equipment')


class MaintenanceEquipment(models.Model):

    _inherit = 'maintenance.equipment'

    internal_reference = fields.Char()
    barcode = fields.Char()

    #todo capire come integrare i macchinari, sono categorie di attrezzatura?
    macchinario_id = fields.Many2one('maintenance.equipment')

    # campi descrizione
    documentazione_ids = fields.One2many('evidenza.documentale', 'equipment_id')
    note_attrezzatura = fields.Html()

    # campi informazioni prodotto
    produttore = fields.Many2one('res.partner')
    modifiche_revisioni = fields.Text()
    anno_revisione = fields.Date()
    revisionatore = fields.Many2one('res.partner')
    costo_revisione = fields.Float()

    # campi manutenzioni
    descrizione_manutenzione = fields.Text()
    ricambi_consumi_ids = fields.Many2many('product.product')
    # consumabili_ids = fields.Many2many('product.product', domain="[('detailed_type','=','consu')]")
    taratura_ids = fields.Many2many('maintenance.equipment.taratura')
    taratura_value_ids = fields.One2many('maintenance.equipment.taratura.value', 'equipment_id')

    # campi macchina utensile
    fabbricante = fields.Many2one('res.partner')
    anno_fabbricazione = fields.Date()
    assistenza = fields.Many2many('res.partner')
    request_operation_ids = fields.One2many('maintenance.request.operation', 'maintenance_equipment_id')

