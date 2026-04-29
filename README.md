# Odoo 17 - Docker Setup

##  Giới thiệu

Project này dùng Docker để chạy:

* Odoo 17
* PostgreSQL
* Nginx (reverse proxy + SSL)

Bao gồm các module custom:

* `octa_dashboard`
* `octa_ticket`
* `octa_project`

---

##  Quick Start

```bash
git clone https://khodichvu.myvnc.com:8443/octa-product/odoo-enhance.git
cd odoo-enhance
docker compose up -d
```

👉 Truy cập:

* http://localhost:8069 (local)
* hoặc domain nếu đã cấu hình

---

##  Cài module custom

### Bước 1: Bật Developer Mode

* Vào **Settings**
* Click **Activate Developer Mode**

---

### Bước 2: Update App List

* Vào **Apps**
* Click **Update Apps List** (hoặc “Cập nhật danh sách ứng dụng”)

---

### Bước 3: Tìm và cài module

* Trong Apps, search:

```
octa
```

👉 Cài lần lượt:

* `octa_dashboard`
* `octa_ticket`
* `octa_project`

---

##  Nếu không thấy module

Kiểm tra:

### 1. Addons path

* Đảm bảo folder module nằm trong addons path của Odoo (docker-compose / config)

---

### 2. Restart container

```bash
docker compose restart odoo
```

---

### 3. Update lại app list

→ quay lại Apps → Update Apps List

---

