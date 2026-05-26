import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("10.188.65.154", username="yang324", password="tougaobizhong324", timeout=30)

service = """[Unit]
Description=Personal Resume SPA
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/yang324/hanmengdie
EnvironmentFile=/home/yang324/hanmengdie/.env
Environment=PATH=/home/yang324/.local/bin:/usr/bin
ExecStart=/home/yang324/.local/bin/gunicorn -b 0.0.0.0:8080 -w 2 server.app:app
Restart=always
RestartSec=3

[Install]
WantedBy=default.target
"""

script = f"""
mkdir -p ~/.config/systemd/user
cat > ~/.config/systemd/user/resume-site.service << 'EOF'
{service}
EOF
systemctl --user daemon-reload
systemctl --user enable resume-site
systemctl --user restart resume-site
sleep 3
systemctl --user status resume-site --no-pager | head -12
wget -qO- http://127.0.0.1:8080/api/health
echo
ss -tlnp | grep 8080
"""

_, o, e = c.exec_command(script, timeout=60)
print(o.read().decode("utf-8", errors="replace"))
err = e.read().decode("utf-8", errors="replace")
if err:
    print("ERR:", err)
c.close()
