import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("10.188.65.154", username="yang324", password="tougaobizhong324", timeout=30)

cmds = [
    "ls -la /home/yang324/hanmengdie/env/bin/ 2>/dev/null | head -20",
    "/home/yang324/hanmengdie/env/bin/pip --version 2>&1 || true",
    "/home/yang324/hanmengdie/env/bin/python3 -c 'import flask; print(flask.__version__)' 2>&1 || true",
    "ls -la /home/yang324/hanmengdie/.venv/bin/ 2>/dev/null | head -10",
]

for cmd in cmds:
    _, o, e = c.exec_command(cmd)
    print("===", cmd)
    print(o.read().decode())
    err = e.read().decode()
    if err:
        print("err:", err)

c.close()
