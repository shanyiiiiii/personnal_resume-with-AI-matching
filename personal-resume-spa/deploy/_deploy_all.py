import paramiko
from pathlib import Path

L = Path(r"C:\Users\15452\personal-resume-spa")
files = [
    "js/data.js",
    "js/app.js",
    "css/styles.css",
    "index.html",
    "assets/wechat-qr.png",
    "deploy/nginx-hmdresume.conf",
    "deploy/setup-domain.sh",
    "deploy/DOMAIN.md",
]

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("10.188.65.154", username="yang324", password="tougaobizhong324", timeout=15)
sftp = c.open_sftp()

for f in files:
    remote = f"/home/yang324/hanmengdie/{f.replace(chr(92), '/')}"
    sftp.put(str(L / f), remote)
    print("ok", f)

sftp.close()
c.exec_command("systemctl --user restart resume-site")

_, o, _ = c.exec_command("curl -s --max-time 5 ifconfig.me; echo")
print("公网 IP:", o.read().decode().strip())

_, o, _ = c.exec_command("which nginx; ss -tlnp 2>/dev/null | grep 8080")
print(o.read().decode())

c.close()
