# -*- coding: utf-8 -*-
import json
from odoo import models, fields, api


class Vd6ApiLog(models.Model):
    """Lưu mỗi lần Portal gọi API — dùng chống trùng (idempotency) & tra soát."""
    _name = 'octa.vd6.api.log'
    _description = 'Nhật ký API Vòng đời 6'
    _order = 'create_date desc'

    request_id = fields.Char('Request ID', index=True, required=True)
    endpoint = fields.Char('Endpoint', required=True)
    ma_ticket = fields.Char('Mã ticket')
    response_json = fields.Text('Response đã trả')

    @api.model
    def get_saved(self, request_id):
        """Trả về dict response đã lưu cho request_id (hoặc None)."""
        if not request_id:
            return None
        rec = self.sudo().search([('request_id', '=', request_id)], limit=1)
        if rec and rec.response_json:
            try:
                return json.loads(rec.response_json)
            except Exception:
                return None
        return None

    @api.model
    def save(self, request_id, endpoint, ma_ticket, response_dict):
        if not request_id:
            return
        self.sudo().create({
            'request_id': request_id,
            'endpoint': endpoint,
            'ma_ticket': ma_ticket or '',
            'response_json': json.dumps(response_dict, ensure_ascii=False),
        })
