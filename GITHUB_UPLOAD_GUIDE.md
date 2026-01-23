# GitHub 上传指南

由于服务器网络限制，无法直接推送到 GitHub。请按照以下步骤操作：

## 方法1：在本地电脑推送（推荐）

### 步骤1：将代码下载到本地

你可以通过以下方式获取代码：
- 使用 `scp` 或 `rsync` 从服务器下载
- 或者直接在服务器上打包下载

### 步骤2：在本地配置 Git

```bash
# 进入项目目录
cd /path/to/My_Patient_Agent

# 配置 Git 用户信息（如果还没配置）
git config user.name "wen-jun-Z"
git config user.email "zhuwen1220@gmail.com"

# 检查远程仓库
git remote -v
# 应该显示：origin  https://github.com/wen-jun-Z/Patient_Agent.git
```

### 步骤3：推送到 GitHub

```bash
# 使用 HTTPS 方式推送
git push -u origin main
```

提示输入时：
- **Username**: `wen-jun-Z`
- **Password**: `YOUR_PERSONAL_ACCESS_TOKEN`（请使用你自己的 token）

---

## 方法2：使用 SSH 方式

### 步骤1：添加 SSH Key 到 GitHub

1. 访问：https://github.com/settings/keys
2. 点击 "New SSH key"
3. Title: `autodl-server`
4. Key: 粘贴以下公钥：
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIITYV/x5EtJCwXtYsc3ep66EgDsteBegAbYFmDPCYTdq zhuwen1220@gmail.com
```
5. 点击 "Add SSH key"

### 步骤2：修改远程仓库为 SSH

```bash
cd /path/to/My_Patient_Agent
git remote set-url origin git@github.com:wen-jun-Z/Patient_Agent.git
git push -u origin main
```

---

## 方法3：手动上传（如果 Git 不可用）

如果以上方法都不行，可以：

1. 在 GitHub 上创建仓库：https://github.com/new
   - Repository name: `Patient_Agent`
   - 选择 Public 或 Private
   - **不要**勾选 "Initialize with README"

2. 在服务器上打包代码：
```bash
cd /root/autodl-tmp
tar -czf Patient_Agent.tar.gz My_Patient_Agent/
```

3. 下载压缩包到本地，解压后手动上传到 GitHub（使用网页界面）

---

## 当前仓库状态

- ✅ Git 仓库已初始化
- ✅ 代码已提交（2 个 commit）
- ✅ 远程仓库已配置
- ✅ 分支已重命名为 `main`
- ❌ 网络连接 GitHub 超时（需要在外网环境推送）

---

## 快速命令（在能访问 GitHub 的地方运行）

```bash
cd /path/to/My_Patient_Agent
git remote set-url origin https://github.com/wen-jun-Z/Patient_Agent.git
git push -u origin main
# 输入用户名：wen-jun-Z
# 输入密码/token：YOUR_PERSONAL_ACCESS_TOKEN（请使用你自己的 token）
```
