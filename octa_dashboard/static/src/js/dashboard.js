/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class OctaDashboard extends Component {
    static template = "octa_dashboard.DashboardMain";

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");

        this.state = useState({
            data: {},
            tasks: [],
            activeTab: "my_tasks",
            tabs: [
                { key: "my_tasks", label: "Việc tôi làm" },
                { key: "assigned", label: "Việc tôi giao" },
                { key: "supervisor", label: "Tôi giám sát" },
                { key: "related", label: "Tôi liên quan" },
            ],
        });

        onWillStart(async () => {
            await this.loadData();
            await this.loadTasks();
        });
    }

    async loadData() {
        this.state.data = await this.orm.call("octa.dashboard", "get_dashboard_data", []);
    }

    async loadTasks() {
        this.state.tasks = await this.orm.call("octa.dashboard", "get_task_list", [], {
            tab: this.state.activeTab,
        });
    }

    async switchTab(tab) {
        this.state.activeTab = tab;
        await this.loadTasks();
    }

    openTask(taskId) {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "project.task",
            res_id: taskId,
            views: [[false, "form"]],
            target: "current",
        });
    }

    openTaskList(type) {
        const uid = this.env.services.user.userId;

        let domain = [];

        if (type === "my_tasks") {
            domain = [["user_ids", "in", [uid]]];
        } else if (type === "assigned") {
            domain = [["create_uid", "=", uid]];
        } else if (type === "supervisor") {
            domain = [["supervisor_ids", "in", [uid]]];
        } else if (type === "related") {
            domain = [["related_user_ids", "in", [uid]]];
        }

        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Danh sách công việc",
            res_model: "project.task",
            views: [
                [false, "list"],
                [false, "form"]
            ],
            domain: domain,
            target: "current",
        });
    }

}

registry.category("actions").add("octa_dashboard", OctaDashboard);