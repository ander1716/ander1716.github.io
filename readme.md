# z-blog

一个基于 Jekyll 搭建的个人静态博客，用来沉淀技术实践、产品思考、AI/LLM 学习笔记、代码片段和日常随笔。

站点包含首页、文章详情、分类页、标签页、网站导航页、关于页等页面，并集成了代码高亮、文章目录、侧边栏、友情链接、Algolia 搜索数据同步脚本等能力。

## 技术栈

- 静态站点生成：Jekyll 4.4
- 主题基础：minima
- 模板语言：Liquid
- 样式：SCSS / CSS
- Markdown 渲染：kramdown
- 代码高亮：Rouge + Prism.js
- 搜索索引：Algolia（通过 Python 脚本同步）
- 部署方式：适合 GitHub Pages 或其他静态站点托管服务

## 目录结构

```text
.
├── _config.yml                 # Jekyll 主配置
├── _data/                      # 导航、页脚、网站导航等数据配置
├── _includes/                  # 可复用页面片段
├── _layouts/                   # 页面布局模板
├── _posts/                     # 文章目录
│   ├── blog/                   # 长文、专题、技术文章
│   ├── code/                   # 代码片段
│   └── daily/                  # 日常思考
├── assets/                     # 样式、脚本等静态资源
├── about.md                    # 关于页
├── categories.md               # 分类页
├── tags.md                     # 标签页
├── guide.html                  # 网站导航页
├── upload_to_algolia_by_requrst.py # Algolia 索引同步脚本
├── Gemfile                     # Ruby / Jekyll 依赖
├── requirements.txt            # Python 脚本依赖
└── CNAME                       # 自定义域名配置
```

> `_site/` 是 Jekyll 构建产物，不建议直接修改。

## 本地运行

### 1. 安装 Ruby 依赖

确保本机已经安装 Ruby 和 Bundler，然后在项目根目录执行：

```bash
bundle install
```

### 2. 启动开发服务

```bash
bundle exec jekyll serve
```

也可以直接运行：

```bash
sh start.sh
```

启动后访问：

```text
http://127.0.0.1:4000/
```

### 3. 构建静态文件

```bash
bundle exec jekyll build
```

构建结果会输出到 `_site/`。

## 内容写作

文章统一放在 `_posts/` 下，当前按内容类型分为：

- `_posts/blog/`：专题文章、技术笔记、产品和 AI 相关长文
- `_posts/code/`：代码片段和工程实践记录
- `_posts/daily/`：日常思考和个人观察

文件名建议使用 Jekyll 约定：

```text
YYYY-MM-DD-文章标题.md
```

示例：

```text
_posts/blog/2026-02-21-langchain核心api.md
```

常用 Front Matter：

```yaml
---
layout: post
title: "文章标题"
date: 2026-02-21
last_modified_at: 2026-02-21
categories: [技术纵横]
tags: [langchain, llm]
cover: https://example.com/cover.jpg
excerpt: >
  这里填写文章摘要，会用于列表页展示。
---
```

字段说明：

- `layout`：文章页使用 `post`
- `title`：文章标题
- `date`：发布日期
- `last_modified_at`：最后更新时间
- `categories`：分类，分类页会按该字段筛选文章
- `tags`：标签，标签页会按该字段筛选文章
- `cover`：文章封面图，可选
- `excerpt`：摘要，可选；未填写时 Jekyll 会从正文截取

## 分类和导航

当前首页和导航中主要使用这些分类：

- 产品思维
- 设计与体验
- 技术纵横
- 运营增长
- 漫谈与思考
- 代码片段

相关配置位置：

- 顶部导航：`_data/navigation.yml`
- 页脚信息：`_data/footer.yml`
- 网站导航页数据：`_data/guided.yml`
- 分类页：`categories.md`
- 标签页：`tags.md`

新增分类时，建议同步检查首页卡片、导航、页脚链接和文章 Front Matter，避免出现分类页没有入口或入口无文章的情况。

## Algolia 搜索索引同步

项目提供了 `upload_to_algolia_by_requrst.py`，用于把文章内容同步到 Algolia。

### 1. 创建 Python 虚拟环境

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制示例配置：

```bash
cp .env.example .env
```

然后在 `.env` 中配置：

```text
ALGOLIA_APP_ID=你的应用 ID
ALGOLIA_API_KEY=你的 API Key
ALGOLIA_INDEX_NAME=你的索引名称
```

`.env` 已加入 `.gitignore`，不要提交真实密钥。

### 4. 执行同步

```bash
python upload_to_algolia_by_requrst.py
```

注意：当前文章实际存放在 `_posts/blog`、`_posts/code`、`_posts/daily` 等子目录中。同步前建议确认脚本是否已经递归扫描子目录，避免索引数据不完整。

## 常用维护命令

```bash
# 本地预览
bundle exec jekyll serve

# 构建站点
bundle exec jekyll build

# 安装 Ruby 依赖
bundle install

# 安装 Python 脚本依赖
pip install -r requirements.txt

# 同步 Algolia 索引
python upload_to_algolia_by_requrst.py
```

## 部署说明

这是一个静态站点项目，构建后的 `_site/` 可部署到 GitHub Pages、Nginx、Vercel、Netlify、Cloudflare Pages 等静态托管服务。

如果使用 GitHub Pages：

1. 确认仓库设置中启用了 Pages。
2. 如果使用自定义域名，维护根目录下的 `CNAME`。
3. 推送代码后由托管平台构建或部署静态产物。

## 维护注意事项

- 修改 `_config.yml` 后需要重启 `jekyll serve` 才会生效。
- 不要直接修改 `_site/` 中的文件，应该修改源文件后重新构建。
- 新增文章后建议本地预览分类页、标签页和文章详情页。
- 真实密钥只放在 `.env`，不要提交到 Git。
- 如果调整文章目录层级，需要同步检查 Algolia 同步脚本、分类页和构建结果。
