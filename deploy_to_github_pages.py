#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI模型数据报告部署到GitHub Pages的Python脚本
此脚本将帮助您将生成的静态网站部署到GitHub Pages
"""

import os
import subprocess
import sys
import webbrowser
from datetime import datetime


def run_command(command, cwd=None):
    """运行命令并返回结果"""
    print(f"正在执行: {' '.join(command)}")
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            shell=True if os.name == 'nt' else False
        )
        if result.returncode != 0:
            print(f"命令执行失败: {result.stderr}")
            return False, result.stderr
        return True, result.stdout
    except Exception as e:
        print(f"执行命令时出错: {str(e)}")
        return False, str(e)


def check_git_installed():
    """检查Git是否安装"""
    print("检查Git是否安装...")
    success, _ = run_command(["git", "--version"])
    if not success:
        print("错误: 未找到Git。请先安装Git再运行此脚本。")
        print("您可以从 https://git-scm.com/download/win 下载Git。")
        input("按Enter键退出...")
        sys.exit(1)
    print("Git已安装")


def check_static_site_dir(static_site_dir):
    """检查静态网站目录是否存在"""
    print(f"检查静态网站目录: {static_site_dir}")
    if not os.path.exists(static_site_dir):
        print("错误: 静态网站目录不存在。请先运行generate_static_site.py生成网站。")
        input("按Enter键退出...")
        sys.exit(1)
    print("静态网站目录存在")


def initialize_git_repo(static_site_dir):
    """初始化Git仓库（如果不存在）"""
    git_dir = os.path.join(static_site_dir, ".git")
    if not os.path.exists(git_dir):
        print("初始化Git仓库...")
        success, _ = run_command(["git", "init"], cwd=static_site_dir)
        if not success:
            print("初始化Git仓库失败")
            return False
        
        # 设置Git用户名和邮箱
        print("设置Git用户名和邮箱...")
        git_username = input("请输入您的GitHub用户名: ")
        git_email = input("请输入您的GitHub邮箱: ")
        
        run_command(["git", "config", "user.name", git_username], cwd=static_site_dir)
        run_command(["git", "config", "user.email", git_email], cwd=static_site_dir)
        
        # 添加远程仓库
        print("添加远程仓库...")
        repo_url = input("请输入您的GitHub仓库URL (例如: https://github.com/username/repository.git): ")
        success, output = run_command(["git", "remote", "add", "origin", repo_url], cwd=static_site_dir)
        if not success:
            print(f"添加远程仓库失败: {output}")
            return False
    else:
        print("Git仓库已存在")
    return True


def deploy_to_github(static_site_dir):
    """
    将文件部署到GitHub
    """
    # 添加所有文件
    print("添加文件...")
    success, _ = run_command(["git", "add", "."], cwd=static_site_dir)
    if not success:
        return False
    
    # 检查是否有更改需要提交
    print("检查是否有更改需要提交...")
    success, status_output = run_command(["git", "status"], cwd=static_site_dir)
    if "nothing to commit, working tree clean" in status_output:
        print("没有需要提交的更改，跳过commit步骤")
    else:
        # 提交更改
        print("提交更改...")
        commit_message = f"更新AI模型数据报告 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        success, output = run_command(["git", "commit", "-m", commit_message], cwd=static_site_dir)
        if not success:
            print(f"git commit 失败，错误信息: {output}")
            print("\n可能的原因：")
            print("1. Git用户信息未配置完整")
            print("2. 权限问题")
            return False
    
    # 推送到GitHub
    print("推送到GitHub...")
    print("注意：如果弹出浏览器窗口要求授权，请完成授权流程。")
    print("如果授权失败，您可以尝试使用SSH密钥认证（推荐）或GitHub凭证管理器。")
    
    # 获取当前分支名称
    success, branch_output = run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=static_site_dir)
    if not success:
        print("获取当前分支名称失败")
        return False
    current_branch = branch_output.strip()
    print(f"当前分支：{current_branch}")
    
    success, output = run_command(["git", "push", "-u", "origin", current_branch], cwd=static_site_dir)
    if not success:
        print(f"推送失败: {output}")
        print("\n可能的原因：")
        print("1. GitHub凭证错误或已过期")
        print("2. 对GitHub仓库没有写入权限")
        print("3. 授权流程未完成")
        print("4. 网络连接问题")
        print("\n解决方案：")
        print("1. 检查GitHub凭证是否正确")
        print("2. 确认对该仓库有写入权限")
        print("3. 确保完成了浏览器授权流程")
        print("4. 检查网络连接是否正常")
        print("5. 考虑使用SSH密钥认证（详见GITHUB_AUTH_GUIDE.md）")
        print("\n如果问题仍然存在，请查看GITHUB_AUTH_GUIDE.md获取详细指导。")
        return False
    
    return True


def print_deployment_guide():
    """打印部署指南"""
    print("====================================")
    print("部署成功！")
    print("接下来的步骤：")
    print("1. 登录您的GitHub账户")
    print("2. 进入您的仓库页面")
    print("3. 点击Settings设置")
    print("4. 在左侧菜单中找到Pages")
    print("5. 在Source选项中，选择main branch作为源")
    print("6. 点击Save保存设置")
    print("7. 等待几分钟，您的网站将自动部署")
    print("8. 访问 https://用户名.github.io/仓库名称 查看您的网站")
    print("====================================")


def main():
    """主函数"""
    print("====================================")
    print("AI模型数据报告 - GitHub Pages部署脚本")
    print("====================================")
    
    # 设置静态网站目录路径
    static_site_dir = "d:\\用户\\ai_model_data_scraper\\static_site"
    
    # 检查Git是否安装
    check_git_installed()
    
    # 检查静态网站目录是否存在
    check_static_site_dir(static_site_dir)
    
    # 初始化Git仓库（如果不存在）
    if not initialize_git_repo(static_site_dir):
        input("按Enter键退出...")
        sys.exit(1)
    
    # 部署到GitHub
    if deploy_to_github(static_site_dir):
        # 打印部署指南
        print_deployment_guide()
        
        # 询问是否打开GitHub网站
        open_github = input("\n您想现在打开GitHub网站吗？(y/n): ")
        if open_github.lower() == 'y':
            webbrowser.open("https://github.com")
    else:
        print("部署失败！")
    
    input("\n部署脚本执行完毕。按Enter键退出...")


if __name__ == "__main__":
    main()