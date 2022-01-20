---
title: 把 Tiddlywiki 整合到 Hexo 中一起部署
categories: 技术
tags: 
    - Tiddlywiki
    - Hexo
date: 2022-01-20
---

最近在找一款 wiki 用来记录一些系统化的知识和笔记，发现了 [TiddlyWiki](https://tiddlywiki.com/) 这个东西。TiddlyWiki 是一个仅由单个 HTML 文件组成的非网络应用的 Wiki 程序，不依赖数据库存储数据，非常有特色，能装插件，玩法也比较多。

后来想到既然最后发布到互联网都是静态文件，那就放到 Hexo 一起部署好了，不需要再搞一个服务来放 TiddlyWiki 的单 HTML 文件了。

我们可以将 TiddlyWiki 的单 HTML 文件放到 Hexo 的 public/wiki 文件夹中，在网站放个 /wiki 入口，随着 Hexo 的提交部署就可以访问了。但随着 wiki 越写越多，生成的单 HTML 文件越来越大，push 也慢，我们不用这种方式。其实我们只关心写东西，其他麻烦的事情全都交给 GitHub Action 或其他自动化部署工具来做就行了。下面是整合的步骤。

### 整合

先安装 TiddlyWiki：

```bash
npm install -g tiddlywiki
tiddlywiki  --version
```

在 Hexo 根目录下初始化一个 TiddlyWiki：

```bash
tiddlywiki tiddlywiki --init server
```

我们写的 wiki 的源文件就放在 tiddlywiki/tiddlers 文件夹中，类似 Hexo 的 source/_posts 文件夹。

Hexo 主题配置加个 wiki 入口：

```bash
menu:
  Home: /
  Archives: /archives
  About: /about
  wiki: /wiki
```

### 修改 GitHub Action 脚本

```yml
name: CI
on:
  push:
    branches:
      - hexo-blog
jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout source
        uses: actions/checkout@v1
        with:
          ref: hexo-blog
      - name: Setup node 
        uses: actions/setup-node@v1
        with:
          node-version: '12.x'
      - name: Setup hexo
        env:
          ACTION_DEPLOY_KEY: ${{ secrets.HEXO_DEPLOY_PRI }}
        run: |
          mkdir -p ~/.ssh/
          echo "$ACTION_DEPLOY_KEY" > ~/.ssh/id_rsa
          chmod 600 ~/.ssh/id_rsa
          ssh-keyscan github.com >> ~/.ssh/known_hosts
          git config --global user.email "xx@xx.com"
          git config --global user.name "yourname"
          npm install hexo-cli -g
          npm install tiddlywiki -g
          npm install
      - name: Hexo deploy
        run: |
          hexo clean
          hexo g
          tiddlywiki tiddlywiki --build index
          mkdir public/wiki
          mv tiddlywiki/output/index.html public/wiki
          hexo d
```
- `npm install tiddlywiki -g` 把 tiddlywiki 也装上

- `hexo g` 执行生成静态文件到 public 文件夹中；

- `tiddlywiki tiddlywiki --build index` 输出 index.html 文件到 tiddlywiki/output 文件夹；

- 在 public 创建 wiki 文件夹，再把 index.html 移过来就完事了。

还有另外一种方法可以先在 source 文件夹下创建 wiki 目录，然后修改 GitHub Action 脚本，先生成 index.html 文件，然后移动到 source/wiki 目录下，然后再 `hexo g` 编译也行，大概改成这样，自行测试：

```bash
- name: Hexo deploy
  run: |
    hexo clean
    mkdir source/wiki
    tiddlywiki tiddlywiki --build index
    mv tiddlywiki/output/index.html source/wiki
    # hexo g 应该都可以不写了
    hexo g
    hexo d
```

不过要设置下 Hexo 不要把 index.html 也编译了：

```bash
# _config.yml skip_render 配置，编译渲染忽略 wiki 下的所有文件
skip_render: [wiki/**]
```

效果：
- [主页](https://zguishen.com/)
- [wiki](https://zguishen.com/wiki/)

### 参考

- [1] [Hexo 自动化部署的参考 GitHub Actions deploy Hexo blog](https://zguishen.com/posts/936b5ee4.html)
- [2] [Tiddlywiki - 维基百科，自由的百科全书](https://zh.wikipedia.org/wiki/Tiddlywiki)
