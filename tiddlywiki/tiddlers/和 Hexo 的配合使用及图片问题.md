既然 Tiddlywiki 能编译成一个静态 html ，那就可以放到 Hexo 网站里，毕竟 Hexo 也是一样将 Markdown 文件转换成静态文件部署的。Tiddlywiki 的图片或其他附件也就可以放到 Hexo 的资源目录下，比如我的图片是放在 \source\images\wiki 目录下。Tiddlywiki 本身也能上传图片，但是会转成 base64（应该是）塞到 html 里面去，所以最好别这么用，不然图片多了 html 文件巨大，而且要配置 Hexo 一起用 Github Action 自动化部署也不能这么干，后面我会先写篇文章说 Tiddlywiki  怎么放到 Hexo 里面一起（写完了[把 Tiddlywiki 整合到 Hexo 中一起部署](https://zguishen.com/posts/f690ac06.html)），其实很简单的。

既然图片放到 Hexo 资源文件夹下，那么我们本地在写 wiki 的时候就会有图片访问的问题，可以用 Nginx 整一下就行了。图片链接跟 Hexo 文章一样写相对路径，比如背景图 `../images/wiki/ganyu.jpg`，这里转发一下，hexo 目录是 `D:\application\hexo`，Nginx 监听7000端口，Tiddlywiki 启动用7001端口，用 http://127.0.0.1:7000/ 访问 wiki。

```nginx
server {
	listen       7000;
	server_name  localhost;
	
	location ^~/images/ {
		root   D:\Project\gitFile\zgshen\source;
	}
	location / {
		proxy_pass http://127.0.0.1:7001;
		proxy_set_header        Host             $host;
		proxy_set_header        X-Real-IP        $remote_addr;
		proxy_set_header        X-Forwarded-For  $proxy_add_x_forwarded_for;
	}
}

```

启动 Nginx 和 Tiddlywiki 烦的话写个 bat 脚本（注意不要保存为 tiddlywiki.bat，会与 tiddlywiki 命令冲突，保存为其他名字如 mywiki.bat 就行）：

```bash
tasklist | find /i "nginx.exe" >nul 2>nul && goto 存在 || goto 不存在

:存在

echo nginx程序存在
goto 启动

:不存在

echo nginx程序不存在
D:
cd D:\application\nginx-1.10.1\
start nginx.exe
echo 'nginx 后台运行'
goto 启动

:启动

echo 启动tiddlywiki
tiddlywiki D:\application\hexo\mywiki --listen port=7001
echo 'tiddlywiki started.'
```