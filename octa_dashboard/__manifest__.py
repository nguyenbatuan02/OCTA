{
    'name': 'OCTA Dashboard',
    'version': '17.0.1.0.0',
    'category': 'Project',
    'summary': 'Bảng thông tin công việc OCTA',
    'depends': ['web', 'project', 'octa_project'],
    'data': [
        'security/ir.model.access.csv',
        'views/dashboard_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'octa_dashboard/static/src/xml/dashboard_template.xml',
            'octa_dashboard/static/src/js/dashboard.js',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}