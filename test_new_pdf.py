#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Тест обработки нового PDF файла
==================================
Тестирует корректность обработки загруженного пользователем PDF
"""

import os
import shutil
import subprocess
import json
from pathlib import Path

def test_pdf_processing():
    """Тестирует полную обработку нового PDF"""
    
    print("🧪 ТЕСТИРОВАНИЕ ОБРАБОТКИ НОВОГО PDF")
    print("=" * 50)
    
    # Проверяем загруженный файл
    uploaded_pdf = "uploads/20250904_130609_LocTracker_Field_Service_Integration_REST_v1.0.34_1.pdf"
    
    if not os.path.exists(uploaded_pdf):
        print("❌ Загруженный PDF не найден!")
        return False
    
    print(f"✅ Найден загруженный PDF: {os.path.basename(uploaded_pdf)}")
    print(f"📊 Размер: {os.path.getsize(uploaded_pdf)} bytes")
    
    # Очищаем кэш и копируем новый PDF
    print("\n🗑️ Очистка кэша...")
    cache_files = ['extracted_text.txt', 'ultimate_final_data']
    for cache_file in cache_files:
        if os.path.exists(cache_file):
            if os.path.isfile(cache_file):
                os.remove(cache_file)
                print(f"   Удален: {cache_file}")
            elif os.path.isdir(cache_file):
                shutil.rmtree(cache_file)
                print(f"   Удалена папка: {cache_file}")
    
    # Копируем новый PDF
    print(f"\n📄 Копирование нового PDF...")
    shutil.copy2(uploaded_pdf, 'documentation.pdf')
    print(f"   Скопирован: {uploaded_pdf} -> documentation.pdf")
    
    # Запускаем парсер
    print(f"\n🚀 Запуск парсера...")
    result = subprocess.run(
        ['python3', 'fleethand_ultimate_parser.py'],
        capture_output=True,
        text=True,
        timeout=300
    )
    
    if result.returncode == 0:
        print("✅ Парсер выполнился успешно!")
        
        # Проверяем результаты
        results_dir = Path('ultimate_final_data')
        if results_dir.exists():
            quality_file = results_dir / 'quality_report_ultimate_final.json'
            if quality_file.exists():
                with open(quality_file, 'r') as f:
                    quality_data = json.load(f)
                
                stats = quality_data['statistics']
                metrics = quality_data['quality_metrics']
                
                print(f"\n📊 РЕЗУЛЬТАТЫ ОБРАБОТКИ:")
                print(f"   Endpoints: {stats['endpoints']}")
                print(f"   Headers: {stats['headers']}")
                print(f"   Parameters: {stats['parameters']}")
                print(f"   Responses: {stats['responses']}")
                print(f"   MCP готовность: {metrics['mcp_readiness_score']}")
                print(f"   Качество: {metrics['professional_quality']}")
                
                # Проверяем время генерации
                gen_time = quality_data['generation_time']
                print(f"   Время генерации: {gen_time}")
                
                return True
            else:
                print("❌ Отчет о качестве не найден!")
        else:
            print("❌ Папка результатов не найдена!")
    else:
        print("❌ Ошибка выполнения парсера:")
        print(f"   stdout: {result.stdout}")
        print(f"   stderr: {result.stderr}")
    
    return False

if __name__ == "__main__":
    success = test_pdf_processing()
    if success:
        print("\n🎉 ТЕСТ ПРОЙДЕН! Новый PDF корректно обрабатывается.")
    else:
        print("\n❌ ТЕСТ НЕ ПРОЙДЕН! Требуется отладка.")