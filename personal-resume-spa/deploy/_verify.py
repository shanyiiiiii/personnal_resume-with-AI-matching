import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("10.188.65.154", username="yang324", password="tougaobizhong324", timeout=30)

cmds = [
    "export PATH=$HOME/.local/bin:$PATH; python3 -m pip --version 2>&1",
    "pgrep -af gunicorn 2>&1; ls -la /home/yang324/hanmengdie/gunicorn.log 2>&1",
    "tail -30 /home/yang324/hanmengdie/gunicorn.log 2>&1",
    "wget -qO- http://127.0.0.1:8080/api/health 2>&1",
    "ss -tlnp | grep 8080 2>&1 || netstat -tlnp 2>/dev/null | grep 8080",
]

for cmd in cmds:
    _, o, e = c.exec_command(cmd, timeout=30)
    print("===", cmd[:60])
    print(o.read().decode("utf-8", errors="replace"))
    err = e.read().decode()
    if err:
        print("err:", err)

c.close()
