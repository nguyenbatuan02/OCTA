# Odoo 17 - Docker Setup

##  Giới thiệu

Project này dùng Docker để chạy:

* Odoo 17
* PostgreSQL
* Nginx (reverse proxy + SSL)

---

##  Quick Start (chạy nhanh)

```bash
git clone https://khodichvu.myvnc.com:8443/octa-product/odoo-enhance.git
cd odoo-enhance
docker compose up -d
```

👉 Sau đó truy cập:

```
http://localhost:8069
```

---

##  1. Cài Docker

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

sudo usermod -aG docker $USER
sudo newgrp docker
```

Kiểm tra:

```bash
docker ps
```

---

##  2. Setup project

```bash
sudo mkdir /opt/odoo
sudo chown -R $USER:$USER /opt/odoo
cd /opt/odoo

git clone https://khodichvu.myvnc.com:8443/octa-product/odoo-enhance.git .
```

---

##  3. Start hệ thống

```bash
docker compose up -d
```

---

##  4. Cấu hình domain (optional)

Trỏ domain về IP server:

```bash
export DOMAIN=your-domain.com
```

---

##  5. Setup SSL

```bash
docker run -it --rm --name certbot \
  -v "/opt/odoo/certbot/conf:/etc/letsencrypt" \
  -v "/opt/odoo/certbot/logs:/var/log/letsencrypt" \
  -v "/opt/odoo/certbot/data:/var/www/html" \
  certbot/certbot certonly --webroot -w /var/www/html \
  -d $DOMAIN \
  --email your-email@example.com \
  --agree-tos --no-eff-email
```

---

##  6. Cấu hình Nginx

```bash
mv /opt/odoo/nginx/conf.d/default.conf /opt/odoo/nginx/conf.d/default.conf.disabled

sed -i "s|\[DOMAIN\]|$DOMAIN|g" /opt/odoo/nginx/conf.d/default-ssl.conf.disabled

mv /opt/odoo/nginx/conf.d/default-ssl.conf.disabled /opt/odoo/nginx/conf.d/default.conf
```

---

##  Reload Nginx

```bash
docker compose exec nginx nginx -t
docker compose exec nginx nginx -s reload
```

---

##  Truy cập

* Không SSL: http://localhost:8069
* Có domain: https://your-domain.com

