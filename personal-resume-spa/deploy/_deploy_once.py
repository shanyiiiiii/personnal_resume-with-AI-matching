#!/usr/bin/env python3
"""一次性部署脚本（勿提交含密码的版本）"""
import os
import stat
from pathlib import Path

import paramiko
from scp import SCPClient

HOST = "10.188.65.154"
USER = "yang324"
PASSWORD = "tougaobizhong324"
REMOTE = "/home/yang324/hanmengdie"
LOCAL = Path(r"C:\Users\15452\personal-resume-spa")

SKIP_DIRS = {".git", ".venv", "__pycache__", "node_modules"}
SKIP_FILES = {".env"}  # 单独写入

ENV_CONTENT = """ZHIPU_API_KEY=321f8b11f58d4da69edbe664de2dcf7f.0Gk80Xfjf1CQQfGU
ZHIPU_MODEL=glm-4-flash
PORT=8080
HOST=0.0.0.0
"""


def should_upload(path: Path) -> bool:
    parts = set(path.parts)
    if parts & SKIP_DIRS:
        return False
    if path.name in SKIP_FILES:
        return False
    return True


def collect_files(base: Path):
    for p in base.rglob("*"):
        if not should_upload(p.relative_to(base)):
            continue
        rel = p.relative_to(base)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if p.is_file():
            yield p, rel


def main():
    print(f"==> 连接 {USER}@{HOST}")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASSWORD, timeout=30)

    client.exec_command(f"mkdir -p {REMOTE}")
    print(f"==> 上传文件到 {REMOTE}")

    with SCPClient(client.get_transport()) as scp:
        for local_path, rel in collect_files(LOCAL):
            remote_path = f"{REMOTE}/{rel.as_posix()}"
            remote_dir = os.path.dirname(remote_path)
            client.exec_command(f"mkdir -p {remote_dir}")
            scp.put(str(local_path), remote_path)
            print(f"  + {rel}")

        # .env
        import tempfile
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".env", encoding="utf-8") as f:
            f.write(ENV_CONTENT)
            tmp = f.name
        scp.put(tmp, f"{REMOTE}/.env")
        os.unlink(tmp)
        print("  + .env")

    print("==> 远程安装并启动")
    cmd = f"""
cd {REMOTE} && \
chmod +x deploy/start-server.sh && \
bash deploy/start-server.sh && \
sleep 2 && \
curl -s http://127.0.0.1:8080/api/health || echo 'health check pending'
"""
    stdin, stdout, stderr = client.exec_command(cmd, timeout=120)
    out = stdout.read().decode("utf-8", errors="replace")
    err = stderr.read().decode("utf-8", errors="replace")
    print(out)
    if err:
        print("stderr:", err)

    # verify process
    stdin, stdout, stderr = client.exec_command("pgrep -af 'gunicorn.*server.app' || ps aux | grep gunicorn | grep -v grep")
    print("进程:", stdout.read().decode())

    client.close()
    print(f"\n==> 部署完成！访问 http://{HOST}:8080")


if __name__ == "__main__":
    main()
