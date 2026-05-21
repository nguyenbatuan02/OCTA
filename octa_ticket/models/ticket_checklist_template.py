# -*- coding: utf-8 -*-
from odoo import models, fields

# FIX: import constants từ project_task thay vì định nghĩa lại
# → 1 nguồn duy nhất, không bao giờ lệch nhau
from .project_task import CSKH_ISSUE_TYPES, VH_ISSUE_TYPES


class TicketChecklistTemplate(models.Model):
    _name = 'ticket.checklist.template'
    _description = 'Checklist Template theo Issue Type'
    _order = 'issue_type, sequence'

    issue_type = fields.Selection(
       
        CSKH_ISSUE_TYPES + VH_ISSUE_TYPES,
        string='Loại sự cố / đầu việc',
        required=True,
        index=True,
    )
    sequence = fields.Integer('Thứ tự', default=10)
    name     = fields.Char('Bước thực hiện', required=True)