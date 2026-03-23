# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Teacher(models.Model):
    """Modelo de Profesor"""
    _name = 'university.teacher'
    _description = 'Profesor'
    _rec_name = 'complete_name'
    
    # Campos básicos
    name = fields.Char(string='Nombre', required=True)
    last_name = fields.Char(string='Apellido', required=True)
    complete_name = fields.Char(string='Nombre Completo', compute='_compute_complete_name', store=True)
    
    # Información de contacto - REQUERIMIENTO: Para finanzas gestionar pagos
    email = fields.Char(string='Email', required=True)
    phone = fields.Char(string='Teléfono', required=True)
    mobile = fields.Char(string='Móvil')
    address = fields.Text(string='Dirección')
    
    # Información bancaria para pagos
    bank_account = fields.Char(string='Cuenta Bancaria')
    bank_name = fields.Char(string='Banco')
    tax_id = fields.Char(string='CUIT/DNI')
    
    # Información académica
    employee_id = fields.Char(string='Legajo', required=True)
    specialization = fields.Char(string='Especialización')
    
    # Relaciones
    subject_ids = fields.One2many(
        'university.subject',
        'teacher_id',
        string='Asignaturas que dicta'
    )
    
    # Campos computados
    subject_count = fields.Integer(
        string='Cantidad de Asignaturas',
        compute='_compute_subject_count'
    )
    
    # Estado
    active = fields.Boolean(string='Activo', default=True)
    
    # Notas internas
    notes = fields.Text(string='Notas')
    
    _sql_constraints = [
        ('employee_id_unique', 'UNIQUE(employee_id)', 'El legajo debe ser único'),
        ('email_unique', 'UNIQUE(email)', 'El email debe ser único'),
    ]
    
    @api.depends('name', 'last_name')
    def _compute_complete_name(self):
        """Calcula el nombre completo"""
        for record in self:
            record.complete_name = f"{record.name} {record.last_name}"
    
    @api.depends('subject_ids')
    def _compute_subject_count(self):
        """Calcula la cantidad de asignaturas"""
        for record in self:
            record.subject_count = len(record.subject_ids)
