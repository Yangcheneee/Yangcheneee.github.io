#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
只补全分类信息
"""
import requests
from bs4 import BeautifulSoup
import os
import re
import time

BASE_URL = "https://yangcheneee.github.io"
POSTS_DIR = "source/_posts"

def get_article_list():
    articles = []
    page = 1
    while True:
        if page == 1:
            url = f"{BASE_URL}/archives/"
        else:
            url = f"{BASE_URL}/archives/page/{page}/"
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            break
        soup = BeautifulSoup(resp.text, 'html.parser')
        links = soup.find_all('a', href=re.compile(r'^/posts/'))
        if not links:
            break
        found_new = False
        for link in links:
            href = link.get('href')
            if href:
                full_url = BASE_URL + href
                slug = href.split('/posts/')[-1].strip('/')
                articles.append({'url': full_url, 'slug': slug})
                found_new = True
        if not found_new:
            break
        page += 1
    return articles

def fetch_categories(url):
    resp = requests.get(url, timeout=10)
    if resp.status_code != 200:
        return []
    soup = BeautifulSoup(resp.text, 'html.parser')
    cats = []
    for cat in soup.select('.post-meta-categories'):
        cats.append(cat.get_text(strip=True))
    return cats

def slug_to_filename(slug):
    from urllib.parse import unquote
    name = unquote(slug).strip()
    name = re.sub(r'\s+', ' ', name)
    if name.startswith('Lin et al'):
        return 'Lin-et-al_2024_Research-on-Security-Protection-Evasion-Mechanism-Based-on-IPv6-Fragment-Headers.md'
    mapping = {
        'cpp': 'cpp.md',
        'computer_encode': 'computer_encode.md',
        'network-IPv6': 'network-IPv6.md',
        'security_information': 'security_information.md',
    }
    if name in mapping:
        return mapping[name]
    safe = name.replace('/', '-')
    return safe + '.md'

def update_post(filepath, categories):
    if not os.path.exists(filepath):
        return False
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if not content.startswith('---'):
        return False
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        return False
    
    fm = parts[1]
    body = parts[2]
    
    lines = fm.split('\n')
    new_lines = []
    skip_next = False
    for i, line in enumerate(lines):
        if skip_next:
            skip_next = False
            continue
        if line.strip().startswith('tags:'):
            new_lines.append(line)
            j = i + 1
            while j < len(lines) and (lines[j].startswith('  -') or lines[j].strip() == ''):
                j += 1
            i = j - 1
            if categories:
                for cat in categories:
                    new_lines.append(f'  - {cat}')
            continue
        new_lines.append(line)
    
    if categories:
        for cat in categories:
            new_lines.append(f'categories:')
            new_lines.append(f'  - {cat}')
            break
    
    new_fm = '\n'.join(new_lines)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('---' + new_fm + '---' + body)
    
    return True

def main():
    articles = get_article_list()
    print(f'找到 {len(articles)} 篇文章')
    
    for i, art in enumerate(articles, 1):
        cats = fetch_categories(art['url'])
        filename = slug_to_filename(art['slug'])
        filepath = os.path.join(POSTS_DIR, filename)
        
        if update_post(filepath, cats):
            cats_str = ', '.join(cats) if cats else '无'
            print(f'[{i}/{len(articles)}] {filename}: {cats_str}')
        else:
            print(f'[{i}/{len(articles)}] {filename}: 文件不存在')
        
        time.sleep(0.3)
    
    print('完成!')

if __name__ == '__main__':
    main()
