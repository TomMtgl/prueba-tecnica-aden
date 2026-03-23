from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Course(models.Model):
    _name = 'university.course'
    _description = 'Curso de la Universidad'

    name = fields.Char(string='Nombre del Curso', required=True)
    subject_id = fields.Many2one('university.subject', string='Asignatura', required=True)
    teacher_id = fields.Many2one('university.teacher', string='Profesor', required=True)
    capacity = fields.Integer(string='Cupo Máximo', default=30)
    
    inscription_ids = fields.One2many('university.enrollment', 'course_id', string='Inscripciones')
    
    enrolled_count = fields.Integer(string='Inscriptos', compute='_compute_enrolled_count', store=True)

    @api.depends('inscription_ids')
    def _compute_enrolled_count(self):
        for record in self:
            record.enrolled_count = len(record.inscription_ids)

    @api.constrains('inscription_ids', 'capacity')
    def _check_capacity(self):
        for record in self:
            if record.enrolled_count > record.capacity:
                raise ValidationError(f"El curso {record.name} ha superado el cupo máximo de {record.capacity} alumnos.")