---
title: 升级一下 Hexo
categories: 技术
tags: 
  - 技术
  - blog
date: 2022-01-04
toc: false
---

GitHub 提醒 Hexo 有一个安全问题 [CVE-2021-25987](https://github.com/hexojs/hexo/issues/4838)，需要升级到最新版本。


把 package.json 修改 Hexo 版本为 6.0.0，推送看 GitHub Action 任务，有错误：
```bash
INFO  Validating config
WARN  Deprecated config detected: "external_link" with a Boolean value is deprecated. See https://hexo.io/docs/configuration for more details.
FATAL TypeError: Object.fromEntries is not a function
```

一个是 external_link 属性要过时了的警告，一个是函数不存在问题。

看下 Hexo 的[配置文档](https://hexo.io/docs/configuration#Writing)。
```bash
external_link	Open external links in a new tab?	
external_link.enable	Open external links in a new tab?	true
external_link.field	Applies to the whole site or post only	site
external_link.exclude	Exclude hostname. Specify subdomain when applicable, including www	[]
```

external_link 配置有变化，在 _config.yml 改为
```bash
external_link:
  enable: true # Open external links in new tab
  field: site # Apply to the whole site
  exclude: ''
```

另一个错误 Object.fromEntries is not a function，是因为 Nodejs 版本低了，需要 12.x 以上版本才行。

修改自动化部署配置文件 HexoCI.yml，Nodejs 版本改成 12.x。
```
- name: Setup node 
  uses: actions/setup-node@v1
  with:
    node-version: '12.x'
```

package.json 中一些比较老的依赖也可以随手升级下：
```bash
D:\application\hexo>npm outdated
Package                       Current  Wanted  Latest  Location  Depended by
hexo                          MISSING   6.0.0   6.0.0  -         hexo
hexo-abbrlink                 MISSING   2.2.1   2.2.1  -         hexo
hexo-deployer-git             MISSING   0.2.0   3.0.0  -         hexo
hexo-generator-archive        MISSING   0.1.5   1.0.0  -         hexo
hexo-generator-baidu-sitemap  MISSING   0.1.9   0.1.9  -         hexo
hexo-generator-category       MISSING   0.1.3   1.0.0  -         hexo
hexo-generator-feed           MISSING   1.2.2   3.0.0  -         hexo
hexo-generator-index          MISSING   0.2.1   2.0.0  -         hexo
hexo-generator-json-content   MISSING   3.0.1   4.2.3  -         hexo
hexo-generator-search         MISSING   2.4.3   2.4.3  -         hexo
hexo-generator-sitemap        MISSING   1.2.0   2.2.0  -         hexo
hexo-generator-tag            MISSING   0.2.0   1.0.0  -         hexo
hexo-renderer-ejs             MISSING   0.2.0   2.0.0  -         hexo
hexo-renderer-marked          MISSING  0.2.11   4.1.0  -         hexo
hexo-renderer-pug             MISSING   0.0.5   2.0.0  -         hexo
hexo-renderer-sass            MISSING   0.3.2   0.4.0  -         hexo
hexo-renderer-scss            MISSING   1.2.0   1.2.0  -         hexo
hexo-renderer-stylus          MISSING   0.3.3   2.0.1  -         hexo
hexo-server                   MISSING   0.2.2   3.0.0  -         hexo
node-sass                     MISSING   5.0.0   7.0.1  -         hexo
```

我懒得升级，等有问题再看吧。

### 2022-03-06 升级

```bash
# 查看版本
hexo -v
# 升级覆盖安装
npm install -g hexo-cli
# 新建目录初始化 hexo
hexo init <folder>
# 再看下版本
hexo -v
```

之前的版本 hexo 一些依赖可能已经没用了，比如 `node-sass` 早该弃用了。备份 package.json，把刚刚初始化的新的 package.json 复制过来，如果有用到 hexo 默认安装以外的插件，手动添加上去。

```bash
# 主要看下三方插件用不用升级
# 没有新增其他依赖下面两个命令就不用执行了
npm outdated
npm install -save
```

例如我自己的 package.json 整理后：

```json
{
  "name": "hexo-site",
  "version": "0.0.0",
  "private": true,
  "scripts": {
    "build": "hexo generate",
    "clean": "hexo clean",
    "deploy": "hexo deploy",
    "server": "hexo server"
  },
  "hexo": {
    "version": "6.0.0"
  },
  "dependencies": {
    "hexo": "^6.0.0",
    "hexo-generator-archive": "^1.0.0",
    "hexo-generator-category": "^1.0.0",
    "hexo-generator-index": "^2.0.0",
    "hexo-generator-tag": "^1.0.0",
    "hexo-renderer-ejs": "^2.0.0",
    "hexo-renderer-marked": "^5.0.0",
    "hexo-renderer-stylus": "^2.0.0",
    "hexo-server": "^3.0.0",
 	  "hexo-deployer-git": "^3.0.0",
	  "hexo-abbrlink": "^2.2.1"
  }
}
```

比默认 hexo 多加了 hexo-deployer-git 和 hexo-abbrlink 依赖，去掉了 hexo-theme-landscape 主题依赖，因为用了其他主题。

