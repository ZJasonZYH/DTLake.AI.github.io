# GitHub Pages 部署详细指南

## 目录
- [准备工作](#准备工作)
- [方法一：手动部署（使用批处理脚本）](#方法一手动部署使用批处理脚本)
- [方法二：手动部署（命令行）](#方法二手动部署命令行)
- [配置自动更新（GitHub Actions）](#配置自动更新github-actions)
- [自定义域名设置](#自定义域名设置)
- [故障排除](#故障排除)
- [常见问题](#常见问题)

## 准备工作

### 1. 创建GitHub账号
如果您还没有GitHub账号，请先在 [GitHub官网](https://github.com) 注册一个账号。

### 2. 创建新仓库
1. 登录GitHub后，点击右上角的 "+" 图标，选择 "New repository"（新建仓库）
2. 输入仓库名称（例如：`ai-model-data-report`）
3. 选择仓库可见性（公开或私有均可）
4. 点击 "Create repository" 按钮创建仓库

### 3. 安装Git（如果尚未安装）
- Windows: 下载并安装 [Git for Windows](https://git-scm.com/download/win)
- macOS: 使用Homebrew安装 `brew install git`
- Linux: 使用包管理器安装，如 `apt install git` 或 `yum install git`

## 方法一：手动部署（使用批处理脚本）

本项目提供了一个便捷的批处理脚本，可以帮助您轻松部署网站。

### 步骤

1. **确保静态网站已生成**
   运行 `generate_static_site.py` 确保 `static_site` 目录已生成所有必要文件。

2. **运行部署脚本**
   - 双击 `deploy_to_github_pages.bat` 文件
   - 按照提示输入您的GitHub用户名、邮箱和仓库URL
   - 脚本将自动初始化Git仓库、添加文件、提交更改并推送到GitHub

3. **配置GitHub Pages**
   - 登录GitHub，进入您的仓库页面
   - 点击 "Settings"（设置）
   - 在左侧菜单中找到 "Pages"
   - 在 "Source" 选项中，选择 "main branch" 作为源
   - 点击 "Save" 保存设置

4. **访问您的网站**
   - 等待几分钟，GitHub Pages将自动构建您的网站
   - 访问 `https://您的用户名.github.io/仓库名称` 查看部署后的网站

## 方法二：手动部署（命令行）

如果您更喜欢使用命令行部署，可以按照以下步骤操作：

### 步骤

1. **进入静态网站目录**
   ```bash
   cd d:\用户\ai_model_data_scraper\static_site
   ```

2. **初始化Git仓库**
   ```bash
   git init
   ```

3. **设置Git用户名和邮箱**
   ```bash
   git config user.name "您的GitHub用户名"
   git config user.email "您的GitHub邮箱"
   ```

4. **添加远程仓库**
   ```bash
   git remote add origin https://github.com/您的用户名/您的仓库名称.git
   ```

5. **添加所有文件**
   ```bash
   git add .
   ```

6. **提交更改**
   ```bash
   git commit -m "初始提交：AI模型数据报告"
   ```

7. **推送到GitHub**
   ```bash
   git push -u origin main
   ```

8. **按照方法一中的步骤3和4配置GitHub Pages并访问您的网站**

## 配置自动更新（GitHub Actions）

为了实现数据的自动更新，您可以配置GitHub Actions工作流，定期重新抓取数据并更新网站。

### 步骤

1. **创建GitHub Actions配置文件**

   在您的仓库中创建以下目录结构和文件：
   ```
   .github/workflows/update-data.yml
   ```

2. **添加工作流配置**

   复制以下内容到 `update-data.yml` 文件中：

   ```yaml
   name: 自动更新AI模型数据

   on:
     # 每月1日的上午9点自动运行
     schedule:
       - cron: '0 9 1 * *'
     # 允许手动触发工作流
     workflow_dispatch:

   jobs:
     update-and-deploy:
       runs-on: ubuntu-latest
       steps:
         - name: 检出代码
           uses: actions/checkout@v3

         - name: 设置Python环境
           uses: actions/setup-python@v4
           with:
             python-version: '3.13'

         - name: 安装依赖
           run: |
             python -m pip install --upgrade pip
             pip install requests beautifulsoup4 matplotlib pandas seaborn scikit-learn

         - name: 下载生成脚本
           run: |
             mkdir -p ../scripts
             curl -o ../scripts/generate_static_site.py https://raw.githubusercontent.com/您的用户名/您的仓库名称/main/generate_static_site.py
             curl -o ../scripts/ai_model_scraper.py https://raw.githubusercontent.com/您的用户名/您的仓库名称/main/ai_model_scraper.py
             chmod +x ../scripts/generate_static_site.py

         - name: 生成最新数据和静态网站
           run: |
             cd ..
             python scripts/generate_static_site.py

         - name: 更新仓库内容
           run: |
             # 复制生成的文件到当前目录
             cp -r ../static_site/* .
             rm -rf ../static_site
             
             # 配置Git
             git config --global user.name 'GitHub Actions Bot'
             git config --global user.email 'actions@github.com'
             
             # 添加并提交更改
             git add .
             git commit -m "自动更新AI模型数据 $(date +'%Y-%m-%d')"
             
             # 推送到仓库
             git push origin main
   ```

   > **注意**：请将 `您的用户名` 和 `您的仓库名称` 替换为您的实际GitHub用户名和仓库名称。

3. **保存并推送配置文件**

   将配置文件保存并推送到GitHub仓库，GitHub Actions将自动识别并启用此工作流。

4. **手动测试工作流**

   - 进入GitHub仓库页面
   - 点击 "Actions" 选项卡
   - 在左侧列表中找到 "自动更新AI模型数据"
   - 点击 "Run workflow" 按钮手动触发一次工作流

## 自定义域名设置

如果您拥有自己的域名，可以将其与GitHub Pages站点关联。

### 步骤

1. **配置DNS记录**

   登录您的域名注册商网站，添加以下DNS记录：

   - 类型：`CNAME`
   - 名称：`www`（或您想要的子域名）
   - 值：`您的用户名.github.io`
   - TTL：建议设置为300或最小可用值

2. **在GitHub中配置自定义域名**

   - 进入GitHub仓库页面
   - 点击 "Settings"（设置）
   - 在左侧菜单中找到 "Pages"
   - 在 "Custom domain" 字段中输入您的自定义域名（例如：`www.yourdomain.com`）
   - 点击 "Save" 保存设置
   - 勾选 "Enforce HTTPS" 选项启用HTTPS

3. **等待DNS传播**

   DNS更改可能需要24-48小时才能完全传播，请耐心等待。

## 故障排除

### 常见错误及解决方案

1. **无法推送到GitHub**
   - 检查您的GitHub凭证是否正确
   - 确认您对仓库有写入权限
   - 尝试使用SSH密钥进行认证

2. **GitHub Pages不显示网站**
   - 确认您已正确配置了Pages源（main branch）
   - 检查是否有构建错误（在Actions选项卡中查看）
   - 清除浏览器缓存后重试

3. **自动更新工作流失败**
   - 检查Actions日志获取详细错误信息
   - 确保依赖包名称正确
   - 验证脚本路径和权限设置

4. **图片或CSS不显示**
   - 确认文件路径在HTML中是正确的
   - 检查文件大小写是否匹配（GitHub Pages对大小写敏感）
   - 确保文件已正确提交并推送到仓库

## 常见问题

### 1. 网站更新后多久能在GitHub Pages上看到变化？

通常情况下，GitHub Pages会在您推送更改后的1-10分钟内更新。有时可能需要更长时间，特别是在GitHub系统负载较高时。

### 2. 我可以使用私有仓库来托管GitHub Pages吗？

是的，自2020年起，GitHub支持从私有仓库托管GitHub Pages，但只有仓库所有者和协作者可以访问网站。

### 3. 如何监控自动更新工作流的运行状态？

您可以在GitHub仓库的Actions选项卡中查看工作流的运行历史和状态。GitHub还支持通过邮件或Webhook通知工作流状态变化。

### 4. 静态网站的大小有限制吗？

GitHub Pages有以下限制：
- 每个网站的总大小限制为1GB
- 每小时推送次数限制为10次
- 每月带宽限制为100GB

对于AI模型数据报告这类网站，这些限制通常不会成为问题。

## 联系与支持

如果您在部署过程中遇到任何问题，请参考[GitHub Pages官方文档](https://docs.github.com/cn/pages)获取更多帮助。