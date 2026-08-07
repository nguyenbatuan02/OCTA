# -*- coding: utf-8 -*-
{
    'name': 'Octa Vòng đời 6',
    'version': '17.0.1.0.0',
    'summary': 'Ticket Hoàn/Hủy/Điều chỉnh giao dịch tạo tự động từ Portal qua API',
    'author': 'Octa',
    'category': 'Octa',
    'depends': [
        'octa_base',
        'octa_project',
        'octa_ticket',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/vd6_rules.xml',
        'data/vd6_config_data.xml',
        'data/vd6_stage_data.xml',
        'data/vd6_team_data.xml',
        'views/project_task_vd6_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
