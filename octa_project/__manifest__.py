{
    'name': 'OCTA Project',
    'version': '17.0.1.0.0',
    'category': 'Project',
    'summary': 'OCTA Project Management',
    'depends': ['project'],
    'data': [
        'security/ir.model.access.csv',
        'views/project_task_views.xml',
        'views/project_task_type_views.xml',
    ],
    'installable': True,
    'application': False,
}