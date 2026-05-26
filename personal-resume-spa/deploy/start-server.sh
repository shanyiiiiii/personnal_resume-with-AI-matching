#!/bin/bash
# 在服务器上执行（路径 your_app_directory）
set -e

APP_DIR="your_app_directory"  # 替换为你的应用目录路径
PORT="${PORT:-8080}"
cd "$APP_DIR"

echo "==> 工作目录: $APP_DIR"

if [ ! -f .env ]; then
  echo "错误: 请先创建 $APP_DIR/.env 并填入 ZHIPU_API_KEY"
  exit 1
fi

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
pip install -r requirements.txt -q

pkill -f "gunicorn.*server.app:app" 2>/dev/null || true
sleep 1

nohup .venv/bin/gunicorn -b 0.0.0.0:$PORT -w 2 server.app:app \
  > "$APP_DIR/gunicorn.log" 2>&1 &

echo "==> 服务已启动 http://0.0.0.0:$PORT"
