---
title: Let's Encrypt HTTPS 证书自动续期
categories: 技术
tags: 基础
date: 2021-08-23
---

Let's Encrypt 可以申请免费的 HTTPS 证书，一般网站都够用了，证书的有效期是 90 天，90 天过期后就要重新申请。[Let's Encrypt 官方](https://letsencrypt.org/zh-cn/getting-started/)推荐使用 [Certbot](https://certbot.eff.org/) ACME 客户端来自动签发证书。

以 CentOS 7 为部署在 Nginx 上的网站域名自动签证为例子。进入 https://certbot.eff.org/lets-encrypt/centosrhel7-nginx 按操作安装 certbot ，如果服务器上没有 snap 客户端须先安装。

先看看之前良心云搞的证书在 Nginx 的 443 端口配置：
``` nginx
server {
    listen       443 ssl;
    server_name  zkcing.com;

    ssl_certificate      1_zkcing.com_bundle.crt;
    ssl_certificate_key  2_zkcing.com.key;

    ssl_session_cache    shared:SSL:1m;
    ssl_session_timeout  5m;

    ssl_ciphers  HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers  on;

    location / {
        root   /usr/share/nginx/html/public;
        index  index.html index.htm;
        #proxy_pass http://127.0.0.1:4000;
    }
}
```

最后执行自动签证命令 `sudo certbot --nginx`（想自己整的用 `sudo certbot certonly --nginx`）

不想输入邮箱的话命令带上 `--register-unsafely-without-email` 跳过，填邮箱是用来发一些提醒的，used for urgent renewal and security notices。

```bash
# root @ VM-0-16-centos in /etc/nginx [18:01:10] C:1
$ sudo certbot --nginx
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Enter email address (used for urgent renewal and security notices)
 (Enter 'c' to cancel): 
Invalid email address: .


If you really want to skip this, you can run the client with
--register-unsafely-without-email but you will then be unable to receive notice
about impending expiration or revocation of your certificates or problems with
your Certbot installation that will lead to failure to renew.

Enter email address (used for urgent renewal and security notices)
 (Enter 'c' to cancel): xxx@xx.com

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Please read the Terms of Service at
https://letsencrypt.org/documents/LE-SA-v1.2-November-15-2017.pdf. You must
agree in order to register with the ACME server. Do you agree?
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
(Y)es/(N)o: y

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Would you be willing, once your first certificate is successfully issued, to
share your email address with the Electronic Frontier Foundation, a founding
partner of the Let's Encrypt project and the non-profit organization that
develops Certbot? We'd like to send you email about our work encrypting the web,
EFF news, campaigns, and ways to support digital freedom.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
(Y)es/(N)o: n
Account registered.

Which names would you like to activate HTTPS for?
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
1: zkcing.com
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Select the appropriate numbers separated by commas and/or spaces, or leave input
blank to select all options shown (Enter 'c' to cancel): 1
Requesting a certificate for zkcing.com

Successfully received certificate.
Certificate is saved at: /etc/letsencrypt/live/zkcing.com/fullchain.pem
Key is saved at:         /etc/letsencrypt/live/zkcing.com/privkey.pem
This certificate expires on 2021-11-21.
These files will be updated when the certificate renews.
Certbot has set up a scheduled task to automatically renew this certificate in the background.

Deploying certificate
Successfully deployed certificate for zkcing.com to /etc/nginx/nginx.conf
Congratulations! You have successfully enabled HTTPS on https://zkcing.com

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
If you like Certbot, please consider supporting our work by:
 * Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
 * Donating to EFF:                    https://eff.org/donate-le
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
```

自动更新后的 Nginx 配置，自动给替换了，再去网站看看生效没，完事。
``` nginx
    server {
    listen       443 ssl;
    server_name  zkcing.com;
    ssl_certificate /etc/letsencrypt/live/zkcing.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/zkcing.com/privkey.pem; # managed by Certbot

    ssl_session_cache    shared:SSL:1m;
    ssl_session_timeout  5m;

    ssl_ciphers  HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers  on;

    location / {
        root   /usr/share/nginx/html/public;
        index  index.html index.htm;
        #proxy_pass http://127.0.0.1:4000;
    }
}
```

