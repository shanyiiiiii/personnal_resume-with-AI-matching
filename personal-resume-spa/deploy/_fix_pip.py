import paramiko

HOST, USER, PW = "10.188.65.154", "yang324", "tougaobizhong324"
REMOTE = "/home/yang324/hanmengdie"

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect(HOST, username=USER, password=PW, timeout=30)

script = f"""
set -e
cd {REMOTE}
export PATH="$HOME/.local/bin:$PATH"

rm -rf /tmp/pipex
python3 -m zipfile -e wheels/pip-26.1.1-py3-none-any.whl /tmp/pipex

# 用解压出的 pip 模块安装 pip 到用户目录
python3 /tmp/pipex/pip install --user --break-system-packages --no-index --find-links=wheels pip 2>&1

$HOME/.local/bin/pip install --user --break-system-packages --no-index --find-links=wheels flask python-dotenv requests gunicorn 2>&1 | tail -5

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
err = e.read().decode("utf-8", errors="replace")
if err:
    print("ERR:", err)
c.close()
