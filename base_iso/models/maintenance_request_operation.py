from odoo import api, models, fields


class MaintenanceRequestOperation(models.Model):

    _name = 'maintenance.request.operation'

    maintenance_request_id = fields.Many2one('maintenance.request')
    maintenance_equipment_id = fields.Many2one(related="maintenance_request_id.equipment_id", store=True)
    equipment_category_id = fields.Many2one(related="maintenance_equipment_id.category_id")
    data_manutenzione = fields.Date()
    tipo_manutenzione = fields.Selection([('ordinaria', 'Ordinaria'), ('straordinania', 'Straordinaria')])
    luogo_manutenzione = fields.Selection([('interna', 'Interna'), ('esterna', 'Esterna')])
    addetti_interni_ids = fields.Many2many('res.users')
    ore_manodopera = fields.Float()
    addetti_esterni = fields.Many2many('res.partner')
    costo_manodopera = fields.Float()
    descrizione_manutenzione = fields.Text()
    operation_ricambi_ids = fields.One2many('operation.ricambio', 'operation_id')
    costo_totale = fields.Float(compute="compute_costo_totale")
    documentazione_ids = fields.One2many('evidenza.documentale', 'request_operation_id')

    # campi macchina utensile
    # todo valutare di renderlo un campo many2one con dei nostri valori preimpostati
    periodicita = fields.Char()


    def compute_costo_totale(self):
        for rec in self:
            totale = rec.costo_manodopera
            for ricambio in rec.operation_ricambi_ids:
                totale += ricambio.costo_ricambi
                totale += ricambio.costo_materiali
            rec.costo_totale = totale
