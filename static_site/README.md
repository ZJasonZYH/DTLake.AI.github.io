
# AI模型数据报告

## 项目简介

这是一个基于GitHub Pages托管的静态网站，用于展示从artificialanalysis.ai网站抓取的AI模型性能数据，包括智能指数、运行成本和输出速度排名。

## 功能特性

- 📊 展示最新的AI模型性能对比图表
- 📈 提供时间序列数据可视化
- 📋 详细的模型排名数据表
- 🌐 响应式设计，支持各种设备访问
- 🚀 静态网站，加载速度快

## 数据来源

数据来源于 [artificialanalysis.ai](https://artificialanalysis.ai/) 网站，包括：

1. Artificial Analysis Intelligence Index
2. Cost to Run Artificial Analysis Intelligence Index
3. Output Speed
4. Frontier Language Model Intelligence Over Time

## 数据更新

数据每月更新一次，并自动归档历史数据。

## 本地开发

如果您想在本地运行此项目：

1. 克隆仓库
2. 使用任何静态文件服务器托管 `static_site` 目录
3. 访问 http://localhost:端口号

例如，使用Python的内置服务器：

```bash
cd static_site
python -m http.server 8000
```

## 部署

1. 将代码推送到GitHub仓库
2. 在仓库设置中，找到GitHub Pages部分
3. 选择主分支作为源
4. 保存设置，几分钟后网站将自动部署

## 许可证

MIT
