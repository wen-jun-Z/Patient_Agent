#!/bin/bash
# 推送代码到 GitHub 的脚本

cd /root/autodl-tmp/My_Patient_Agent

# 使用 HTTPS 方式（需要 token）
git remote set-url origin https://github.com/wen-jun-Z/Patient_Agent.git

# 推送代码（会提示输入用户名和 token）
echo "正在推送到 GitHub..."
echo "用户名: wen-jun-Z"
echo "密码/Token: 请手动输入你的 Personal Access Token"
git push -u origin main
