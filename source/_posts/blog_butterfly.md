---
title: 博客（二）：美化你的个人博客
date: 2023-08-21
categories:
  - 博客
tags:
  - 博客
  - nodejs
  - npm
  - Hexo
  - Butterfly
---


*此文章将会指引你使用butterfly美化你的hexo博客*

# 一. 部署butterfly主题


## 1. butterfly主题

butterfly是hexo框架下的一个主题。
butterfly主题：
![Alt text](/img/blog_butterfly/image.png)
相比于原生的hexo博客样式，我相信你肯定更喜欢butterfly。
了解更多？[butterfly](https://butterfly.js.org/)

## 2. 下载butterfly主题

参考文档：[Butterfly 安裝文檔(一) 快速開始](https://butterfly.js.org/posts/21cfbf15/)
在myblog目录下输入命令安装butterfly：

```
git clone -b master https://github.com/jerryc127/hexo-theme-butterfly.git themes/butterfly

```


## 3. 安装插件

安装pug和stylus渲染器：

```
npm install hexo-renderer-pug hexo-renderer-stylus --save

```


## 4. 应用主题

修改配置文件_config.yml：

```
theme: butterfly

```


## 5. 升级建议

为了減少升级主题带来的不便，我们可以把主题文件夹中的 _config.yml 重命名为 _config.butterfly.yml，复制到 Hexo 根目录下与_config.yml同级。
Hexo会自动合并主题中的_config.yml和 _config.butterfly.yml ，如果存在同名配置，会使用_config.butterfly.yml的配置，其优先度较高。所以像和博客网址相关联的固定资料可以设置在_config.yml中，比如博客的标题、作者信息和邮箱等等资料，而和主题样式相关的配置放在 _config.butterfly.yml 中，那么在将来你想换一个主题是很方便的。

# 二. 美化主题


## 1. 图片&图标


### （1）网站图标

**.config.butterfly.yml配置：**

```
    # Favicon（網站圖標）
    favicon: /img/favicon.jpg

```

将网站图标favicon.jpg放置在此目录：blog\hexo\themes\butterfly\source\img
**效果图：**
![Alt text](/img/blog_butterfly/favicon.jpg)
![Alt text](/img/blog_butterfly/image-5.png)

### （2） 网站背景图片

**.config.butterfly.yml配置：**

```
# The banner image of home page
index_img: /img/background.jpg

```

将网站背景图片background.jpg放置在此目录：blog\hexo\themes\butterfly\source\img
**效果图：**
![Alt text](/img/blog_butterfly/background.jpg)
![Alt text](/img/blog_butterfly/image-1.png)

### （3） 作者头像


```
# Avatar (頭像)
avatar:
img: /img/avatar.jpg
effect: false

```

将作者头像avatar.jpg放置在此目录：blog\hexo\themes\butterfly\source\img
**效果图：**
![Alt text](/img/blog_butterfly/avatar.jpg)
![Alt text](/img/blog_butterfly/image-2.png)

### （4） 菜单顶图


```
# If the banner of page not setting, it will show the top_img
default_top_img: /img/default_top_img.jpg

```

将菜单顶图default_top_img.jpg放置在此目录：blog\hexo\themes\butterfly\source\img
**效果图：**
![Alt text](/img/blog_butterfly/default_top_img.jpg)
*其他菜单页面同样显示默认顶图*
![Alt text](/img/blog_butterfly/image-6.png)

### （5） 404页面


```
# Replace Broken Images (替換無法顯示的圖片)
error_img:
flink: /img/friend_404.gif
post_page: /img/404.jpg

# A simple 404 page
error_404:
enable: true
subtitle: 'Page Not Found'
background: /img/404.jpg

```

这里使用默认的设置即可

### （6） 图片懒加载


```
# Lazyload (圖片懶加載)
# https://github.com/verlok/vanilla-lazyload
lazyload:
  enable: true
  loadingImg: /img/loading.gif
  field: site # site/post
  placeholder:
  blur: false

```


## 2. 网站首页

**_config.yml配置：**

```
# Site
title: 良月的小窝   #网站标题
subtitle: ''
description: 郎朗晴天   #个性签名
keywords:
author: 良月    #博客作者
language: zh-CN    #网站语言为简体中文
timezone: Asia/Shanghai     #Shanghai是中国时区

```

**_config.butterfly.yml配置：**

```
# the subtitle on homepage (主頁subtitle)
subtitle:
enable: true
# Typewriter Effect (开启打字效果)
effect: true
# loop (循環打字)
loop: true
# source調用第三方服務
# source: false 關閉調用
# source: 1  調用搏天api的隨機語錄（簡體）
# source: 2  調用一言網的一句話（簡體）
# source: 3  調用一句網（簡體）
# source: 4  調用今日詩詞（簡體）
# subtitle 會先顯示 source , 再顯示 sub 的內容
source: false
# 如果有英文逗号' , ',请使用转义字元 &#44;
# 如果有英文双引号' " ',请使用转义字元 &quot;
# 开头不允許转义字元，如需要，请把整個句子用双引号包住
# 如果关闭打字效果，subtitle只会现示sub的第一行文字
sub:
    - BY 良月
    - 山野渐染暮春色，碧落微醺残阳曦。
    - 碎花飘落云海地，琐事淡没扶摇时。
    - 凡人入梦蝴蝶语，天官醉酒云云归。
    - 众生皆苦非尘世，你我逍遥不自知。

```


## 3. 侧边栏


### 个人资料

**Follow Me：**

```
card_author:
    enable: true
    description:
    button:
    enable: true
    icon: fab fa-github
    text: Follow Me
    link: https://github.com/Yangcheneee    #GitHub个人主页

```

**社交媒体：**

```
# Social Settings (社交圖標設置)
# formal:
#   icon: link || the description || color
social:
fab fa-github: https://github.com/Yangcheneee || Github
fab fa-qq:  tencent://AddContact/?fromId=45&fromSubId=1&subcmd=all&uin=2657761647&website=www.oicqzone.com || QQ
fas fa-envelope-open-text: mailto:2657761647@qq.com || Email

```

**效果图：**
![Alt text](/img/blog_butterfly/image-11.png)

### 公告

**.config.butterfly.yml配置：**

```
card_announcement:
    enable: true
    content: 欢迎来到我的个人博客

```

**效果图：**
![Alt text](/img/blog_butterfly/image-13.png)

### 网站咨询

**.config.butterfly.yml配置：**

```
card_webinfo:
    enable: true
    post_count: true
    last_push_date: true
    sort_order: # Don't modify the setting unless you know how it works

```

**效果图：**
![Alt text](/img/blog_butterfly/image-14.png)

## 4. 导航菜单

**预览：**

## 

**_config.butterfly.yml配置：**

```
# Menu 目錄
menu:
主页: / || fas fa-home
博文 || fa fa-graduation-cap:    
 分类: /categories/ || fa fa-archive
 标签: /tags/ || fa fa-tags
 归档: /archives/ || fa fa-folder-open
生活 || fas fa-list:
 分享: /shuoshuo/ || fa fa-comments
 相册: /photos/ || fa fa-camera-retro
 音乐: /music/ || fa fa-music
 影视: /movies/ || fas fa-video
友链: /link/ || fa fa-link
留言板: /messageboard/ || fa fa-paper-plane
关于笔者: /about/ || fas fa-heart  

```


## 5. 本地搜索功能

**预览：**

## 

**安装搜索插件：**

```
npm install hexo-generator-search --save

```

**_config.butterfly.yml配置：**

```
# Local search
local_search:
  enable: true
  labels:
    input_placeholder: Search for Posts
    hits_empty: "We didn't find any results for the search: ${query}" # 如果没有查到内容相关内容显示

```


## 6. 博文：分类|标签|归档


### 创建分类界面


```
hexo new page categories

```

打开./source/categories/index.md

```
---
title: 分类
date: 2023-08-20 20:20:51
type: "categories"
comments: false
---

```


### 创建标签页面


```
hexo new page tags

```

打开./source/tags/index.md

```
---
title: 标签
date: 2023-08-20 20:20:16
type: "tags"
comments: false
orderby: random
order: 1
---

```


### 创建归档界面

默认创建…

## 7.生活：分享|相册|音乐|影视

待更新…

## 8. 友情链接页面

创建友情链接页面：

```
hexo new page link

```

打开source/link/index.md文件：

```
---
title: 友情链接
date: 2023-08-20 22:17:49
type: "link"
comments: false
---

```

添加友情链接：
在Hexo博客目录中的 source/_data（如果没有 _data 文件夾，请自行创建），创建一个文件 link.yml

```
- class_name: 友情链接
  class_desc: 执子之手，与子偕老。
  link_list:
    - name: Hexo
      link: https://hexo.io/zh-tw/
      avatar: https://d33wubrfki0l68.cloudfront.net/6657ba50e702d84afb32fe846bed54fba1a77add/827ae/logo.svg
      descr: 快速、簡單且強大的網誌框架

- class_name: 网站
  class_desc: 值得推荐的网站
  link_list:
    - name: Youtube
      link: https://www.youtube.com/
      avatar: https://i.loli.net/2020/05/14/9ZkGg8v3azHJfM1.png
      descr: 視頻網站
    - name: Weibo
      link: https://www.weibo.com/
      avatar: https://i.loli.net/2020/05/14/TLJBum386vcnI1P.png
      descr: 中國最大社交分享平台
    - name: Twitter
      link: https://twitter.com/
      avatar: https://i.loli.net/2020/05/14/5VyHPQqR6LWF39a.png
      descr: 社交分享平台

```


## 9. 留言板&评论

创建留言板界面：

```
hexo new page messageboard

```

打开./source/messageboard/index.md：

```
---
title: 留言板
date: 2023-08-20 20:21:06
types: "messageboard"
---

```


## 10. 关于笔者

创建关于笔者界面：

```
hexo new page about

```

打开./source/about/index.md：

```
---
title: 关于我
date: 2023-08-21 03:20:56
type: "about"
comments: false
---

```


## 11. 博文


### 代码块


### 文章分享

**_config.butterfly.yml配置：**

```
# Share.js
# https://github.com/overtrue/share.js
sharejs:
enable: true
sites: wechat,qq,weibo

```

**效果图：**
![Alt text](/img/blog_butterfly/image-7.png)

## 13. 音乐播放器


```
Inject:
bottom:
- '<div class="aplayer no-destroy" data-id="8674547170" data-server="netease" data-type="playlist" data-fixed="true" data-autoplay="true" data-lrcType="-1"> </div>'
# - <script src="xxxx"></script>

```


## 14. 背景美化


```
# Mouse click effects: fireworks (鼠標點擊效果: 煙火特效)
fireworks:
  enable: true
  zIndex: 9999 # -1 or 9999
  mobile: false

# Typewriter Effect (打字效果)
# https://github.com/disjukr/activate-power-mode
activate_power_mode:
  enable: true
  colorful: true # open particle animation (冒光特效)
  shake: false #  open shake (抖動特效)
  mobile: true

# canvas_nest
# https://github.com/hustcc/canvas-nest.js
canvas_nest:
  enable: true
  color: '0,0,255' #color of lines, default: '0,0,0'; RGB values: (R,G,B).(note: use ',' to separate.)
  opacity: 0.7 # the opacity of line (0~1), default: 0.5.
  zIndex: -1 # z-index property of the background, default: -1.
  count: 99 # the number of lines, default: 99.
  mobile: false

```
