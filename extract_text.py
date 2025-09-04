#!/usr/bin/env python3
"""
Извлекаем текст из PDF и сохраняем
"""

import fitz

def extract_text():
    doc = fitz.open('documentation.pdf')
    text = ""
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += f"\n=== Страница {page_num + 1} ===\n"
        text += page.get_text()
    
    doc.close()
    
    with open('extracted_text.txt', 'w', encoding='utf-8') as f:
        f.write(text)
    
    print(f"Извлечено {len(text)} символов")
    print("Сохранено в extracted_text.txt")

if __name__ == "__main__":
    extract_text()