import base64
from io import BytesIO
from datetime import timedelta

from odoo import models, fields
from odoo.exceptions import UserError

import openpyxl


ISSUE_TYPE_MAP = {
    'cs01': 'card_error',
    'khiếu nại thẻ không nạp được':          'card_error',
    'cs02': 'topup_error',
    'khiếu nại topup lỗi':                   'topup_error',
    'cs03': 'gateway_39',
    'theo dõi cổng 39':                      'gateway_39',
    'theo dõi cổng 39 / hỗn hợp':           'gateway_39',
    'cs04': 'gateway_70',
    'cảnh báo tồn kho cổng 70':             'gateway_70',
    'cảnh báo tồn kho cổng 70 / vina':      'gateway_70',
    'cs05': 'deposit_complaint',
    'khiếu nại nạp tiền tài khoản octa':    'deposit_complaint',
    'cs06': 'txn_monitor',
    'kiểm tra giao dịch mua hàng':           'txn_monitor',
    'cs07': 'shift_tool_check',
    'kiểm tra công cụ đầu ca':              'shift_tool_check',
    'kiểm tra công cụ, dụng cụ trước ca':   'shift_tool_check',
    'cs08': 'shift_sales_check',
    'kiểm tra điều kiện bán hàng':          'shift_sales_check',
    'kiểm tra điều kiện bán hàng hệ thống': 'shift_sales_check',
    'cs09': 'miniapp_check',
    'kiểm tra web / mini app':              'miniapp_check',
    'kiểm tra công cụ bán hàng hệ thống':   'miniapp_check',
    'cs10': 'msg_channels',
    'theo dõi kênh phản ánh khách hàng':    'msg_channels',
    'theo dõi kênh phản ánh':               'msg_channels',
}

TICKET_TYPE_MAP = {
    'card_error':        'incident',
    'topup_error':       'incident',
    'deposit_complaint': 'incident',
    'gateway_39':        'periodic',
    'gateway_70':        'periodic',
    'txn_monitor':       'periodic',
    'shift_tool_check':  'shift',
    'shift_sales_check': 'shift',
    'miniapp_check':     'shift',
    'msg_channels':      'continuous',
}

SLA_MINUTES = {
    'card_error':        10,
    'topup_error':       15,
    'gateway_39':        20,
    'gateway_70':        60,
    'deposit_complaint': 15,
    'txn_monitor':       30,
    'shift_tool_check':  10,
    'shift_sales_check': 10,
    'miniapp_check':     10,
    'msg_channels':       3,
}

NETWORK_MAP = {
    'viettel':   'viettel',
    'vinaphone': 'vina',
    'vina':      'vina',
    'mobifone':  'mobi',
    'mobi':      'mobi',
}

SOURCE_COMPLAINT_MAP = {
    'chat':      'chat',
    'email':     'email',
    'tổng đài':  'hotline',
    'hotline':   'hotline',
    'zalo':      'zalo',
    'telegram':  'telegram',
    'tawkto':    'tawkto',
    'tawk.to':   'tawkto',
    'trực tiếp': 'walk_in',
}


