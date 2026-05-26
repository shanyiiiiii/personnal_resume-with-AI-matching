import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("10.188.65.154", username="yang324", password="tougaobizhong324", timeout=30)

script = """
set -e
cd /home/yang324/hanmengdie
export PATH="$HOME/.local/bin:$PATH"

pip install --user --break-system-packages --no-index --find-links=wheels requests jinja2 click certifi idna urllib3 charset-normalizer markupsafe 2>&1 | tail -5

python3 -c "import flask, gunicorn, requests; print('imports ok')" 2>&1

pkill -f 'gunicorn.*server.app:app' 2>/dev/null || true
sleep 1

cd /home/yang324/hanmengdie
nohup $HOME/.local/bin/gunicorn -b 0.0.0.0:8080 -w 2 server.app:app > gunicorn.log 2>&1 &
sleep 4
cat gunicorn.log
echo '---'
wget -qO- http://127.0.0.1:8080/api/health
echo
pgrep -af gunicorn
"""

_, o, e = c.exec_command(script, timeout=60)
print(o.read().decode("utf-8", errors="replace"))
err = e.read().decode("utf-8", errors="replace")
if err:
    print("ERR:", err)
c.close()
