# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Subject(models.Model):
    """Modelo de Asignatura"""
    _name = 'university.subject'
    _description = 'Asignatura'
    
    # Campos básicos
    name = fields.Char(string='Nombre de la Asignatura', required=True)
    code = fields.Char(string='Código', required=True)
    
    # Relación con plan de estudios
    study_plan_id = fields.Many2one(
        'university.study_plan',
        string='Plan de Estudios',
        required=True,
        ondelete='cascade'
    )
    
    # Información académica
    year = fields.Selection([
        ('1', 'Primer Año'),
        ('2', 'Segundo Año'),
        ('3', 'Tercer Año'),
        ('4', 'Cuarto Año'),
        ('5', 'Quinto Año'),
    ], string='Año', required=True)
    
    semester = fields.Selection([
        ('1', 'Primer Semestre'),
        ('2', 'Segundo Semestre'),
        ('anual', 'Anual'),
    ], string='Cuatrimestre', default='1')
    
    credits = fields.Integer(string='Créditos')
    hours_per_week = fields.Integer(string='Horas Semanales')
    
    # Relación con profesores calificados para dictar esta materia
    qualified_teacher_ids = fields.Many2many(
        'university.teacher',
        'subject_teacher_rel',
        'subject_id',
        'teacher_id',
        string='Profesores Calificados',
        help='Profesores que pueden dictar esta asignatura'
    )
    
    # Relaciones con inscripciones
    enrollment_ids = fields.One2many(
        'university.enrollment',
        'subject_id',
        string='Inscripciones'
    )
    
    # Campos computados - REQUERIMIENTO: Ver inscriptos en tiempo real
    enrollment_count = fields.Integer(
        string='Cantidad de Inscriptos',
        compute='_compute_enrollment_count',
        help='Cantidad de estudiantes inscriptos a esta asignatura'
    )
    
    description = fields.Text(string='Descripción')
    active = fields.Boolean(string='Activo', default=True)
    
    _sql_constraints = [
        ('code_study_plan_unique', 'UNIQUE(code, study_plan_id)', 
         'El código de asignatura debe ser único dentro del plan de estudios'),
    ]
    
    @api.depends('enrollment_ids')
    def _compute_enrollment_count(self):
        """Calcula la cantidad de inscriptos en tiempo real"""
        for record in self:
            record.enrollment_count = len(record.enrollment_ids)
