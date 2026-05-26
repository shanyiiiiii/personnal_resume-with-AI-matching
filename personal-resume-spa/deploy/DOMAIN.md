# 域名 hmdresume.xyz 配置说明

## 关于 ns1.volcengine-dns.com / ns2.volcengine-dns.com

这是**火山引擎（字节）DNS 的域名服务器地址（NS）**，不是网站 IP。

| 类型 | 作用 |
|------|------|
| **NS（域名服务器）** | 告诉全世界：这个域名的 DNS 记录由火山引擎解析 |
| **A 记录** | 把 `hmdresume.xyz` 指向你服务器的 **公网 IP** |

### 两种常见配置方式

**方式 A：域名在火山引擎 DNS 解析（推荐）**

1. 在域名注册商处，把域名的 NS 改为：
   - `ns1.volcengine-dns.com`
   - `ns2.volcengine-dns.com`
2. 登录 [火山引擎 DNS 控制台](https://console.volcengine.com/) → 找到 `hmdresume.xyz` → 添加 **A 记录**：

| 主机记录 | 记录类型 | 记录值 |
|----------|----------|--------|
| `@` | A | 服务器公网 IP |
| `www` | A | 同上 |

**方式 B：NS 仍在注册商（如 Namecheap）**

- 不必改 NS，直接在注册商 DNS 里添加上述 **A 记录** 即可。

> 仅填写 NS 而不添加 A 记录，域名无法打开网站。

## 在服务器安装 Nginx 反代

```bash
ssh your_server_ip
sudo apt install -y nginx
cd your_project_dir
chmod +x deploy/setup-domain.sh
sudo bash deploy/setup-domain.sh
```

## 3. 放行防火墙端口

```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp   # 若后续配置 HTTPS
```

## 4. 验证

DNS 生效后（通常 10 分钟～48 小时）访问：

- http://hmdresume.xyz
- http://www.hmdresume.xyz

## 5. HTTPS（可选）

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d hmdresume.xyz -d www.hmdresume.xyz
```
