@echo off
REM 在本机 Windows 执行：将项目上传到服务器
REM 需已配置 SSH 密钥，或执行时会提示输入 your-server-name 的密码

set SERVER=your-server-name@your-server-ip
set REMOTE=your_app_directory  REM 替换为服务器上的应用目录路径
set LOCAL=C:\Users\15452\personal-resume-spa

echo === 创建远程目录 ===
ssh %SERVER% "mkdir -p %REMOTE%"

echo === 上传项目文件（排除 .venv 和 .git）===
scp -r "%LOCAL%\index.html" "%LOCAL%\css" "%LOCAL%\js" "%LOCAL%\assets" "%LOCAL%\server" "%LOCAL%\requirements.txt" "%LOCAL%\Dockerfile" "%LOCAL%\docker-compose.yml" "%LOCAL%\.env.example" "%LOCAL%\deploy" %SERVER%:%REMOTE%/

echo === 上传 .env（API Key）===
scp "%LOCAL%\.env" %SERVER%:%REMOTE%/.env

echo === 远程启动服务 ===
ssh %SERVER% "chmod +x %REMOTE%/deploy/start-server.sh && bash %REMOTE%/deploy/start-server.sh"

echo.
echo 完成！浏览器访问 http://your-server-ip:8080
pause
