# 个人动态简历网站

现代浅色 SPA + AI 岗位匹配，**无需数据库**。

## 功能

- 五个板块：个人浏览、教育背景、技能特长、项目经历、工作经历
- 首页 AI 岗位匹配器：粘贴 JD，智谱 AI 对照全站简历内容生成匹配报告
- 统一部署服务：静态页面 + `/api/match` 接口

## 本地运行

```powershell
cd C:\Users\15452\personal-resume-spa

# 1. 配置 API Key（复制并编辑）
copy .env.example .env

# 2. 安装依赖并启动（监听 0.0.0.0，局域网可访问）
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
.\.venv\Scripts\python server\app.py
```

浏览器访问：**http://localhost:8080**

同一 WiFi 下的手机可访问：`http://你的电脑IP:8080`

> 不要用 `python -m http.server` 或双击打开 HTML，否则 ES Module 和 AI 接口无法工作。

## 部署到 3080 服务器（无数据库）

### 方式 A：Docker（推荐）

```bash
# 上传项目到服务器后
cp .env.example .env   # 填入 ZHIPU_API_KEY
docker compose up -d --build
```

访问 `http://服务器公网IP:8080`，并在云厂商安全组放行 **8080** 端口。

### 方式 B：脚本 + systemd

```bash
chmod +x deploy/deploy.sh
./deploy/deploy.sh
```

## 修改简历内容

| 文件 | 用途 |
|------|------|
| `js/data.js` | 前端展示 |
| `server/resume.json` | AI 匹配读取（需与 data.js 保持同步） |
| `assets/profile.png` | 首页头像 |

## 环境变量

| 变量 | 说明 |
|------|------|
| `ZHIPU_API_KEY` | 智谱 AI API Key（仅服务端，勿写进前端） |
| `ZHIPU_MODEL` | 默认 `glm-4-flash` |
| `PORT` | 默认 `8080` |

## 架构说明

```
浏览器 → Flask (server/app.py)
           ├── 静态文件 (HTML/CSS/JS/图片)
           └── POST /api/match → 智谱 AI → 返回 JSON 匹配报告
```

简历数据存在 `server/resume.json` 文件中，**不需要 MySQL / Redis 等数据库**。
