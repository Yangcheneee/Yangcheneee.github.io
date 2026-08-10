---
title: 使用 rsync 实现服务器版本控制
date: 2026-08-09
---
# 使用 rsync 实现服务器版本控制

> 并非所有同步场景都需要版本控制。例如，将前端构建产物同步到 CDN 源站、更新配置文件、备份日志文件，或快速部署静态网站时，我们更看重传输速度和简单性。此时，rsync 等文件级同步工具成为不二之选。本文将重点介绍 rsync 的使用方法，并延伸至实时同步方案。

## rsync 核心优势

- **增量传输**：只传送源端和目标端不同的文件块，节省带宽和时间。
- **灵活选项**：支持排除、保留权限、压缩、断点续传等。
- **安全加密**：可通过 SSH 通道传输，保证数据安全。
- **跨平台**：Linux/macOS/Windows（WSL/Cygwin）均可使用。

## 安装 rsync

绝大多数 Linux 发行版已预装，若未安装：

```bash
# Debian/Ubuntu
sudo apt install rsync

# RHEL/CentOS
sudo yum install rsync
```

Windows 用户可使用 WSL 或安装 MSYS2 环境。

## 基本语法与常用选项

```bash
rsync [选项] 源路径 目标路径
```

| 选项        | 说明                                                    |
| ----------- | ------------------------------------------------------- |
| `-a`        | 归档模式（保留权限、时间戳、递归等）                    |
| `-v`        | 详细输出（verbose）                                     |
| `-z`        | 传输时压缩（节省带宽）                                  |
| `-P`        | 显示进度并支持断点续传（等价于 `--partial --progress`） |
| `--delete`  | 删除目标端中源端没有的文件（**谨慎使用**）              |
| `--exclude` | 排除特定文件或目录，可多次使用                          |
| `-n`        | 试运行（dry-run），查看将要执行的操作，无实际改动       |

## 典型同步场景示例

### 1. 从本地推送到服务器（部署）

```bash
# 将本地 /build/ 目录同步到服务器 /var/www/html/
rsync -avzP /build/ user@remote-server:/var/www/html/
```

**注意**：路径末尾的斜杠 ` /` 表示同步目录**内容**，而不创建目录本身；若不加斜杠，则会将源目录整体复制到目标下。

### 2. 从服务器拉取到本地（备份）

```bash
rsync -avzP user@remote-server:/var/log/ /local/backup/logs/
```

### 3. 排除不需要同步的目录

```bash
rsync -avzP --exclude='node_modules' --exclude='*.tmp' /src/ user@server:/dest/
```

### 4. 清理目标端多余文件（慎用）

```bash
rsync -avzP --delete /local/ user@server:/remote/
```

建议先用 `-n` 模拟：

```bash
rsync -avzP --delete -n /local/ user@server:/remote/
```

## 安全优化：配置 SSH 免密登录

若频繁同步，使用密码既繁琐又不安全。生成 SSH 密钥对并复制公钥到服务器：

```bash
# 本地生成密钥（若已有则跳过）
ssh-keygen -t ed25519

# 复制公钥到服务器
ssh-copy-id user@remote-server
```

此后 rsync 使用 `-e ssh` 自动利用 SSH 通道，无需再次输入密码。
