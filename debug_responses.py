#!/usr/bin/env python3

import re

# Читаем текст
with open('extracted_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Ищем все секции Response example
sections = re.findall(r'Response example\s*\n(.*?)(?=\n\n|\Z)', text, re.DOTALL)

print(f"Найдено {len(sections)} секций Response example")

for i, section in enumerate(sections[:5]):
    print(f"\n=== Секция {i+1} ===")
    print(repr(section[:200]))
    print("---")
    print(section[:200])