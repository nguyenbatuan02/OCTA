# -*- coding: utf-8 -*-
{
    'name': 'Octa Base',
    'version': '17.0.1.0.0',
    'category': 'Octa',
    'summary': 'Nền tảng phân quyền, audit log và cấu hình hạn mức cho hệ thống Octa',
    'description': """
        Module nền tảng của hệ thống Octa trên Odoo 17.
        - Định nghĩa 6 security groups theo thứ bậc
        - Record rules lọc scope: Bigtel / BigM / UTV
        - Audit log model theo yêu cầu 5 năm
        - Cấu hình hạn mức phê duyệt và ngưỡng ranh đỏ
        - Sequences cho các đối tượng nghiệp vụ
    """,
    'author': 'Octa',
    'depends': ['base', 'mail'],
    'data': [
        # Security — load trước nhất
        'security/octa_groups.xml',
        'security/octa_record_rules.xml',
        'security/ir.model.access.csv',

        # Data
        'data/ir_sequence.xml',

        # Views
        'views/octa_approval_config_views.xml',
        'views/octa_audit_log_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
