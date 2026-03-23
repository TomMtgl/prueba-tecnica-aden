# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Career(models.Model):
    """Modelo de Carrera"""
    _name = 'university.career'
    _description = 'Carrera'
    
    # Campos básicos
    name = fields.Char(string='Nombre de la Carrera', required=True)
    code = fields.Char(string='Código', required=True)
    description = fields.Text(string='Descripción')
    
    # Duración
    duration_years = fields.Integer(string='Duración (años)', default=4)
    
    # Relaciones
    study_plan_ids = fields.One2many(
        'university.study_plan',
        'career_id',
        string='Planes de Estudio'
    )
    
    enrollment_ids = fields.One2many(
        'university.enrollment',
        'career_id',
        string='Inscripciones'
    )
    
    # Campos computados
    student_count = fields.Integer(
        string='Cantidad de Estudiantes Inscriptos',
        compute='_compute_student_count'
    )
    
    active = fields.Boolean(string='Activo', default=True)
    
    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'El código de carrera debe ser único'),
    ]
    
    @api.depends('enrollment_ids')
    def _compute_student_count(self):
        """Calcula la cantidad de estudiantes inscriptos"""
        for record in self:
            # Contar estudiantes únicos
            record.student_count = len(record.enrollment_ids.mapped('student_id'))
