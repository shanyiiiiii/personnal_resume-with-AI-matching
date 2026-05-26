import paramiko
import time

HOST, USER, PW = "10.188.65.154", "yang324", "tougaobizhong324"
REMOTE = "/home/yang324/hanmengdie"

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect(HOST, username=USER, password=PW, timeout=30)

script = f"""
set -e
echo '{PW}' | sudo -S apt-get update -qq 2>/dev/null || true
echo '{PW}' | sudo -S apt-get install -y python3-pip python3-venv 2>&1 | tail -5

cd {REMOTE}
rm -rf .venv
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt -q
pkill -f 'gunicorn.*server.app:app' 2>/dev/null || true
sleep 1
nohup .venv/bin/gunicorn -b 0.0.0.0:8080 -w 2 server.app:app > gunicorn.log 2>&1 &
sleep 4
curl -s http://127.0.0.1:8080/api/health
echo
pgrep -af gunicorn || (echo '--- log ---'; tail -30 gunicorn.log)
"""

_, o, e = c.exec_command(script, timeout=300)
print(o.read().decode("utf-8", errors="replace"))
err = e.read().decode("utf-8", errors="replace")
if err:
    print("ERR:", err)
c.close()
