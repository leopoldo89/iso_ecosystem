from odoo import api, models, fields


class RapportoNonconformitaAlert(models.Model):

    _inherit = 'quality.alert'

    # lavoro
    nc_data = fields.Datetime()
    nc_data_risoluzione = fields.Datetime()
    nc_risolta_da = fields.Many2one('hr.employee')
    nc_costo = fields.Float()
    qualification_id = fields.Many2one('res.partner.qualification')
    satisfaction_id = fields.Many2one('res.partner.satisfaction')
    employee_qualification_id = fields.Many2one('hr.employee.qualification')
    employee_formazione_qualification_id = fields.Many2one('hr.employee.qualification')