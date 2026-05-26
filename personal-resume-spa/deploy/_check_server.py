import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("10.188.65.154", username="yang324", password="tougaobizhong324", timeout=30)

cmds = [
    "which python3 python pip3 pip docker 2>/dev/null; python3 --version; pip3 --version 2>/dev/null || true",
    "ls -la /home/yang324/hanmengdie",
    "python3 -m pip --version 2>&1 || true",
    "docker --version 2>&1 || true",
    "id; uname -a",
]

for cmd in cmds:
    _, o, e = c.exec_command(cmd)
    print("===", cmd)
    print(o.read().decode())
    err = e.read().decode()
    if err:
        print("err:", err)

c.close()
