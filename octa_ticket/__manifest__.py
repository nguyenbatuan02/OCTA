{
    'name': 'OCTA Ticket',
    'version': '1.0',
    'summary': 'Quản lý ticket',
    'author': 'OCTA',
    'depends': ['project', 'octa_project'],
    'data': [
        'security/ir.model.access.csv',
        'data/checklist_template_data.xml',
        'views/ticket_checklist_views.xml',
        'views/project_task_views.xml',
        'wizards/ticket_import_wizard_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': False,
}