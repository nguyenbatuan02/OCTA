# -*- coding: utf-8 -*-
{
    'name': 'Octa Ticket',
    'version': '17.0.2.0.0',
    'summary': 'Quản lý ticket CSKH & Vận hành thương mại Bigtel',
    'author': 'Octa',
    'category': 'Octa',
    'depends': [
        'project',
        'octa_base',    
        'octa_project', 
    ],
    'data': [
        'security/octa_ticket_rules.xml',
        'security/ir.model.access.csv',

        'data/checklist_template_data.xml',
        'data/checklist_template_vh_data.xml',
        'data/ir_cron.xml',

        'views/ticket_checklist_views.xml',
        'views/project_task_views.xml',

        'wizards/ticket_import_wizard_views.xml',
        'wizards/ticket_check_log_wizard_views.xml',
        'wizards/ticket_handover_wizard_views.xml',

        'views/menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'octa_ticket/static/src/js/check_warning.js',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}