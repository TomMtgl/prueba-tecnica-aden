# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StudyPlan(models.Model):
    """Modelo de Plan de Estudios"""
    _name = 'university.study_plan'
    _description = 'Plan de Estudios'
    _rec_name = 'complete_name'
    
    # Campos básicos
    name = fields.Char(string='Nombre', required=True)
    year = fields.Integer(string='Año', required=True, help='Año del plan de estudios (ej: 2024)')
    complete_name = fields.Char(string='Nombre Completo', compute='_compute_complete_name', store=True)
    
    # Relación con carrera
    career_id = fields.Many2one(
        'university.career',
        string='Carrera',
        required=True,
        ondelete='cascade'
    )
    
    # Relaciones con asignaturas
    subject_ids = fields.One2many(
        'university.subject',
        'study_plan_id',
        string='Asignaturas'
    )
    
    # Relaciones con inscripciones
    enrollment_ids = fields.One2many(
        'university.enrollment',
        'study_plan_id',
        string='Inscripciones'
    )
    
    description = fields.Text(string='Descripción')
    active = fields.Boolean(string='Activo', default=True)
    
    _sql_constraints = [
        ('career_year_unique', 'UNIQUE(career_id, year)', 
         'Ya existe un plan de estudios para esta carrera en ese año'),
    ]
    
    @api.depends('career_id.name', 'year')
    def _compute_complete_name(self):
        """Genera el nombre completo del plan"""
        for record in self:
            if record.career_id and record.year:
                record.complete_name = f"{record.career_id.name} - Plan {record.year}"
            else:
                record.complete_name = record.name or ''
