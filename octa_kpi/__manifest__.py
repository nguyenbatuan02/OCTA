# -*- coding: utf-8 -*-
{
    'name': 'Octa KPI',
    'version': '17.0.1.0.0',
    'summary': 'KPI CSKH/VH: SLA, FCR, tái phát, xếp loại A/B/C',
    'author': 'Octa',
    'category': 'Octa',
    'depends': [
        'octa_base',
        'octa_project',
        'octa_ticket',
        'octa_report',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/octa_kpi_rules.xml',
        'data/ir_cron.xml',
        'views/octa_kpi_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
