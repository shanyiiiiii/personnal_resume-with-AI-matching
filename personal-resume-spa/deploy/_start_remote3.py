import paramiko

HOST, USER, PW = "10.188.65.154", "yang324", "tougaobizhong324"
REMOTE = "/home/yang324/hanmengdie"

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect(HOST, username=USER, password=PW, timeout=30)

script = f"""
set -e
cd {REMOTE}

if ! python3 -m pip --version 2>/dev/null; then
  wget -q -O /tmp/get-pip.py https://bootstrap.pypa.io/get-pip.py
  python3 /tmp/get-pip.py --user --break-system-packages 2>&1 | tail -5
fi

export PATH="$HOME/.local/bin:$PATH"
python3 -m pip install --user --break-system-packages -r requirements.txt 2>&1 | tail -8

pkill -f 'gunicorn.*server.app:app' 2>/dev/null || true
sleep 1

nohup $HOME/.local/bin/gunicorn -b 0.0.0.0:8080 -w 2 server.app:app > gunicorn.log 2>&1 &
sleep 5
curl -s http://127.0.0.1:8080/api/health 2>/dev/null || wget -qO- http://127.0.0.1:8080/api/health
echo
pgrep -af gunicorn || (echo '--- log ---'; tail -40 gunicorn.log)
"""

_, o, e = c.exec_command(script, timeout=300)
print(o.read().decode("utf-8", errors="replace"))
err = e.read().decode("utf-8", errors="replace")
if err:
    print("ERR:", err)
c.close()
