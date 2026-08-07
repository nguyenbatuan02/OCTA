# -*- coding: utf-8 -*-
{
    'name': 'Octa Báo cáo',
    'version': '17.0.1.0.0',
    'summary': 'Danh mục & quản lý báo cáo ca/ngày/tuần/tháng/quý cho CSKH, VH, Lead, TDABG',
    'author': 'Octa',
    'category': 'Octa',
    'depends': [
        'web',
        'octa_base',
        'octa_project',
        'octa_ticket',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/octa_report_rules.xml',
        'data/report_catalog_data.xml',
        'data/ir_cron.xml',
        'views/octa_report_views.xml',
        'views/octa_report_dashboard_views.xml',
        'views/menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'octa_report/static/src/xml/report_dashboard.xml',
            'octa_report/static/src/js/report_dashboard.js',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
