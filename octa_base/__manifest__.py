# -*- coding: utf-8 -*-
{
    'name': 'Octa Base',
    'version': '17.0.1.1.0',
    'category': 'Octa',
    'summary': 'Nền tảng phân quyền, audit log và cấu hình hạn mức cho hệ thống Octa',
    'description': """
        Module nền tảng của hệ thống Octa trên Odoo 17.
        - Định nghĩa 6 security groups theo thứ bậc (implied_ids chain)
        - Audit log model bất biến, lưu trữ 5 năm
        - Cấu hình hạn mức phê duyệt và ngưỡng ranh đỏ (singleton)
        - Sequences cho approval, gateway command, alert
        - Record rules cho audit log theo scope
    """,
    'author': 'Octa',
    'depends': ['base', 'mail', 'project'],
    'data': [
        'security/octa_groups.xml',
        'security/ir.model.access.csv',
        'security/octa_record_rules.xml',
        'data/ir_sequence.xml',
        'data/octa_approval_config_data.xml',
        'views/octa_approval_config_views.xml',
        'views/octa_audit_log_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}