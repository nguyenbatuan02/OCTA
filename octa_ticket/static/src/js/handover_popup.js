/** @odoo-module **/
/**
 * Handover Popup Service
 *
 * Lắng nghe bus.bus channel 'octa_handover_notification'.
 * Khi NV ca sau nhận được thông báo bàn giao → hiện dialog popup
 * với 2 lựa chọn: "Xác nhận nhận tất cả" hoặc "Để sau".
 *
 * Odoo 17 dùng Owl component + service registry.
 */

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";
import { Component, useState, onWillStart } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";

// ── Dialog Component ──────────────────────────────────────────────

class HandoverNotificationDialog extends Component {
    static template = "octa_ticket.HandoverNotificationDialog";
    static components = { Dialog };
    static props = {
        count:     { type: Number },
        fromUser:  { type: String },
        shift:     { type: String },
        taskIds:   { type: Array },
        onConfirm: { type: Function },
        onLater:   { type: Function },
        close:     { type: Function },
    };

    setup() {
        this.state = useState({ loading: false });
    }

    async onClickConfirm() {
        this.state.loading = true;
        try {
            await this.props.onConfirm(this.props.taskIds);
            this.props.close();
        } finally {
            this.state.loading = false;
        }
    }

    onClickLater() {
        this.props.onLater();
        this.props.close();
    }
}

// ── Service ───────────────────────────────────────────────────────

const handoverPopupService = {
    dependencies: ["bus_service", "dialog", "orm", "notification", "action"],

    start(env, { bus_service, dialog, orm, notification, action }) {

        // Lắng nghe notification từ server (bus.bus._sendone)
        bus_service.subscribe("octa_handover_notification", async (payload) => {
            if (!payload || payload.type !== "handover") return;

            const { count, from_user, shift, task_ids, message } = payload;

            // Hiện popup dialog
            dialog.add(HandoverNotificationDialog, {
                count:    count,
                fromUser: from_user,
                shift:    shift,
                taskIds:  task_ids,

                onConfirm: async (ids) => {
                    // Gọi method bulk confirm trên server
                    await orm.call(
                        "project.task",
                        "action_confirm_handover_bulk",
                        [ids],
                    );
                    notification.add(
                        _t("Đã xác nhận nhận %(count)s ticket từ ca trước.", { count }),
                        { type: "success", sticky: false }
                    );
                    // Reload action hiện tại để list view cập nhật
                    action.doAction({ type: "ir.actions.client", tag: "reload" });
                },

                onLater: () => {
                    // NV chọn "Để sau" → chỉ dismiss popup
                    // Vẫn thấy ticket trong menu "Ticket được bàn giao cho tôi"
                    notification.add(
                        _t("Bạn có %(count)s ticket chờ xác nhận nhận bàn giao.", { count }),
                        { type: "warning", sticky: true }
                    );
                },
            });
        });

        // Start bus listener khi service khởi động
        bus_service.start();
    },
};

registry.category("services").add("octa_handover_popup", handoverPopupService);