---
title: Nginx 配置与多站点托管完整指南
date: 2026-08-09
---
# Nginx 配置与多站点托管完整指南

**适用环境**：Ubuntu 24.04 LTS + Nginx 1.24.0  
**目标**：在一个服务器 IP 上托管多个独立域名网站

---

## 一、Nginx 配置文件结构速览

| 路径 | 作用 | 加载方式 |
|------|------|----------|
| `/etc/nginx/nginx.conf` | 主配置文件，全局设置入口 | 自动加载 |
| `/etc/nginx/sites-available/` | **仓库**：存放所有网站的配置文件 | 手动创建，不自动加载 |
| `/etc/nginx/sites-enabled/` | **前台**：存放被启用的网站配置（软链接） | 自动加载目录下所有文件 |
| `/etc/nginx/conf.d/` | 存放通用配置片段（如 upstream、缓存设置） | 自动加载 `*.conf` |
| `/var/log/nginx/access.log` | 访问日志 | 可自定义 |
| `/var/log/nginx/error.log` | 错误日志 | 可自定义 |

### 🔑 核心概念：通过 `server_name` 区分多个域名

Nginx 不依赖 IP 区分网站，而是依赖 HTTP 请求中的 `Host` 头。同一个 IP 的 80 端口可以同时监听无数个域名，Nginx 会根据 `server_name` 指令匹配对应的 `server` 块。

```nginx
server {
    listen 80;
    server_name example.com www.example.com;  # 匹配这些域名
    # ... 该网站的专属配置
}
```

---

## 二、多站点托管实战流程

假设你要托管两个网站：`blog.example.com` 和 `shop.example.com`。

### 第一步：创建网站目录结构

为每个网站创建独立的根目录，并设置好权限：

```bash
# 创建目录
sudo mkdir -p /var/www/blog/html
sudo mkdir -p /var/www/shop/html

# 创建测试页面（确认配置生效）
echo "<h1>Blog Site</h1>" | sudo tee /var/www/blog/html/index.html
echo "<h1>Shop Site</h1>" | sudo tee /var/www/shop/html/index.html

# 将目录所有者设置为当前用户（方便后续上传文件）
sudo chown -R $USER:$USER /var/www/blog
sudo chown -R $USER:$USER /var/www/shop
```

### 第二步：创建站点配置文件

在 `/etc/nginx/sites-available/` 下为每个网站创建独立的配置文件。

#### 📄 创建 `blog.conf`

```bash
sudo vim /etc/nginx/sites-available/blog.conf
```

写入以下内容：

```nginx
server {
    listen 80;
    server_name blog.example.com www.blog.example.com;

    root /var/www/blog/html;
    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }

    # 访问日志单独存放，便于分析
    access_log /var/log/nginx/blog.access.log;
    error_log /var/log/nginx/blog.error.log;
}
```

#### 📄 创建 `shop.conf`

```bash
sudo vim /etc/nginx/sites-available/shop.conf
```

写入以下内容：

```nginx
server {
    listen 80;
    server_name shop.example.com www.shop.example.com;

    root /var/www/shop/html;
    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }

    access_log /var/log/nginx/shop.access.log;
    error_log /var/log/nginx/shop.error.log;
}
```

### 第三步：启用站点（创建软链接）

```bash
# 启用 blog
sudo ln -s /etc/nginx/sites-available/blog.conf /etc/nginx/sites-enabled/

# 启用 shop
sudo ln -s /etc/nginx/sites-available/shop.conf /etc/nginx/sites-enabled/
```

### 第四步：测试配置并重载

```bash
# 1. 检查配置文件语法（必做！）
sudo nginx -t

# 2. 如果显示 "syntax is ok"，则重载配置（零停机）
sudo systemctl reload nginx
```

### 第五步：配置 DNS 解析

在域名注册商（如阿里云、腾讯云、Namesilo）的控制台，将 `blog.example.com` 和 `shop.example.com` 的 A 记录解析到你的服务器公网 IP。

---

## 三、安全建议：配置默认拦截规则

为了防止恶意域名解析（别人把未备案的域名指向你的 IP），建议配置一个兜底的 `default_server`，拦截所有未配置的域名访问。

创建一个独立的默认配置文件：

```bash
sudo vim /etc/nginx/sites-available/default-block.conf
```

写入：

```nginx
server {
    listen 80 default_server;
    server_name _;  # 下划线匹配任意未列出的域名
    return 403;     # 直接拒绝
}
```

启用它：

```bash
sudo ln -s /etc/nginx/sites-available/default-block.conf /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

---

## 四、性能优化建议（可选）

可以在 `/etc/nginx/conf.d/performance.conf` 中统一配置全局性能参数：

```nginx
# 启用 Gzip 压缩
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

# 客户端上传限制
client_max_body_size 50M;

# 静态文件缓存
open_file_cache max=1000 inactive=20s;
open_file_cache_valid 30s;
open_file_cache_min_uses 2;
open_file_cache_errors on;
```

---

## 五、HTTPS 配置（配合 Let's Encrypt）

如果需要启用 HTTPS，可以使用 Certbot 自动申请并配置证书：

```bash
# 1. 安装 Certbot
sudo apt install certbot python3-certbot-nginx

# 2. 为指定域名自动配置 HTTPS（Certbot 会自动修改配置文件）
sudo certbot --nginx -d blog.example.com -d www.blog.example.com

# 3. 测试自动续期（证书有效期 90 天）
sudo certbot renew --dry-run
```

Certbot 会自动在原有的 `server` 块中添加 `listen 443 ssl` 和相关证书路径，并配置 HTTP 自动跳转到 HTTPS。

---

## 六、常用管理命令附录

| 操作 | 命令 |
|------|------|
| 测试配置文件语法 | `sudo nginx -t` |
| 查看当前所有生效配置 | `sudo nginx -T` |
| 重载配置（零停机） | `sudo systemctl reload nginx` |
| 完全重启 Nginx | `sudo systemctl restart nginx` |
| 查看 Nginx 运行状态 | `sudo systemctl status nginx` |
| 查看访问日志（实时） | `sudo tail -f /var/log/nginx/access.log` |
| 查看错误日志 | `sudo tail -f /var/log/nginx/error.log` |
| 启用站点（创建链接） | `sudo ln -s /etc/nginx/sites-available/xxx.conf /etc/nginx/sites-enabled/` |
| 禁用站点（删除链接） | `sudo rm /etc/nginx/sites-enabled/xxx.conf` |

---

## 七、故障排查清单

遇到问题时，按以下顺序检查：

1. **DNS 是否生效**：`dig blog.example.com` 是否返回你的 IP。
2. **防火墙是否放行**：`sudo ufw status` 确认 80/443 端口为 ALLOW。
3. **云安全组是否放行**：登录腾讯云/阿里云控制台，检查安全组规则。
4. **配置文件语法**：`sudo nginx -t` 必须通过。
5. **错误日志**：`sudo tail -30 /var/log/nginx/error.log` 查看具体报错。
6. **端口是否被占用**：`sudo netstat -tlnp | grep :80`。
7. **SELinux/AppArmor**：Ubuntu 默认开启 AppArmor，如有异常需检查其日志。

---

### 💬 后续可以帮你什么？

这份文档已经覆盖了从零开始配置多站点 Nginx 的完整流程。如果你有具体的域名需要配置，或者遇到了什么报错，随时可以把信息贴出来，我可以帮你分析解决。😊