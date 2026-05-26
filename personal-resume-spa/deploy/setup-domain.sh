#!/bin/bash
# 在服务器上配置 hmdresume.xyz → 本地 8080（需 root/sudo）
set -e

CONF_NAME="hmdresume"
SITE_CONF="/etc/nginx/sites-available/${CONF_NAME}"
ENABLED="/etc/nginx/sites-enabled/${CONF_NAME}"
APP_DIR="your_app_directory"  # 替换为你的应用目录路径

sudo cp "$APP_DIR/deploy/nginx-hmdresume.conf" "$SITE_CONF"
sudo ln -sf "$SITE_CONF" "$ENABLED"
sudo nginx -t
sudo systemctl reload nginx

echo "Nginx 已配置：http://hmdresume.xyz"
echo "请确保域名 DNS A 记录指向本机公网 IP"
