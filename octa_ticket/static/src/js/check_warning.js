/** @odoo-module **/

import { registry } from "@web/core/registry";

const checkWarningService = {
    dependencies: ["bus_service", "notification"],
    start(env, { bus_service, notification }) {

        const activeOverdue = new Map();

        bus_service.subscribe("octa_check_warning", (payload) => {
            const { task_name, task_id, level } = payload;
            const isOverdue = level === "overdue";

            if (isOverdue && activeOverdue.has(task_id)) {
                return;
            }

            const remove = notification.add(
                `${isOverdue ? "QUÁ HẠN" : "Sắp đến giờ"} kiểm tra: ${task_name}`,
                {
                    title: isOverdue ? "Quá hạn kiểm tra!" : "Nhắc nhở",
                    type: isOverdue ? "danger" : "warning",
                    sticky: isOverdue,
                    onClose: () => {
                        activeOverdue.delete(task_id);
                    },
                    buttons: [
                        {
                            name: "Mở ticket",
                            primary: true,
                            onClick: () => {
                                activeOverdue.delete(task_id);
                                if (typeof remove === "function") remove();
                                env.services.action.doAction({
                                    type: "ir.actions.act_window",
                                    res_model: "project.task",
                                    res_id: task_id,
                                    views: [[false, "form"]],
                                });
                            },
                        },
                        ...(isOverdue ? [{
                            name: "Bỏ qua",
                            primary: false,
                            onClick: () => {
                                if (typeof remove === "function") remove();
                                activeOverdue.delete(task_id);
                            },
                        }] : []),
                    ],
                }
            );

            if (isOverdue) {
                activeOverdue.set(task_id, remove);
            }
        });
    },
};

registry.category("services").add("octa_check_warning", checkWarningService);