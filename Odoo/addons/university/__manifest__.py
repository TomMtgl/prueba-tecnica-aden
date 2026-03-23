# -*- coding: utf-8 -*-
{
    'name': 'University Management',
    'version': '1.0',
    'category': 'Education',
    'installable': True,  
    'application': True,
    'summary': 'Sistema de gestión universitaria',
    'license': 'LGPL-3',
    'description': """
        Módulo para gestionar:
        - Estudiantes
        - Carreras
        - Planes de estudio
        - Asignaturas
        - Inscripciones
        - Profesores
        
        Incluye:
        - Reportes en tiempo real de inscripciones
        - Gestión de información de profesores para pagos
        - Control de acceso por roles
    """,
    'author': 'Tomas',
    'website': 'https://www.tuempresa.com',
    'depends': ['base', 'mail'],
'data': [
    'security/security.xml',
    'security/ir.model.access.csv',
    'data/user_data.xml',
    'data/demo_data.xml',
    'views/student_views.xml', 
    'views/enrollment_views.xml',   
    'views/career_views.xml',
    'views/subject_views.xml',
    'views/course.xml',
    'views/teacher_views.xml',
    'views/menu.xml',                
],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
