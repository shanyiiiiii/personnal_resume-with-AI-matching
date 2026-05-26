import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("10.188.65.154", username="yang324", password="tougaobizhong324", timeout=30)

script = """
set -e
cd /home/yang324/hanmengdie
export PATH="$HOME/.local/bin:$PATH"

rm -rf /tmp/pipex
python3 -m zipfile -e wheels/pip-26.1.1-py3-none-any.whl /tmp/pipex

python3 /tmp/pipex/pip install --user --break-system-packages --no-index --find-links=wheels --ignore-installed pip setuptools wheel 2>&1 | tail -8

which pip
pip --version

pip install --user --break-system-packages --no-index --find-links=wheels flask python-dotenv requests gunicorn 2>&1 | tail -5

pkill -f 'gunicorn.*server.app:app' 2>/dev/null || true
sleep 1
nohup $HOME/.local/bin/gunicorn -b 0.0.0.0:8080 -w 2 server.app:app > gunicorn.log 2>&1 &
sleep 5
wget -qO- http://127.0.0.1:8080/api/health
echo
pgrep -af 'gunicorn.*server.app' || (echo '--- log ---'; tail -50 gunicorn.log)
"""

_, o, e = c.exec_command(script, timeout=120)
print(o.read().decode("utf-8", errors="replace"))
print(e.read().decode("utf-8", errors="replace"))
c.close()
