#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hexo 博客文章抓取工具
从网站抓取文章并生成正确的 markdown 文件
"""

import requests
from bs4 import BeautifulSoup
import re
import os
import time
from urllib.parse import urljoin, unquote

# 配置
BASE_URL = "https://yangcheneee.github.io"
OUTPUT_DIR = "source/_posts"
IMG_DIR = "img"

# 抓取文章列表
def get_article_list():
    articles = []
    seen_urls = set()
    page = 1
    while True:
        if page == 1:
            url = f"{BASE_URL}/archives/"
        else:
            url = f"{BASE_URL}/archives/page/{page}/"
        
        print(f"正在抓取文章列表: {url}")
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            break
        
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # 查找所有文章链接
        links = soup.find_all('a', href=re.compile(r'^/posts/'))
        
        if not links:
            break
        
        found_new = False
        for link in links:
            href = link.get('href')
            if href and href not in seen_urls:
                seen_urls.add(href)
                full_url = urljoin(BASE_URL, href)
                title = link.get_text(strip=True)
                if not title or title == '无题':
                    # 从URL提取标题
                    title = href.split('/posts/')[-1].strip('/')
                    title = unquote(title).replace('-', ' ').replace('_', ' ')
                if title:
                    articles.append({
                        'url': full_url,
                        'title': title
                    })
                    found_new = True
        
        if not found_new:
            break
            
        page += 1
        time.sleep(1)
    
    return articles

# 抓取单篇文章
def fetch_article(url):
    resp = requests.get(url, timeout=10)
    if resp.status_code != 200:
        return None
    
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    # 提取标题
    title = soup.select_one('.post-title') or soup.select_one('.article-title')
    title_text = title.get_text(strip=True) if title else ''
    
    # 提取日期
    date_elem = soup.select_one('time')
    date = date_elem.get('datetime', '') if date_elem else ''
    
    # 提取分类
    categories = []
    cat_links = soup.select('.post-meta__categories') or soup.select('.article-category a')
    for cat in cat_links:
        categories.append(cat.get_text(strip=True))
    
    # 提取标签
    tags = []
    tag_links = soup.select('.post-meta__tags') or soup.select('.article-tag a')
    for tag in tag_links:
        tags.append(tag.get_text(strip=True))
    
    # 提取文章内容
    content = soup.select_one('#article-container')
    
    # 提取图片（从 data-lazy-src 中获取真正的图片URL）
    images = []
    if content:
        for img in content.find_all('img'):
            src = img.get('data-lazy-src') or img.get('data-src') or img.get('src', '')
            if src and not src.startswith('data:'):
                full_src = urljoin(BASE_URL, src)
                images.append(full_src)
                # 替换为正确的markdown格式
                img['src'] = src
                if 'data-lazy-src' in img.attrs:
                    del img['data-lazy-src']
                if 'data-src' in img.attrs:
                    del img['data-src']
    
    # 转换为markdown
    markdown_content = html_to_markdown(content) if content else ''
    
    return {
        'title': title_text,
        'date': date[:10] if date else '',
        'categories': categories,
        'tags': tags,
        'content': markdown_content,
        'images': images
    }

# HTML转Markdown
def html_to_markdown(element):
    if element is None:
        return ''
    
    markdown = []
    
    for child in element.children:
        if child.name == 'p':
            markdown.append(p_to_markdown(child))
        elif child.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            level = int(child.name[1])
            markdown.append(f"\n{'#' * level} {child.get_text(strip=True)}\n")
        elif child.name == 'pre':
            code = child.select_one('code')
            lang = ''
            if code:
                lang = code.get('class', [''])[0].replace('language-', '') if code.get('class') else ''
                text = code.get_text()
            else:
                text = child.get_text()
            markdown.append(f"\n```{lang}\n{text}\n```\n")
        elif child.name == 'ul':
            markdown.append(ul_to_markdown(child))
        elif child.name == 'ol':
            markdown.append(ol_to_markdown(child))
        elif child.name == 'blockquote':
            text = child.get_text(strip=True)
            markdown.append(f"\n> {text}\n")
        elif child.name == 'img':
            src = child.get('src', '')
            alt = child.get('alt', '')
            markdown.append(f"![{alt}]({src})")
        elif child.name == 'table':
            markdown.append(table_to_markdown(child))
        elif hasattr(child, 'get_text'):
            text = child.get_text(strip=True)
            if text:
                markdown.append(text)
    
    return '\n'.join(markdown)

def p_to_markdown(p):
    parts = []
    for child in p.children:
        if child.name == 'img':
            src = child.get('src', '')
            alt = child.get('alt', '')
            parts.append(f"![{alt}]({src})")
        elif child.name == 'a':
            href = child.get('href', '')
            text = child.get_text(strip=True)
            parts.append(f"[{text}]({href})")
        elif child.name == 'code':
            parts.append(f"`{child.get_text()}`")
        elif child.name == 'strong' or child.name == 'b':
            parts.append(f"**{child.get_text(strip=True)}**")
        elif child.name == 'em' or child.name == 'i':
            parts.append(f"*{child.get_text(strip=True)}*")
        elif hasattr(child, 'get_text'):
            parts.append(child.get_text())
        else:
            parts.append(str(child))
    return ''.join(parts)

def ul_to_markdown(ul, level=0):
    items = []
    for li in ul.find_all('li', recursive=False):
        text = li.get_text(strip=True)
        items.append(f"{'  ' * level}- {text}")
        nested = li.find(['ul', 'ol'])
        if nested:
            items.append(ul_to_markdown(nested, level + 1))
    return '\n'.join(items)

def ol_to_markdown(ol, level=0):
    items = []
    for i, li in enumerate(ol.find_all('li', recursive=False), 1):
        text = li.get_text(strip=True)
        items.append(f"{'  ' * level}{i}. {text}")
    return '\n'.join(items)

def table_to_markdown(table):
    rows = []
    for tr in table.find_all('tr'):
        cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
        rows.append('| ' + ' | '.join(cells) + ' |')
    
    if len(rows) > 1:
        separator = '| ' + ' | '.join(['---'] * len(rows[0].split('|')[1:-1])) + ' |'
        rows.insert(1, separator)
    
    return '\n'.join(rows)

# 保存文章
def save_article(article, slug):
    # 生成 front-matter
    front_matter = "---\n"
    front_matter += f"title: {article['title']}\n"
    front_matter += f"date: {article['date']}\n"
    
    if article['categories']:
        front_matter += "categories:\n"
        for cat in article['categories']:
            front_matter += f"  - {cat}\n"
    
    if article['tags']:
        front_matter += "tags:\n"
        for tag in article['tags']:
            front_matter += f"  - {tag}\n"
    
    front_matter += "---\n\n"
    
    # 保存文件
    filename = f"{slug}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(front_matter)
        f.write(article['content'])
    
    print(f"已保存: {filepath}")
    return filepath

# 下载图片
def download_images(images, slug):
    for img_url in images:
        try:
            resp = requests.get(img_url, timeout=10)
            if resp.status_code == 200:
                # 从URL提取文件名
                filename = img_url.split('/')[-1]
                filepath = os.path.join(IMG_DIR, filename)
                
                os.makedirs(IMG_DIR, exist_ok=True)
                with open(filepath, 'wb') as f:
                    f.write(resp.content)
                print(f"已下载图片: {filepath}")
        except Exception as e:
            print(f"下载图片失败 {img_url}: {e}")

# 主函数
def main():
    print("开始抓取文章...")
    
    # 创建输出目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(IMG_DIR, exist_ok=True)
    
    # 获取文章列表
    articles = get_article_list()
    print(f"找到 {len(articles)} 篇文章")
    
    # 抓取每篇文章
    for i, article_info in enumerate(articles, 1):
        print(f"\n[{i}/{len(articles)}] 正在抓取: {article_info['title']}")
        
        article = fetch_article(article_info['url'])
        if article:
            # 生成slug
            slug = article_info['url'].split('/posts/')[-1].strip('/')
            slug = unquote(slug).replace(' ', '-')
            
            # 保存文章
            save_article(article, slug)
            
            # 下载图片
            if article['images']:
                download_images(article['images'], slug)
            
            time.sleep(1)  # 避免请求过快
    
    print("\n抓取完成！")

if __name__ == '__main__':
    main()
