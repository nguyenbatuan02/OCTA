# -*- coding: utf-8 -*-
{
    'name': 'Octa Approval',
    'version': '17.0.1.0.0',
    'category': 'Octa',
    'summary': 'Workflow phê duyệt 5 tầng cho hệ thống Octa',
    'description': """
        Workflow phê duyệt tập trung cho Octa:
        - Hoàn tiền / nạp bù (WF-BT-06, WF-PP-06, WF-KD-06)
        - Mở / đóng cổng (WF-BT-05, WF-PP-05, WF-KD-05)
        - NCC mới (WF-PP-01)
        - Giá / chiết khấu (WF-PP-03, WF-KD-03)
        - Công nợ đại lý (WF-PP-07, WF-KD-07)

        Nguyên tắc:
        - Auto-escalate theo hạn mức cấu hình trong octa.approval.config
        - Không tự tạo + tự duyệt cùng phiếu (SoD)
        - Vượt hạn mức: disable nút Duyệt, chỉ hiện nút Escalate
        - Mọi thao tác ghi audit log
    """,
    'author': 'Octa',
    'depends': [
        'octa_base',    
        'octa_ticket',  
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'views/octa_approval_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}