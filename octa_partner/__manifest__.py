# -*- coding: utf-8 -*-
{
    'name': 'Octa Partner',
    'version': '17.0.1.0.0',
    'category': 'Octa',
    'summary': 'Extend res.partner: NCC, đại lý, hạn mức công nợ, phân hạng, ranh đỏ',
    'description': """
        Mở rộng res.partner cho hệ thống Octa:
        - Phân loại: NCC / Đại lý / Cả hai
        - Phân hạng đại lý: A / B / C
        - Hạn mức công nợ theo từng đối tác
        - SLA cam kết NCC
        - Tỷ trọng tập trung: ranh đỏ NCC >50%, đại lý >40%
        - Cron kiểm tra ranh đỏ công nợ và tập trung hằng ngày
    """,
    'author': 'Octa',
    'depends': [
        'sale',         
        'purchase',     
        'account',     
        'octa_base',    
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/octa_partner_rules.xml',
        'data/ir_cron.xml',
        'views/res_partner_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}