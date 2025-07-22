from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ReservaReunion(models.Model):
    _name = 'reserva.reunion'
    _description = 'Reserva de Sala de Reunión'
    _order = 'fecha_inicio desc'

    referencia = fields.Char(
        string='Referencia',
        required=True,
        default='Nuevo',
        readonly=True,
        copy=False,
    )
    sala_id = fields.Many2one('sala.reunion', string='Sala', required=True)
    fecha_inicio = fields.Datetime(string='Fecha de inicio', required=True)
    fecha_fin = fields.Datetime(string='Fecha de fin', required=True)
    usuario_reserva = fields.Many2one(
        'res.users',
        string='Usuario de reserva',
        default=lambda self: self.env.user.id,
        readonly=True,
    )

    @api.model
    def create(self, vals):
        if vals.get('referencia', 'Nuevo') == 'Nuevo':
            vals['referencia'] = self.env['ir.sequence'].next_by_code('reserva.reunion') or 'Nuevo'
        return super().create(vals)

    @api.constrains('sala_id', 'fecha_inicio', 'fecha_fin')
    def _check_solapamiento(self):
        for reserva in self:
            if reserva.fecha_inicio and reserva.fecha_fin:
                if reserva.fecha_inicio >= reserva.fecha_fin:
                    raise ValidationError('La fecha de fin debe ser posterior a la fecha de inicio.')
                coincidencias = self.search([
                    ('id', '!=', reserva.id),
                    ('sala_id', '=', reserva.sala_id.id),
                    ('fecha_inicio', '<', reserva.fecha_fin),
                    ('fecha_fin', '>', reserva.fecha_inicio),
                ], limit=1)
                if coincidencias:
                    raise ValidationError('Existe una reserva solapada para esta sala.')
