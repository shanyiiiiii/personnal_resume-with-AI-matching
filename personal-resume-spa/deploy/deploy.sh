#!/bin/bash
# 在 3080 服务器上部署个人简历站点（无需数据库）
set -e

APP_DIR="${APP_DIR:-/opt/personal-resume-spa}"
PORT="${PORT:-8080}"

echo "==> 部署目录: $APP_DIR"

sudo mkdir -p "$APP_DIR"
sudo rsync -av --exclude '.git' --exclude '__pycache__' --exclude '.venv' \
  ./ "$APP_DIR/"

cd "$APP_DIR"

if [ ! -f .env ]; then
  echo "请创建 $APP_DIR/.env 并填入 ZHIPU_API_KEY"
  cp .env.example .env
  echo "已复制 .env.example，请编辑后重新运行"
  exit 1
fi

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# systemd 服务（可选）
sudo tee /etc/systemd/system/resume-site.service > /dev/null <<EOF
[Unit]
Description=Personal Resume SPA
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$APP_DIR
EnvironmentFile=$APP_DIR/.env
ExecStart=$APP_DIR/.venv/bin/gunicorn -b 0.0.0.0:$PORT -w 2 server.app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable resume-site
sudo systemctl restart resume-site

echo "==> 部署完成！访问 http://$(hostname -I | awk '{print $1}'):$PORT"
echo "    若需外网访问，请在防火墙/云安全组放行 TCP $PORT"
