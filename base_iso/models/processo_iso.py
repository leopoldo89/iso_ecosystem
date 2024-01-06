from odoo import api, models, fields


class ProcessoIsoIndicatore(models.Model):

    _name = 'processo.iso.indicatore'

    processo_id = fields.Many2one('processo.iso')
    name = fields.Char()
    anno = fields.Integer()
    descrizione = fields.Text()
    strumenti_monitoraggio = fields.Char()
    misurazione = fields.Char()
    resoconto = fields.Text()
    tipo_valore_previsto = fields.Selection(selection=[('percentuale', 'Percentuale'), ('valore_numerico', 'Valore Numerico')])
    valore_previsto = fields.Float()


class ProcessoIsoInputOutput(models.Model):

    _name = 'processo.iso.input.output'

    processo_id = fields.Many2one('processo.iso')
    is_input = fields.Boolean()
    descrizione = fields.Char()
    rilevanza = fields.Selection(selection=[('bassa', 'Bassa'), ('media', 'Media'), ('alta', 'Alta')], default="media")

class ProcessoIso(models.Model):

    _name = 'processo.iso'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # campi anagrafica
    name = fields.Char()
    parent_id = fields.Many2one('processo.iso')
    tipo_processo = fields.Selection(selection=[('primario', 'Primario'), ('supporto', 'Supporto'),
                                                ('sistema', 'Sistema')])
    responsible_id = fields.Many2one('hr.employee')

    # campi input/output
    input_ids = fields.One2many('processo.iso.input.output', 'processo_id', domain=[('is_input', '=', True)])
    output_ids = fields.One2many('processo.iso.input.output', 'processo_id', domain=[('is_input', '=', False)])

    # campi indicatori
    indicatori_ids = fields.One2many('processo.iso.indicatore', 'processo_id')

    # campi INFO
    non_conformita_ids = fields.Many2many('quality.alert')
    azioni_correttive_ids = fields.One2many('azione.correttiva', 'processo_id')
    rischi_ids = fields.One2many('rischio.iso', 'processo_id')
    opportunita_ids = fields.One2many('opportunita.iso', 'processo_id')

    # campi Audit
    audit_ids = fields.One2many('processo.audit', 'processo_id')
