#!/usr/bin/env python3

import re
import json

# Читаем текст и делаем то же самое, что в парсере
with open('extracted_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Найдем первую секцию endpoint для тестирования  
method_urls = re.findall(r'(GET|POST|PUT|DELETE)\s+(\S+)', text)
print(f"Найдено {len(method_urls)} method/url пар")

# Возьмем первую секцию
method, url = method_urls[0]
print(f"Тестируем: {method} {url}")

# Найдем эту секцию в тексте
pattern = rf'\b{re.escape(method)}\s+{re.escape(url)}\b'
match = re.search(pattern, text)

if match:
    start_pos = match.start()
    
    # Определим границы секции (ищем следующий Method или конец)
    next_method_pattern = r'\n(?:GET|POST|PUT|DELETE)\s+\S+'
    next_match = re.search(next_method_pattern, text[start_pos + len(match.group()):])
    
    if next_match:
        end_pos = start_pos + len(match.group()) + next_match.start()
    else:
        end_pos = len(text)
    
    section = text[start_pos:end_pos]
    print(f"Длина секции: {len(section)}")
    
    # Теперь ищем Response example в этой секции
    response_sections = re.findall(r'Response example\s*\n(.*?)(?=\n\n|\Z)', section, re.DOTALL)
    print(f"Найдено {len(response_sections)} response example в секции")
    
    if response_sections:
        print("Первый Response example:")
        print(repr(response_sections[0][:300]))
    
    # Проверим также полный поиск по всему тексту
    all_responses = re.findall(r'Response example\s*\n(.*?)(?=\n\n|\Z)', text, re.DOTALL)
    print(f"Всего Response example в тексте: {len(all_responses)}")