# -*- coding: utf-8 -*-
import json
from odoo import http, fields
from odoo.http import request

from ..models.vd6_common import (
    VD6_TH, VD6_PHUONG_AN, VD6_NGUON, VD6_GD_STATUS,
)

BASE = '/api/octa/v1'
TH_KEYS = {k for k, _ in VD6_TH}
PA_KEYS = {k for k, _ in VD6_PHUONG_AN}
NGUON_KEYS = {k for k, _ in VD6_NGUON}
GD_KEYS = {k for k, _ in VD6_GD_STATUS}


def _json(payload, status=200):
    return request.make_response(
        json.dumps(payload, ensure_ascii=False, default=str),
        headers=[('Content-Type', 'application/json; charset=utf-8')],
        status=status,
    )


def _ok(data):
    return _json({'success': True, 'data': data, 'error': None})


def _err(code, message, status=200):
    return _json({'success': False, 'data': None,
                  'error': {'code': code, 'message': message}}, status=status)


def _check_key():
    """True nếu X-Api-Key hợp lệ."""
    expected = request.env['ir.config_parameter'].sudo().get_param('octa_vd6.api_key')
    got = request.httprequest.headers.get('X-Api-Key')
    return bool(expected) and got == expected


def _body():
    raw = request.httprequest.get_data(as_text=True) or '{}'
    return json.loads(raw)


def _iso(dt):
    return fields.Datetime.to_string(dt) if dt else None


def _ticket_dict(t):
    """Serialize ticket theo các trường mục 5.5."""
    return {
        'ma_ticket': t.vd6_ma_ticket,
        'ma_gd_goc': t.vd6_ma_gd_goc,
        'trang_thai_gd_goc': t.vd6_trang_thai_gd_goc,
        'so_tien_gia_tri': t.vd6_so_tien,
        'loai_ticket': t.vd6_loai_ticket,
        'loai_th': t.vd6_loai_th,
        'nguon_phat_hien': t.vd6_nguon_phat_hien,
        'mo_ta_su_vu': t.description or '',
        'trang_thai': t.vd6_status,
        'nhom_phu_trach': t.get_vd6_teams(),
        'phuong_an_de_xuat': t.vd6_phuong_an_de_xuat,
        'phuong_an_da_duyet': t.vd6_phuong_an_da_duyet,
        'nguoi_tao': t.vd6_nguoi_tao_portal,
        'nguoi_xu_ly': t.vd6_nguoi_xu_ly_portal,
        'nguoi_duyet': t.user_ids[:1].name if t.user_ids else None,
        'ticket_khach_lien_ket': t.vd6_ticket_khach_lien_ket,
        'ma_phuong_an_da_thuc_hien': t.vd6_ma_pa_thuc_hien,
        'thoi_gian_tao': _iso(t.create_date),
        'thoi_gian_dong': _iso(t.date_closed),
        'ket_qua_cuoi': t.result_final,
    }


def _open_customer_ticket(ma_gd_goc):
    """Ticket khách đang mở của giao dịch (chưa DA_DONG/TU_CHOI)."""
    return request.env['project.task'].sudo().search([
        ('is_vd6', '=', True),
        ('vd6_loai_ticket', '=', 'TICKET_KHACH'),
        ('vd6_ma_gd_goc', '=', ma_gd_goc),
        ('stage_id.fold', '=', False),
    ], limit=1)


