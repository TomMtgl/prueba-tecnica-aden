# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Student(models.Model):
    """Modelo de Estudiante"""
    _name = 'university.student'
    _description = 'Estudiante'
    _rec_name = 'complete_name'
    
    # Campos básicos
    name = fields.Char(string='Nombre', required=True)
    last_name = fields.Char(string='Apellido', required=True)
    complete_name = fields.Char(string='Nombre Completo', compute='_compute_complete_name', store=True)
    
    # Información de contacto
    email = fields.Char(string='Email', required=True)
    phone = fields.Char(string='Teléfono')
    address = fields.Text(string='Dirección')
    
    # Información académica
    student_id = fields.Char(string='Matrícula', required=True, copy=False)
    enrollment_date = fields.Date(string='Fecha de Ingreso', default=fields.Date.today)
    
    # Relaciones
    enrollment_ids = fields.One2many(
        'university.enrollment', 
        'student_id', 
        string='Inscripciones'
    )
    
    # Campos computados
    enrollment_count = fields.Integer(
        string='Cantidad de Inscripciones',
        compute='_compute_enrollment_count'
    )
    
    # Estado
    active = fields.Boolean(string='Activo', default=True)
    
    # Restricciones SQL
    _sql_constraints = [
        ('student_id_unique', 'UNIQUE(student_id)', 'La matrícula debe ser única'),
        ('email_unique', 'UNIQUE(email)', 'El email debe ser único'),
    ]
    
    @api.depends('name', 'last_name')
    def _compute_complete_name(self):
        """Calcula el nombre completo"""
        for record in self:
            record.complete_name = f"{record.name} {record.last_name}"
    
    @api.depends('enrollment_ids')
    def _compute_enrollment_count(self):
        """Calcula la cantidad de inscripciones"""
        for record in self:
            record.enrollment_count = len(record.enrollment_ids)
