# -*- coding: utf-8 -*-
{
    'name': 'Octa Biz Dashboard',
    'version': '17.0.1.0.0',
    'summary': 'Dashboard điều hành theo scope: vận hành, ranh đỏ, NCC, đại lý, cổng, công nợ, ticket, KPI',
    'author': 'Octa',
    'category': 'Octa',
    'depends': [
        'web',
        'octa_base',
        'octa_project',
        'octa_ticket',
        'octa_gateway',
        'octa_partner',
        'octa_kpi',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/biz_dashboard_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'octa_biz_dashboard/static/src/xml/biz_dashboard.xml',
            'octa_biz_dashboard/static/src/js/biz_dashboard.js',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
