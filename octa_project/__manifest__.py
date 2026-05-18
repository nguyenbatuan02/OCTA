# -*- coding: utf-8 -*-
{
    'name': 'Octa Project',
    'version': '17.0.2.0.0',
    'category': 'Octa',
    'summary': 'Nền tảng project.task mở rộng cho hệ thống Octa',
    'description': """
        Extend project.task với các field dùng chung toàn hệ thống:
        - scope: phân loại dữ liệu theo dự án (bigtel/bigm/utv)
        - dept: phân loại theo bộ phận (cskh/ops)
        - date_closed: thời điểm đóng task
        - related_user_ids: người liên quan
        - supervisor_ids: người giám sát
        - approver_id trên stage: người duyệt theo stage

        Stage data mặc định cho hệ thống Octa.
    """,
    'author': 'Octa',
    'depends': [
        'project',
        'octa_base',   #
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/project_stage_data.xml',     
        'views/project_task_type_views.xml',
        'views/project_task_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}