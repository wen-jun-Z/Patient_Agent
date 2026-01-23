# 🚀 Streamlit Cloud 部署检查清单

## ✅ 部署前检查

### 1. 代码准备
- [x] 创建 `requirements.txt` - Python 依赖列表
- [x] 创建 `streamlit_app.py` - Streamlit Cloud 入口文件
- [x] 创建 `.streamlit/config.toml` - Streamlit 配置
- [x] 更新 `.gitignore` - 确保敏感文件不被提交

### 2. 安全性检查
- [x] `run.sh` 已添加到 `.gitignore`（包含硬编码的 API 密钥）
- [x] 确保没有 API 密钥硬编码在代码中
- [x] 所有敏感信息将通过 Streamlit Cloud Secrets 配置

### 3. 文件完整性
- [x] `demo/demo.py` - 主应用文件
- [x] `demo/config.json` - 配置文件
- [x] `demo/demo_data.json` - 患者数据
- [x] `src/` - 源代码目录完整
- [x] `src/prompts/` - Prompt 文件完整

### 4. 测试
- [ ] 本地测试 `streamlit_app.py` 是否能正常运行
- [ ] 确认所有依赖都在 `requirements.txt` 中

---

## 📤 推送到 GitHub

### 步骤 1：检查 Git 状态

```bash
cd /root/autodl-tmp/My_Patient_Agent
git status
```

### 步骤 2：添加新文件

```bash
# 添加新创建的文件
git add requirements.txt
git add streamlit_app.py
git add .streamlit/config.toml
git add DEPLOY_STREAMLIT_CLOUD.md
git add DEPLOY_CHECKLIST.md

# 添加其他更改
git add .
```

### 步骤 3：提交更改

```bash
git commit -m "准备部署到 Streamlit Cloud

- 添加 requirements.txt
- 添加 streamlit_app.py 作为入口文件
- 添加 Streamlit 配置文件
- 更新 .gitignore 保护敏感信息
- 添加部署文档"
```

### 步骤 4：推送到 GitHub

```bash
git push origin main
```

---

## 🌐 部署到 Streamlit Cloud

### 步骤 1：访问 Streamlit Cloud
1. 打开 https://share.streamlit.io/
2. 使用 GitHub 账号登录

### 步骤 2：创建新应用
1. 点击 "New app"
2. 选择你的仓库：`你的用户名/My_Patient_Agent`
3. 选择分支：`main`
4. Main file path：`streamlit_app.py`

### 步骤 3：配置 Secrets
在 "Advanced settings" → "Secrets" 中添加：

```toml
QWEN_API_KEY = "sk-fclzckobrlffwetgkylgbbrnmlmvmdlvwtnbszleujiyuzkx"
DEEPSEEK_API_KEY = "sk-f586f2a14d8b4bc7b07b23ee6529872c"
```

### 步骤 4：部署
点击 "Deploy!" 并等待部署完成

---

## 🧪 部署后测试

- [ ] 应用可以正常访问
- [ ] 页面加载正常
- [ ] 可以选择患者
- [ ] 患者可以正常回答（测试中文）
- [ ] 患者可以正常回答（测试英文）
- [ ] 没有控制台错误
- [ ] API 调用正常（检查日志）

---

## 📝 注意事项

1. **API 密钥**：确保在 Streamlit Cloud Secrets 中正确配置
2. **文件路径**：所有路径都应该是相对路径
3. **依赖版本**：如果部署失败，检查 `requirements.txt` 中的版本
4. **日志**：部署后检查 Streamlit Cloud 的日志以排查问题

---

## 🆘 遇到问题？

1. 查看 Streamlit Cloud 的日志
2. 检查 `requirements.txt` 是否包含所有依赖
3. 确认 API 密钥在 Secrets 中正确配置
4. 参考 `DEPLOY_STREAMLIT_CLOUD.md` 中的故障排除部分
