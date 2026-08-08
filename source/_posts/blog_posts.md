---
title: 博客（四）：优雅的写一篇文章
date: 2023-09-07
categories:
  - 博客
tags:
  - 博客
  - Hexo
  - Butterfly
  - VScode
  - MarkDown
---


*你需要先了解…*
*有关此文章…*

# 一. MarkDown/MD基础

如果你需要向博客上传文章，将MD文档放置到blog/hexo/source/_posts目录下即可。
类似于WORD文档，MD同样适用于写作和笔记。MD依赖于键盘输入控制文章的排版格式，不需要鼠标意味着你能拥抱更快的写作速度。不必担心的是，MD比WORD要简单的多。
如果你需要学习，下面是一些MarkDown语法。

## 1. 标题


```
# 一级标题

```


# 一级标题


```
## 二级标题

```


## 二级标题


```
### 三级标题

```


### 三级标题


```
#### 四级标题

```


#### 四级标题


```
##### 五级标题

```


##### 五级标题


```
###### 六级标题

```


###### 六级标题


## 2. 正文

正文

```
正文

```

**加粗**

```
**加粗**

```

*斜体*

```
*斜体*

```

*加粗&斜体*

```
***加粗&斜体***

```


## 3. 图片&链接


### 图片

复制图片以后在文档的合适位置粘贴。
![Alt text](/img/blog_posts/1694181786100.jpeg)
当然你可以更改括号中的图片位置，MD文件会识别同目录下的图片。
如果你把这些图片放在下层的一个目录进行收录，那么请更改括号中的路径。
另外，你也可以在括号中放置图片的网页链接。

### 链接

[百度](https://www.baidu.com/)

```
[百度](https://www.baidu.com/)

```


## 4. 代码


```Python
    print(Hello MarkDown!)

```


```
```Python
    print(Hello MarkDown!)
```

```

你可以在 **```** 后面指定代码所使用的语言，当然也可以不指定。

# 二. MarkDown美化

butterfly提供了MD的额外样式。你可以引用这些标注放在MD文档的开头。
下面是本篇文章的头：

```
---
title: 博客：优雅的写一篇文章
date: 2023-9-8
updated:
tags: [博客,hexo,butterfly,md]
categories: 博客
keywords:
description:
top_img: /img/cover/0.jpg
comments:
cover: /img/cover/0.jpg
toc:
toc_number:
toc_style_simple:
copyright:
copyright_author:
copyright_author_href:
copyright_url:
copyright_info:
mathjax:
katex:
aplayer:
highlight_shrink:
aside:
abcjs:
---

```

你可以通过网络了解其他标注的作用。

# 三. 问题？


## 1. MD文档中的图片放置？

当你向MD文件中复制一张图片时，这张图片会被复制到MD的同级目录下。
建议你在目录blog\hexo\source\img\xxx下存放你的文章xxx，同时更改MD文件中的图片路径。

```
![Alt text](img/xxx/liangyue.jpg)

```

*Tips：*
更换大量图片路径是枯燥且费时的。
如果你使用VSCode编辑MD，那么使用’Ctrl+F’对图片路径进行批量更换是个不错的方法。

## 2. 博客文章的封面图片？

你可以将封面图片放置在以下目录：blog\hexo\themes\butterfly\source\img
然后在MD文件中更改以下配置

```
top_img: /img/xxx.jpg
cover: /img/xxx.jpg

```

里面存放了一些网页配置的图片：网站背景图片；头像；404页面；默认顶图。
如果可以，建议你新建一个cover目录，保存封面图片。然后更改一下路径

```
top_img: /img/cover/0.jpg
cover: /img/cover/0.jpg

```


## 3. MD侧边预览

如果你使用VScode编辑MD，右上角打开侧边预览
![Alt text](/img/blog_posts/image.png)

## 4. 如果你有任何问题？

欢迎你给我留言
同时希望你能通过搜索引擎和GPT解决大部分问题