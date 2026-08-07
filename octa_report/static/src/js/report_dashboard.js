/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class OctaReportDashboard extends Component {
    static template = "octa_report.ReportDashboard";

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");

        this.state = useState({
            data: { summary: {}, roles: [], catalog: [] },
            reports: [],
            activeTab: "all",
            catalogRole: "all",
            tabs: [
                { key: "all", label: "Tất cả" },
                { key: "draft", label: "Nháp" },
                { key: "submitted", label: "Chờ duyệt" },
                { key: "overdue", label: "Quá hạn" },
            ],
        });

        onWillStart(async () => {
            await this.loadData();
            await this.loadReports();
        });
    }

    async loadData() {
        this.state.data = await this.orm.call("octa.report", "get_report_dashboard", []);
    }

    async loadReports() {
        this.state.reports = await this.orm.call("octa.report", "get_report_list", [], {
            state_filter: this.state.activeTab,
        });
    }

    async switchTab(tab) {
        this.state.activeTab = tab;
        await this.loadReports();
    }

    setCatalogRole(role) {
        this.state.catalogRole = role;
    }

    get filteredCatalog() {
        const role = this.state.catalogRole;
        if (role === "all") {
            return this.state.data.catalog;
        }
        return this.state.data.catalog.filter((c) => c.owner_role === role);
    }

    async createReport(catalogId) {
        const act = await this.orm.call("octa.report", "create_from_catalog", [catalogId]);
        this.action.doAction(act);
    }

    openReport(id) {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "octa.report",
            res_id: id,
            views: [[false, "form"]],
            target: "current",
        });
    }

    stateLabel(s) {
        return { draft: "Nháp", submitted: "Đã nộp", approved: "Đã duyệt" }[s] || s;
    }
}

registry.category("actions").add("octa_report_dashboard", OctaReportDashboard);
