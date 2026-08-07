# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, time
from odoo import models, fields, api


def nth_working_day(year, month, n):
    """datetime.date là ngày làm việc thứ n của tháng (bỏ T7/CN)."""
    d = datetime(year, month, 1).date()
    count = 0
    while True:
        if d.weekday() < 5:
            count += 1
            if count >= n:
                return d
        d += timedelta(days=1)


ROLE_LABELS = {
    'cskh':  'CSKH',
    'ops':   'Vận hành',
    'lead':  'Lead CSKH & VH',
    'tdabg': 'Trưởng dự án Bigtel',
}
FREQ_LABELS = {
    'shift':    'Ca',
    'day':      'Ngày',
    'week':     'Tuần',
    'month':    'Tháng',
    'quarter':  'Quý',
    'periodic': 'Định kỳ',
    'adhoc':    'Đột xuất',
}


class OctaReportCatalog(models.Model):
    """
    Danh mục loại báo cáo (data-seeded từ tài liệu nghiệp vụ).

    Mỗi bộ phận/role có nhiều loại báo cáo với tần suất & hạn nộp khác nhau.
    octa.report tham chiếu 1 catalog để lấy role, tần suất, cách tính hạn nộp.
    """
    _name = 'octa.report.catalog'
    _description = 'Danh mục loại báo cáo Octa'
    _order = 'owner_role, sequence, code'

    code = fields.Char('Mã', required=True, index=True)
    name = fields.Char('Tên loại báo cáo', required=True, translate=False)
    owner_role = fields.Selection([
        ('cskh',  'CSKH'),
        ('ops',   'Vận hành'),
        ('lead',  'Lead CSKH & VH'),
        ('tdabg', 'Trưởng dự án Bigtel'),
    ], string='Bộ phận / vai trò', required=True, index=True)
    frequency = fields.Selection([
        ('shift',    'Ca'),
        ('day',      'Ngày'),
        ('week',     'Tuần'),
        ('month',    'Tháng'),
        ('quarter',  'Quý'),
        ('periodic', 'Định kỳ'),
        ('adhoc',    'Đột xuất'),
    ], string='Tần suất', required=True)
    recipients   = fields.Char('Người nhận')
    deadline_note = fields.Char('Hạn nộp (mô tả)')
    scope = fields.Selection([
        ('bigtel', 'Bigtel'), ('bigm', 'BigM'), ('utv', 'UTV'),
    ], string='Phạm vi', default='bigtel')
    sequence = fields.Integer('Thứ tự', default=10)
    active   = fields.Boolean('Đang dùng', default=True)

    _sql_constraints = [
        ('uniq_code', 'unique(code)', 'Mã loại báo cáo phải duy nhất.'),
    ]

    def compute_deadline(self, period_date, create_dt=None):
        """Tính hạn nộp cho 1 báo cáo theo tần suất của catalog này."""
        self.ensure_one()
        d = period_date
        if not d:
            return False
        freq = self.frequency
        if freq == 'shift':
            return datetime.combine(d, time(23, 59))
        if freq == 'day':
            return datetime.combine(d + timedelta(days=1), time(9, 30))
        if freq == 'week':
            next_mon = d + timedelta(days=7 - d.weekday())
            return datetime.combine(next_mon, time(10, 0))
        if freq == 'month':
            y, m = (d.year + 1, 1) if d.month == 12 else (d.year, d.month + 1)
            return datetime.combine(nth_working_day(y, m, 5), time(17, 0))
        if freq == 'quarter':
            # Tháng đầu quý kế tiếp
            q_first_month = ((d.month - 1) // 3 + 1) * 3 + 1
            y = d.year
            if q_first_month > 12:
                q_first_month, y = 1, d.year + 1
            return datetime.combine(nth_working_day(y, q_first_month, 5), time(17, 0))
        if freq == 'adhoc':
            base = create_dt or fields.Datetime.now()
            return base + timedelta(minutes=30)
        # periodic — mặc định cuối ngày kế tiếp
        return datetime.combine(d + timedelta(days=1), time(17, 0))