class Vd6Controller(http.Controller):

    # ── API-1: Tạo ticket khách ─────────────────────────────────────
    @http.route(f'{BASE}/tickets', type='http', auth='public',
                methods=['POST'], csrf=False)
    def create_ticket(self, **kw):
        if not _check_key():
            return _err('UNAUTHORIZED', 'Sai hoặc thiếu X-Api-Key.', 401)
        try:
            b = _body()
        except Exception:
            return _err('VALIDATION_ERROR', 'Body không phải JSON hợp lệ.')

        req_id = b.get('request_id')
        saved = request.env['octa.vd6.api.log'].get_saved(req_id)
        if saved is not None:
            return _json(saved)

        # Validate
        required = ['request_id', 'ma_gd_goc', 'trang_thai_gd_goc', 'so_tien_gia_tri',
                    'loai_th', 'mo_ta_su_vu', 'nguon_phat_hien', 'phuong_an_de_xuat',
                    'nguoi_tao']
        missing = [f for f in required if b.get(f) in (None, '')]
        if missing:
            return _err('VALIDATION_ERROR', 'Thiếu trường bắt buộc: %s' % ', '.join(missing))
        if b['loai_th'] not in TH_KEYS:
            return _err('INVALID_TH', 'loai_th không thuộc TH1–TH8.')
        if b['phuong_an_de_xuat'] not in PA_KEYS:
            return _err('VALIDATION_ERROR', 'phuong_an_de_xuat không hợp lệ.')
        if str(b['trang_thai_gd_goc']) not in GD_KEYS:
            return _err('VALIDATION_ERROR', 'trang_thai_gd_goc không hợp lệ (0/2/3).')

        Task = request.env['project.task'].sudo()
        project = request.env.ref('octa_vd6.project_vd6')
        stage = Task._vd6_stage('MOI_TAO')

        # Ticket khách đã đóng trước đó của cùng giao dịch → liên kết truy vết
        prior = Task.search([
            ('is_vd6', '=', True), ('vd6_loai_ticket', '=', 'TICKET_KHACH'),
            ('vd6_ma_gd_goc', '=', b['ma_gd_goc']), ('stage_id.fold', '=', True),
        ], order='create_date desc', limit=1)

        task = Task.create({
            'name': 'VĐ6 %s · %s' % (b['loai_th'], b['ma_gd_goc']),
            'project_id': project.id,
            'stage_id': stage.id,
            'is_vd6': True,
            'source': 'api',
            'dept': 'cskh',
            'vd6_loai_ticket': 'TICKET_KHACH',
            'vd6_loai_th': b['loai_th'],
            'vd6_ma_gd_goc': b['ma_gd_goc'],
            'vd6_trang_thai_gd_goc': str(b['trang_thai_gd_goc']),
            'vd6_so_tien': b['so_tien_gia_tri'],
            'vd6_nguon_phat_hien': b['nguon_phat_hien'],
            'vd6_phuong_an_de_xuat': b['phuong_an_de_xuat'],
            'vd6_request_id': req_id,
            'vd6_nguoi_tao_portal': b['nguoi_tao'],
            'description': b['mo_ta_su_vu'],
            'vd6_ticket_khach_lien_ket': prior.vd6_ma_ticket if prior else None,
        })
        task.vd6_ma_ticket = 'TK-%06d' % task.id

        # TH5/6/7 → tự sinh ticket trách nhiệm nội bộ (độc lập, ẩn với khách)
        task._vd6_create_internal_ticket()

        request.env['octa.audit.log'].log_action(
            action_type='create', object_model='project.task',
            object_id=task.id, object_name=task.vd6_ma_ticket,
            reason='API-1 tạo ticket VĐ6 %s' % b['loai_th'], scope_tag='bigtel')

        data = {
            'ma_ticket': task.vd6_ma_ticket,
            'trang_thai': 'MOI_TAO',
            'thoi_gian_tao': _iso(task.create_date),
            'loai_th': task.vd6_loai_th,
            'nhom_phu_trach': task.get_vd6_teams(),
            'phuong_an_de_xuat': task.vd6_phuong_an_de_xuat,
            'ticket_khach_lien_ket': task.vd6_ticket_khach_lien_ket,
        }
        resp = {'success': True, 'data': data, 'error': None}
        request.env['octa.vd6.api.log'].save(req_id, 'API-1', task.vd6_ma_ticket, resp)
        return _json(resp)

    # ── API-2: Lấy ticket theo giao dịch ────────────────────────────
    @http.route(f'{BASE}/tickets', type='http', auth='public',
                methods=['GET'], csrf=False)
    def list_tickets(self, **kw):
        if not _check_key():
            return _err('UNAUTHORIZED', 'Sai hoặc thiếu X-Api-Key.', 401)
        ma_gd = request.httprequest.args.get('ma_gd_goc')
        if not ma_gd:
            return _err('VALIDATION_ERROR', 'Thiếu ma_gd_goc.')
        tasks = request.env['project.task'].sudo().search([
            ('is_vd6', '=', True), ('vd6_loai_ticket', '=', 'TICKET_KHACH'),
            ('vd6_ma_gd_goc', '=', ma_gd),
        ], order='create_date desc')
        return _ok([_ticket_dict(t) for t in tasks])

    # ── API-3: Kiểm tra điều kiện thực hiện ─────────────────────────
    @http.route(f'{BASE}/tickets/check-condition', type='http', auth='public',
                methods=['POST'], csrf=False)
    def check_condition(self, **kw):
        if not _check_key():
            return _err('UNAUTHORIZED', 'Sai hoặc thiếu X-Api-Key.', 401)
        try:
            b = _body()
        except Exception:
            return _err('VALIDATION_ERROR', 'Body không phải JSON hợp lệ.')
        ma_gd = b.get('ma_gd_goc')
        pa = b.get('phuong_an_du_kien')
        if not ma_gd or not pa:
            return _err('VALIDATION_ERROR', 'Thiếu ma_gd_goc hoặc phuong_an_du_kien.')

        t = _open_customer_ticket(ma_gd)
        if not t:
            return _ok({'duoc_phep': False, 'ma_ticket_lien_quan': None,
                        'phuong_an_de_xuat': None, 'phuong_an_da_duyet': False,
                        'nguoi_duyet': None, 'ly_do_tu_choi': 'Không có ticket đang mở.'})
        if t.vd6_status != 'DA_DUYET':
            return _ok({'duoc_phep': False, 'ma_ticket_lien_quan': t.vd6_ma_ticket,
                        'phuong_an_de_xuat': t.vd6_phuong_an_de_xuat,
                        'phuong_an_da_duyet': False, 'nguoi_duyet': None,
                        'ly_do_tu_choi': 'Phương án chưa được phê duyệt.'})
        if t.vd6_phuong_an_de_xuat != pa:
            return _ok({'duoc_phep': False, 'ma_ticket_lien_quan': t.vd6_ma_ticket,
                        'phuong_an_de_xuat': t.vd6_phuong_an_de_xuat,
                        'phuong_an_da_duyet': True, 'nguoi_duyet': None,
                        'ly_do_tu_choi': 'Phương án không khớp phương án đã duyệt.'})
        return _ok({'duoc_phep': True, 'ma_ticket_lien_quan': t.vd6_ma_ticket,
                    'phuong_an_de_xuat': t.vd6_phuong_an_de_xuat,
                    'phuong_an_da_duyet': True,
                    'nguoi_duyet': t.user_ids[:1].name if t.user_ids else None,
                    'ly_do_tu_choi': None})

    # ── API-4: Cập nhật kết quả thực hiện ───────────────────────────
    @http.route(f'{BASE}/tickets/execution-result', type='http', auth='public',
                methods=['POST'], csrf=False)
    def execution_result(self, **kw):
        if not _check_key():
            return _err('UNAUTHORIZED', 'Sai hoặc thiếu X-Api-Key.', 401)
        try:
            b = _body()
        except Exception:
            return _err('VALIDATION_ERROR', 'Body không phải JSON hợp lệ.')
        req_id = b.get('request_id')
        saved = request.env['octa.vd6.api.log'].get_saved(req_id)
        if saved is not None:
            return _json(saved)

        for f in ['request_id', 'ma_ticket', 'ma_gd_goc', 'trang_thai_gd_goc',
                  'phuong_an_da_thuc_hien', 'nguoi_xu_ly', 'thoi_gian_thuc_hien']:
            if b.get(f) in (None, ''):
                return _err('VALIDATION_ERROR', 'Thiếu trường bắt buộc: %s' % f)

        t = request.env['project.task'].sudo().search(
            [('vd6_ma_ticket', '=', b['ma_ticket'])], limit=1)
        if not t:
            return _err('TICKET_NOT_FOUND', 'Không tìm thấy ticket %s.' % b['ma_ticket'])
        if t.vd6_status != 'DA_DUYET':
            return _err('TICKET_CLOSED', 'Ticket không ở trạng thái Đã duyệt, không thể cập nhật.')
        if t.vd6_phuong_an_de_xuat != b['phuong_an_da_thuc_hien']:
            return _err('PLAN_MISMATCH', 'Phương án thực hiện không khớp phương án đã duyệt.')

        t.write({
            'vd6_ma_pa_thuc_hien': b.get('ma_phuong_an_da_thuc_hien') or None,
            'vd6_nguoi_xu_ly_portal': b['nguoi_xu_ly'],
            'vd6_trang_thai_gd_goc': str(b['trang_thai_gd_goc']),
        })
        request.env['octa.audit.log'].log_action(
            action_type='write', object_model='project.task',
            object_id=t.id, object_name=t.vd6_ma_ticket,
            reason='API-4 cập nhật kết quả %s' % b['phuong_an_da_thuc_hien'],
            scope_tag='bigtel')

        resp = {'success': True, 'error': None, 'data': {
            'ma_ticket': t.vd6_ma_ticket,
            'thoi_gian_cap_nhat': _iso(fields.Datetime.now()),
            'error_message': None}}
        request.env['octa.vd6.api.log'].save(req_id, 'API-4', t.vd6_ma_ticket, resp)
        return _json(resp)

    # ── API-5: Đóng ticket (riêng TH4) ──────────────────────────────
    @http.route(f'{BASE}/tickets/close', type='http', auth='public',
                methods=['POST'], csrf=False)
    def close_ticket(self, **kw):
        if not _check_key():
            return _err('UNAUTHORIZED', 'Sai hoặc thiếu X-Api-Key.', 401)
        try:
            b = _body()
        except Exception:
            return _err('VALIDATION_ERROR', 'Body không phải JSON hợp lệ.')
        req_id = b.get('request_id')
        saved = request.env['octa.vd6.api.log'].get_saved(req_id)
        if saved is not None:
            return _json(saved)

        for f in ['request_id', 'loai_th', 'ma_gd_goc']:
            if b.get(f) in (None, ''):
                return _err('VALIDATION_ERROR', 'Thiếu trường bắt buộc: %s' % f)

        t = _open_customer_ticket(b['ma_gd_goc'])
        if not t:
            return _err('NO_OPEN_TICKET', 'Không có ticket đang mở cho giao dịch.')
        if t.vd6_loai_th != 'TH4':
            return _err('VALIDATION_ERROR', 'API-5 chỉ áp dụng cho TH4.')

        t.write({'stage_id': request.env['project.task'].sudo()._vd6_stage('DA_DONG').id,
                 'result_final': 'success'})
        request.env['octa.audit.log'].log_action(
            action_type='stop', object_model='project.task',
            object_id=t.id, object_name=t.vd6_ma_ticket,
            reason='API-5 đóng ticket TH4 (Portal tự khớp)', scope_tag='bigtel')

        resp = {'success': True, 'error': None, 'data': {
            'ma_ticket': t.vd6_ma_ticket,
            'thoi_gian_cap_nhat': _iso(fields.Datetime.now())}}
        request.env['octa.vd6.api.log'].save(req_id, 'API-5', t.vd6_ma_ticket, resp)
        return _json(resp)