class TicketImportWizard(models.TransientModel):
    _name = 'ticket.import.wizard'
    _description = 'Import Ticket từ Excel'

    file       = fields.Binary(string='File Excel', required=True)
    filename   = fields.Char()
    project_id = fields.Many2one('project.project', string='Dự án', required=True)

    auto_close = fields.Boolean(
        'Đánh dấu hoàn thành khi import',
        default=True,
        help='Tự động chuyển ticket sang stage Hoàn tất, tick hết checklist và set date_closed'
    )

    # Kết quả
    result_total   = fields.Integer('Tổng dòng',  readonly=True)
    result_success = fields.Integer('Thành công', readonly=True)
    result_fail    = fields.Integer('Lỗi',        readonly=True)
    result_log     = fields.Text('Chi tiết lỗi',  readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done',  'Done'),
    ], default='draft')

    def action_import(self):
        if not self.file:
            raise UserError('Vui lòng chọn file Excel.')

        try:
            wb = openpyxl.load_workbook(
                filename=BytesIO(base64.b64decode(self.file)),
                read_only=True, data_only=True
            )
        except Exception as e:
            raise UserError('Không đọc được file: %s' % str(e))

        ws   = wb.active
        rows = list(ws.iter_rows(values_only=True))

        if len(rows) < 2:
            raise UserError('File không có dữ liệu (cần ít nhất 1 dòng header + 1 dòng data).')

        header = [str(c).strip().lower() if c else '' for c in rows[0]]

        def col(name):
            try:
                return header.index(name)
            except ValueError:
                return None

        IDX = {
            'ten_dau_viec':       col('tên đầu việc'),
            'issue_type':         col('loại sự cố (code)'),
            'customer_info':      col('thông tin khách hàng'),
            'source_complaint':   col('nguồn phản ánh'),
            'buy_datetime':       col('thời điểm mua/in'),
            'ncc':                col('nhà cung cấp (ncc)'),
            'card_code':          col('mã / serial thẻ'),
            'network':            col('nhà mạng'),
            'transaction_id':     col('transaction id'),
            'phone':              col('số điện thoại'),
            'amount':             col('số tiền nạp'),
            'bank_name':          col('ngân hàng chuyển'),
            'gateway_name':       col('tên cổng'),
            'assignee':           col('người thực hiện (email)'),
        }

        Task = self.env['project.task']
        User = self.env['res.users']

        closed_stage = None
        if self.auto_close:
            closed_stage = self.env['project.task.type'].search([
                ('fold', '=', True),
                ('user_id', '=', False),
            ], order='sequence asc', limit=1)

        success, fail, log = 0, 0, []

        for i, row in enumerate(rows[1:], start=2):

            def cell(key):
                idx = IDX.get(key)
                if idx is None or idx >= len(row):
                    return ''
                v = row[idx]
                return str(v).strip() if v is not None else ''

            raw = cell('issue_type').lower() or cell('ten_dau_viec').lower()
            issue_type = ISSUE_TYPE_MAP.get(raw)
            if not issue_type:
                fail += 1
                log.append(f'Dòng {i}: Không nhận diện được loại sự cố "{raw}"')
                continue

            ticket_type = TICKET_TYPE_MAP.get(issue_type, 'incident')

            minutes = SLA_MINUTES.get(issue_type)
            sla_deadline = (
                fields.Datetime.now() + timedelta(minutes=minutes)
                if minutes else False
            )

            network = NETWORK_MAP.get(cell('network').lower()) or False
            source_complaint = SOURCE_COMPLAINT_MAP.get(
                cell('source_complaint').lower()
            ) or False

            raw_dt = cell('buy_datetime')
            buy_datetime = False
            if raw_dt:
                try:
                    from datetime import datetime
                    buy_datetime = datetime.strptime(raw_dt, '%Y-%m-%d %H:%M:%S')
                except Exception:
                    try:
                        buy_datetime = datetime.strptime(raw_dt, '%d/%m/%Y %H:%M')
                    except Exception:
                        buy_datetime = False

            # amount
            raw_amount = cell('amount')
            try:
                amount = float(raw_amount) if raw_amount else 0.0
            except ValueError:
                amount = 0.0

            # Assignee
            assignee_email = cell('assignee')
            user = (
                User.search([('email', '=', assignee_email)], limit=1)
                if assignee_email else False
            )

            vals = {
                'name':             cell('ten_dau_viec') or raw,
                'issue_type':       issue_type,
                'ticket_type':      ticket_type,
                'source':           'excel',
                'project_id':       self.project_id.id,
                'sla_deadline':     sla_deadline,
                'customer_info':    cell('customer_info') or False,
                'source_complaint': source_complaint,
                'buy_datetime':     buy_datetime,
                'ncc':              cell('ncc') or False,
                'card_code':        cell('card_code') or False,
                'network':          network,
                'transaction_id':   cell('transaction_id') or False,
                'phone':            cell('phone') or False,
                'amount':           amount,
                'bank_name':        cell('bank_name') or False,
                'gateway_name':     cell('gateway_name') or False,
            }
            if user:
                vals['user_ids'] = [(6, 0, [user.id])]

            try:
                task = Task.create(vals)
                # _generate_checklist() tự chạy trong create()

                if self.auto_close and closed_stage:
                    task.write({
                        'stage_id':    closed_stage.id,
                        'date_closed': fields.Datetime.now(),
                    })
                    task.checklist_ids.write({'done': True})

                success += 1

            except Exception as e:
                fail += 1
                log.append(f'Dòng {i}: Lỗi tạo ticket — {str(e)}')

        self.write({
            'result_total':   success + fail,
            'result_success': success,
            'result_fail':    fail,
            'result_log':     '\n'.join(log) if log else 'Không có lỗi.',
            'state':          'done',
        })

        return {
            'type':      'ir.actions.act_window',
            'res_model': self._name,
            'res_id':    self.id,
            'view_mode': 'form',
            'target':    'new',
        }
    
    def action_reset(self):
        self.write({
            'file': False,
            'filename': False,
            'result_total': 0,
            'result_success': 0,
            'result_fail': 0,
            'result_log': False,
            'state': 'draft',
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }