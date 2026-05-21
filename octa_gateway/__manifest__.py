# -*- coding: utf-8 -*-
{
    'name': 'Octa Gateway',
    'version': '17.0.1.0.0',
    'category': 'Octa',
    'summary': 'Quản lý cổng API, lệnh mở/đóng và ranh đỏ tự động',
    'author': 'Octa',
    'depends': [
        'base',
        'mail',
        'purchase',
        'octa_base',
        'octa_ticket',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/octa_gateway_rules.xml',
        'data/ir_cron.xml',
        'views/octa_gateway_views.xml',
        'views/octa_gateway_command_views.xml',
        'wizards/octa_gateway_command_wizard_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}