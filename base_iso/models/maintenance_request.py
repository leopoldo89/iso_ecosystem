from odoo import api, models, fields

class MaintenanceTeam(models.Model):

    _inherit = 'maintenance.team'

    responsible_id = fields.Many2one('res.users')

class OperationRicambio(models.Model):

    _name = 'operation.ricambio'

    operation_id = fields.Many2one('maintenance.request.operation')
    descrizione_ricambi = fields.Char()
    costo_ricambi = fields.Float()
    materiali_consumo = fields.Char()
    costo_materiali = fields.Float()


class MaintenanceRequest(models.Model):

    _inherit = 'maintenance.request'

    internal_reference = fields.Char(related="equipment_id.internal_reference")
    equipment_assign_to = fields.Selection([('department', 'Department'), ('employee', 'Employee'), ('other', 'Other')],
                                           related="equipment_id.equipment_assign_to")
    location = fields.Char(related="equipment_id.location")
    workcenter_id = fields.Many2one('mrp.workcenter', related="equipment_id.workcenter_id")
    last_request_ids = fields.Many2many('maintenance.request', compute="_compute_last_request_ids")

    # campi scheda manutenzione: manutenzione
    operation_ids = fields.One2many('maintenance.request.operation', 'maintenance_request_id')

    # campi scheda manutenzione: esito
    costo_manutenzione = fields.Float(compute="compute_costo_totale_manutenzione")
    validatore_interno = fields.Many2one('hr.employee')
    note_finali = fields.Html()
    prossima_manutenzione = fields.Char()
    data_prossima_manutenzione = fields.Date()


    @api.onchange('maintenance_team_id')
    def _onchange_maintenance_team_id(self):
        if self.maintenance_team_id and self.maintenance_team_id.responsible_id:
            self.responsible_id = self.maintenance_team_id.responsible_id.id

    @api.onchange('equipment_id')
    def onchange_equipment_id(self):
        res = super(MaintenanceRequest, self).onchange_equipment_id()
        if self.equipment_id:
            self._compute_last_request_ids()
        return res

    def _compute_last_request_ids(self):
        if self.equipment_id:
            done_stages = self.env['maintenance.stage'].search([('done', '=', True)]).ids
            request_ids = self.env['maintenance.request'].search([('equipment_id', '=', self.equipment_id.id),
                                                                  ('stage_id', 'in', done_stages), ('equipment_id', '!=', self.equipment_id.id)],
                                                                 limit=5, order='schedule_date DESC').ids
            self.last_request_ids = [(6, 0, request_ids)]
        else:
            self.last_request_ids = False

    def compute_costo_totale_manutenzione(self):
        for rec in self:
            totale = 0
            for operazione in rec.operation_ids:
                totale += operazione.costo_totale
            rec.costo_manutenzione = totale





