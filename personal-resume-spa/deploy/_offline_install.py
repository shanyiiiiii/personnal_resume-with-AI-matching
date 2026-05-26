import os
import tempfile
import urllib.request
from pathlib import Path

import paramiko
from scp import SCPClient

HOST, USER, PW = "10.188.65.154", "yang324", "tougaobizhong324"
REMOTE = "/home/yang324/hanmengdie"
WHEELS = Path(r"C:\Users\15452\personal-resume-spa\deploy\wheels")

with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp:
    get_pip_path = tmp.name
urllib.request.urlretrieve("https://bootstrap.pypa.io/get-pip.py", get_pip_path)

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect(HOST, username=USER, password=PW, timeout=30)

print("==> 上传 wheels")
c.exec_command(f"mkdir -p {REMOTE}/wheels")
with SCPClient(c.get_transport()) as scp:
    scp.put(get_pip_path, f"{REMOTE}/get-pip.py")
    for whl in WHEELS.glob("*.whl"):
        scp.put(str(whl), f"{REMOTE}/wheels/{whl.name}")
        print(f"  + {whl.name}")
os.unlink(get_pip_path)

script = f"""
set -e
cd {REMOTE}

python3 get-pip.py --user --break-system-packages --no-index --find-links=wheels 2>&1 | tail -8

export PATH="$HOME/.local/bin:$PATH"
python3 -m pip install --user --break-system-packages --no-index --find-links=wheels flask python-dotenv requests gunicorn 2>&1 | tail -8

pkill -f 'gunicorn.*server.app:app' 2>/dev/null || true
sleep 1
nohup $HOME/.local/bin/gunicorn -b 0.0.0.0:8080 -w 2 server.app:app > gunicorn.log 2>&1 &
sleep 5
wget -qO- http://127.0.0.1:8080/api/health
echo
pgrep -af 'gunicorn.*server.app' || (echo '--- log ---'; tail -50 gunicorn.log)
"""

print("==> 离线安装并启动")
_, o, e = c.exec_command(script, timeout=180)
print(o.read().decode("utf-8", errors="replace"))
err = e.read().decode("utf-8", errors="replace")
if err:
    print("ERR:", err)
c.close()
print(f"\n==> 访问 http://{HOST}:8080")
