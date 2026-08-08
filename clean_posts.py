#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理文章的 front-matter
"""
import os
import re

POSTS_DIR = "source/_posts"

def clean_post(filepath):
    if not os.path.exists(filepath):
        return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if not content.startswith('---'):
        return
    
    # 找到 front-matter 的结束
    end = content.find('---', 3)
    if end < 0:
        return
    
    fm = content[3:end]
    body = content[end+3:]
    
    # 解析 fields
    title = ''
    date = ''
    tags = []
    categories = []
    
    lines = fm.strip().split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('title:'):
            title = line[6:].strip()
        elif line.startswith('date:'):
            date = line[5:].strip()
        elif line.strip() == 'tags:':
            i += 1
            while i < len(lines) and (lines[i].startswith('  -') or lines[i].strip() == ''):
                if lines[i].startswith('  -'):
                    tag = lines[i][3:].strip()
                    tag = re.sub(r'^\|', '', tag).strip()
                    if tag and tag not in tags:
                        tags.append(tag)
                i += 1
            continue
        elif line.strip() == 'categories:':
            i += 1
            while i < len(lines) and (lines[i].startswith('  -') or lines[i].strip() == ''):
                if lines[i].startswith('  -'):
                    cat = lines[i][3:].strip()
                    cat = re.sub(r'^\|', '', cat).strip()
                    if cat and cat not in categories:
                        categories.append(cat)
                i += 1
            continue
        i += 1
    
    new_fm = '---\n'
    new_fm += f'title: {title}\n'
    new_fm += f'date: {date}\n'
    if categories:
        new_fm += 'categories:\n'
        for c in categories:
            new_fm += f'  - {c}\n'
    if tags:
        new_fm += 'tags:\n'
        for t in tags:
            new_fm += f'  - {t}\n'
    new_fm += '---\n'
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_fm + body)
    
    print(f'清理: {os.path.basename(filepath)}')

def main():
    for f in os.listdir(POSTS_DIR):
        if f.endswith('.md'):
            clean_post(os.path.join(POSTS_DIR, f))
    print('完成!')

if __name__ == '__main__':
    main()
