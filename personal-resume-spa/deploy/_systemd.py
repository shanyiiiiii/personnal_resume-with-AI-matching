import paramiko

PW = "tougaobizhong324"

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("10.188.65.154", username="yang324", password=PW, timeout=30)

service = """[Unit]
Description=Personal Resume SPA
After=network.target

[Service]
Type=simple
User=yang324
WorkingDirectory=/home/yang324/hanmengdie
EnvironmentFile=/home/yang324/hanmengdie/.env
Environment=PATH=/home/yang324/.local/bin:/usr/bin
ExecStart=/home/yang324/.local/bin/gunicorn -b 0.0.0.0:8080 -w 2 server.app:app
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
"""

# 写入 service 文件
cmd = f"""
echo '{PW}' | sudo -S tee /etc/systemd/system/resume-site.service > /dev/null << 'EOF'
{service}
EOF
echo '{PW}' | sudo -S systemctl daemon-reload
echo '{PW}' | sudo -S systemctl enable resume-site
echo '{PW}' | sudo -S systemctl restart resume-site
sleep 3
echo '{PW}' | sudo -S systemctl status resume-site --no-pager | head -15
wget -qO- http://127.0.0.1:8080/api/health
echo
"""

_, o, e = c.exec_command(cmd, timeout=60)
print(o.read().decode("utf-8", errors="replace"))
err = e.read().decode("utf-8", errors="replace")
if err:
    print("ERR:", err)
c.close()
print("\n==> http://10.188.65.154:8080")
