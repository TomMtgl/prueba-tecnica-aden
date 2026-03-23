# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Enrollment(models.Model):
    """Modelo de Inscripción de Estudiante"""
    _name = 'university.enrollment'
    _description = 'Inscripción'
    _rec_name = 'display_name'
    
    # Relación con estudiante
    student_id = fields.Many2one(
        'university.student',
        string='Estudiante',
        required=True,
        ondelete='cascade'
    )
    
    # Relación con carrera
    career_id = fields.Many2one(
        'university.career',
        string='Carrera',
        required=True,
        ondelete='cascade'
    )
    
    # Relación con plan de estudios
    study_plan_id = fields.Many2one(
        'university.study_plan',
        string='Plan de Estudios',
        required=True,
        ondelete='cascade',
        domain="[('career_id', '=', career_id)]"
    )
    
    # Relación con asignatura
    subject_id = fields.Many2one(
        'university.subject',
        string='Asignatura',
        required=True,
        ondelete='cascade',
        domain="[('study_plan_id', '=', study_plan_id)]"
    )
    
    # Información de inscripción
    enrollment_date = fields.Date(
        string='Fecha de Inscripción',
        default=fields.Date.today,
        required=True
    )
    
    # Estado de la inscripción
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('enrolled', 'Inscripto'),
        ('approved', 'Aprobado'),
        ('failed', 'Desaprobado'),
        ('withdrawn', 'Retirado'),
    ], string='Estado', default='draft', required=True)
    
    # Calificaciones
    final_grade = fields.Float(string='Nota Final')
    
    # Notas
    notes = fields.Text(string='Observaciones')
    
    # Campo display
    display_name = fields.Char(string='Nombre', compute='_compute_display_name')
    
    # Estado activo
    active = fields.Boolean(string='Activo', default=True)
    
    # Restricción: Un estudiante no puede inscribirse dos veces a la misma asignatura
    _sql_constraints = [
        ('student_subject_unique', 
         'UNIQUE(student_id, subject_id)', 
         'El estudiante ya está inscripto en esta asignatura'),
    ]
    
    @api.depends('student_id.complete_name', 'subject_id.name')
    def _compute_display_name(self):
        """Calcula el nombre a mostrar"""
        for record in self:
            if record.student_id and record.subject_id:
                record.display_name = f"{record.student_id.complete_name} - {record.subject_id.name}"
            else:
                record.display_name = 'Nueva Inscripción'
    
    @api.onchange('career_id')
    def _onchange_career_id(self):
        """Resetea plan de estudios y asignatura cuando cambia la carrera"""
        if self.career_id:
            self.study_plan_id = False
            self.subject_id = False
    
    @api.onchange('study_plan_id')
    def _onchange_study_plan_id(self):
        """Resetea asignatura cuando cambia el plan de estudios"""
        if self.study_plan_id:
            self.subject_id = False
    
    def action_enroll(self):
        """Confirma la inscripción"""
        self.write({'state': 'enrolled'})
    
    def action_approve(self):
        """Aprueba la materia"""
        self.write({'state': 'approved'})
    
    def action_fail(self):
        """Desaprueba la materia"""
        self.write({'state': 'failed'})
