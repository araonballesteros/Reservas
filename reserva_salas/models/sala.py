from odoo import models, fields


class SalaReunion(models.Model):
    _name = 'sala.reunion'
    _description = 'Sala de Reunión'
    _order = 'nombre'

    nombre = fields.Char(string='Nombre', required=True)
    capacidad = fields.Integer(string='Capacidad', required=True)
    ubicacion = fields.Char(string='Ubicación')
    disponible = fields.Boolean(string='Disponible', default=True)
