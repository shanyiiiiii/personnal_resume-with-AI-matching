import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("10.188.65.154", username="yang324", password="tougaobizhong324", timeout=30)

script = """
export PATH="$HOME/.local/bin:$PATH"
cd /home/yang324/hanmengdie
timeout 4 gunicorn -b 0.0.0.0:8080 -w 1 server.app:app 2>&1 || true
"""

_, o, e = c.exec_command(script, timeout=30)
print(o.read().decode("utf-8", errors="replace"))
print(e.read().decode("utf-8", errors="replace"))
c.close()
