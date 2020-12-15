---
title: eclipse neon版本打开某些javascript文件异常问题
categories: 技术
tags: 其他
date: 2017-05-02
---
eclipse neon版本的javascript编辑器无法处理某些异常信息，比如本人在用require js和vue js的时候碰过这种异常
<p style="word-wrap:break-word;word-break:break-all;">
java.lang.NoSuchMethodError:jdk.nashorn.internal.runtime.ECMAException.getEcmaError()Ljava/lang/Object;
</p>
然后js文件直接就打不开了，最终在stackoverflow找到相关问题，链接
http://stackoverflow.com/questions/38089331/eclipse-neon-java-ee-ide-javascript-editor-broken

照回答者意思是javascript开发工具没法解析某些特殊语法的js代码；
另一个回答是说新版本的jdk已经解决这个问题，尝试卸了jdk（一直用的1.8.0_05版），装上最新版本的（目前是1.8.0_131版），问题解决。（仅供参考）
