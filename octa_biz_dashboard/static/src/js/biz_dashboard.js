/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class OctaBizDashboard extends Component {
    static template = "octa_biz_dashboard.Main";

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({ d: null, loading: true, active: null });

        onWillStart(async () => {
            await this.reload();
        });
    }

    async reload() {
        this.state.loading = true;
        this.state.d = await this.orm.call("octa.biz.dashboard", "get_biz_dashboard", []);
        // Chọn dashboard đầu tiên còn dữ liệu làm mặc định
        const first = (this.state.d.menu || []).find((m) => m.available) || this.state.d.menu[0];
        this.state.active = first ? first.key : null;
        this.state.loading = false;
    }

    select(key) {
        this.state.active = key;
    }

    money(v) {
        return (v || 0).toLocaleString("vi-VN");
    }

    gateColor(s) {
        return { active: "#36b37e", warning: "#ffab00", closed: "#f56565", locked: "#c026d3" }[s] || "#999";
    }

    gateLabel(s) {
        return { active: "Hoạt động", warning: "Cảnh báo", closed: "Đóng", locked: "Khóa" }[s] || s;
    }

    openGateways() {
        this.action.doAction({
            type: "ir.actions.act_window", name: "Cổng API",
            res_model: "octa.gateway", views: [[false, "list"], [false, "form"]],
            target: "current",
        });
    }

    openPartner(id) {
        this.action.doAction({
            type: "ir.actions.act_window", res_model: "res.partner",
            res_id: id, views: [[false, "form"]], target: "current",
        });
    }
}

registry.category("actions").add("octa_biz_dashboard", OctaBizDashboard);
