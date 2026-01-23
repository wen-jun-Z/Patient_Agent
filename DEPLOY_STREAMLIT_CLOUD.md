# Streamlit Cloud 部署指南

## 📋 部署前准备

### 1. 确保代码已推送到 GitHub

```bash
# 检查 Git 状态
git status

# 如果还没有提交，先提交所有更改
git add .
git commit -m "准备部署到 Streamlit Cloud"

# 推送到 GitHub
git push origin main
```

### 2. 重要：API 密钥安全

⚠️ **不要将 API 密钥硬编码在代码中！**

- ✅ `run.sh` 已添加到 `.gitignore`，不会被提交
- ✅ API 密钥将通过 Streamlit Cloud 的 Secrets 功能配置

---

## 🚀 部署步骤

### 步骤 1：登录 Streamlit Cloud

1. 访问 [Streamlit Cloud](https://share.streamlit.io/)
2. 使用 GitHub 账号登录
3. 点击 "New app"

### 步骤 2：配置应用

**Repository（仓库）**：
- 选择你的 GitHub 仓库：`你的用户名/My_Patient_Agent`

**Branch（分支）**：
- 选择 `main` 或 `master`

**Main file path（主文件路径）**：
- 输入：`streamlit_app.py`

**App URL（应用 URL）**：
- 可以自定义，例如：`patient-simulation-demo`

### 步骤 3：配置 Secrets（API 密钥）

在部署前，点击 "Advanced settings" → "Secrets"，添加以下环境变量：

```toml
QWEN_API_KEY = "sk-fclzckobrlffwetgkylgbbrnmlmvmdlvwtnbszleujiyuzkx"
DEEPSEEK_API_KEY = "sk-f586f2a14d8b4bc7b07b23ee6529872c"
```

或者使用 TOML 格式：

```toml
[secrets]
QWEN_API_KEY = "sk-fclzckobrlffwetgkylgbbrnmlmvmdlvwtnbszleujiyuzkx"
DEEPSEEK_API_KEY = "sk-f586f2a14d8b4bc7b23ee6529872c"
```

### 步骤 4：部署

点击 "Deploy!" 按钮，等待部署完成。

---

## 📁 项目结构要求

Streamlit Cloud 需要以下文件：

```
My_Patient_Agent/
├── streamlit_app.py      # ✅ 已创建 - Streamlit Cloud 入口文件
├── requirements.txt      # ✅ 已创建 - Python 依赖
├── .streamlit/
│   └── config.toml      # ✅ 已创建 - Streamlit 配置
├── demo/
│   ├── demo.py          # 主应用文件
│   ├── config.json      # 配置文件
│   └── demo_data.json   # 患者数据
└── src/                 # 源代码目录
```

---

## 🔧 故障排除

### 问题 1：导入错误

如果出现 `ModuleNotFoundError`，检查：
- `requirements.txt` 是否包含所有依赖
- `streamlit_app.py` 的路径是否正确

### 问题 2：API 密钥错误

如果患者不回答，检查：
- Streamlit Cloud Secrets 中是否设置了 `QWEN_API_KEY` 和 `DEEPSEEK_API_KEY`
- 密钥是否正确（没有多余的空格）

### 问题 3：文件路径错误

如果出现文件找不到错误：
- 确保所有数据文件都在仓库中
- 检查 `demo/config.json` 中的路径是否为相对路径

---

## 🔒 安全建议

1. **永远不要**将 API 密钥提交到 Git
2. **使用** Streamlit Cloud Secrets 管理敏感信息
3. **定期**轮换 API 密钥
4. **检查** `.gitignore` 确保敏感文件被忽略

---

## 📝 部署后检查清单

- [ ] 应用可以正常访问
- [ ] 可以选择患者
- [ ] 患者可以正常回答（测试中文和英文）
- [ ] API 调用正常（检查 Streamlit Cloud 日志）
- [ ] 没有控制台错误

---

## 🎉 完成！

部署成功后，你会得到一个类似这样的 URL：
```
https://你的应用名.streamlit.app
```

可以分享给其他人使用！
