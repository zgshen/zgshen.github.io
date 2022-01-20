
可参考官方文档 [How to apply custom styles](https://tiddlywiki.com/#How%20to%20apply%20custom%20styles)。

新建条目随便命名个 [Custom data-styles](#Custom%20data-styles)，标签设置为 `$:/tags/Stylesheet`。如果要把本条目的内容设置为红色可以这么写：
```css
[data-tiddler-title="自定义CSS"] {
  color: red;
}
```

能看到这个条目的字体是红的了。其实就是根据 attribute 的值，把有对应 attribute 的内容加上样式。

如果加普通样式的话，直接写 css 就行，比如给网站加上背景图：
```css
body {
    background-image: url(../images/wiki/ganyu.jpg);
    background-repeat: no-repeat;
	background-attachment:fixed;
}
```