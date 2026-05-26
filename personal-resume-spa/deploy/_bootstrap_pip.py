import os
from pathlib import Path

import paramiko

HOST, USER, PW = "10.188.65.154", "yang324", "tougaobizhong324"
REMOTE = "/home/yang324/hanmengdie"
WHEELS = Path(r"C:\Users\15452\personal-resume-spa\deploy\wheels")

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect(HOST, username=USER, password=PW, timeout=30)

sftp = c.open_sftp()
try:
    try:
        sftp.mkdir(f"{REMOTE}/wheels")
    except OSError:
        pass

    print("==> 上传 wheels")
    for whl in WHEELS.glob("*.whl"):
        remote = f"{REMOTE}/wheels/{whl.name}"
        print(f"  + {whl.name}")
        sftp.put(str(whl), remote)
finally:
    sftp.close()

script = f"""
set -e
cd {REMOTE}
export PATH="$HOME/.local/bin:$PATH"

# 从 pip wheel 引导安装（无需 get-pip / apt）
rm -rf /tmp/pipex
python3 -m zipfile -e wheels/pip-26.1.1-py3-none-any.whl /tmp/pipex
python3 /tmp/pipex/pip install --user --break-system-packages --no-index --find-links=wheels pip setuptools wheel 2>&1 | tail -5
python3 -m pip install --user --break-system-packages --no-index --find-links=wheels flask python-dotenv requests gunicorn 2>&1 | tail -5

pkill -f 'gunicorn.*server.app:app' 2>/dev/null || true
sleep 1
nohup $HOME/.local/bin/gunicorn -b 0.0.0.0:8080 -w 2 server.app:app > gunicorn.log 2>&1 &
sleep 5
wget -qO- http://127.0.0.1:8080/api/health
echo
pgrep -af 'gunicorn.*server.app' || (echo '--- log ---'; tail -50 gunicorn.log)
"""

print("==> 离线安装并启动")
_, o, e = c.exec_command(script, timeout=120)
print(o.read().decode("utf-8", errors="replace"))
err = e.read().decode("utf-8", errors="replace")
if err:
    print("ERR:", err)
c.close()
print(f"\n==> 访问 http://{HOST}:8080")
