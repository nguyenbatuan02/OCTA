{
    'name': 'OCTA Ticket',
    'version': '1.1',
    'summary': 'Quan ly ticket CSKH & Van hanh thuong mai',
    'author': 'OCTA',
    'category': 'Octa Ticket',
    'depends': ['project', 'octa_project'],
    'data': [
        'security/octa_ticket_groups.xml',
        'security/octa_ticket_rules.xml',
        'security/ir.model.access.csv',
        'data/checklist_template_data.xml',
        'data/checklist_template_vh_data.xml',
        'data/ir_cron.xml',
        'views/ticket_checklist_views.xml',
        'views/project_task_views.xml',
        'wizards/ticket_import_wizard_views.xml',
        'wizards/ticket_check_log_wizard_views.xml',
        'views/menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'octa_ticket/static/src/js/check_warning.js',
        ],
    },
    'installable': True,
    'application': True,
}