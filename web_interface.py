#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 API Documentation Parser - Web Interface
===========================================
Веб-интерфейс для загрузки и обработки PDF документации API

Features:
- Drag & Drop загрузка PDF
- Прогресс обработки в реальном времени
- Интерактивное отображение результатов
- Экспорт в различных форматах
"""

import os
import json
import tempfile
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Конфигурация
UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'
ALLOWED_EXTENSIONS = {'pdf'}

# Создаем необходимые папки
for folder in [UPLOAD_FOLDER, RESULTS_FOLDER]:
    Path(folder).mkdir(exist_ok=True)

def allowed_file(filename: str) -> bool:
    """Проверка допустимости файла"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_size(file_path: str) -> str:
    """Получение размера файла в читаемом формате"""
    size = os.path.getsize(file_path)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"

def run_parser(pdf_path: str) -> Dict[str, Any]:
    """Запуск парсера и получение результатов"""
    try:
        # Копируем PDF в рабочую директорию как documentation.pdf
        import shutil
        import os
        shutil.copy2(pdf_path, 'documentation.pdf')
        
        # Удаляем кэшированные файлы для корректной обработки нового PDF
        cache_files = ['extracted_text.txt', 'ultimate_final_data/']
        for cache_file in cache_files:
            if os.path.exists(cache_file):
                if os.path.isfile(cache_file):
                    os.remove(cache_file)
                elif os.path.isdir(cache_file):
                    shutil.rmtree(cache_file)
        
        # Запускаем парсер
        result = subprocess.run(
            ['python3', 'fleethand_ultimate_parser.py'],
            capture_output=True,
            text=True,
            timeout=300  # 5 минут таймаут
        )
        
        if result.returncode == 0:
            # Читаем результаты
            results_dir = Path('ultimate_final_data')
            if results_dir.exists():
                results = {}
                
                # Читаем все JSON файлы из результатов
                for json_file in results_dir.glob('*.json'):
                    with open(json_file, 'r', encoding='utf-8') as f:
                        results[json_file.stem] = json.load(f)
                
                return {
                    'success': True,
                    'results': results,
                    'stdout': result.stdout,
                    'stderr': result.stderr
                }
            else:
                return {
                    'success': False,
                    'error': 'Результаты не найдены',
                    'stdout': result.stdout,
                    'stderr': result.stderr
                }
        else:
            return {
                'success': False,
                'error': f'Ошибка парсера (код: {result.returncode})',
                'stdout': result.stdout,
                'stderr': result.stderr
            }
            
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'error': 'Тайм-аут обработки (превышено 5 минут)'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Неожиданная ошибка: {str(e)}'
        }

@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Загрузка и обработка PDF файла"""
    if 'file' not in request.files:
        flash('Файл не выбран')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('Файл не выбран')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        # Информация о файле
        file_info = {
            'name': filename,
            'size': get_file_size(file_path),
            'upload_time': datetime.now().isoformat()
        }
        
        return jsonify({
            'success': True,
            'message': 'Файл успешно загружен, начинаем обработку...',
            'file_info': file_info,
            'processing_url': url_for('process_file', filename=filename)
        })
    
    else:
        flash('Недопустимый тип файла. Поддерживаются только PDF файлы.')
        return redirect(url_for('index'))

@app.route('/process/<filename>')
def process_file(filename: str):
    """Обработка загруженного файла"""
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    
    if not os.path.exists(file_path):
        return jsonify({'success': False, 'error': 'Файл не найден'})
    
    # Запускаем парсинг
    results = run_parser(file_path)
    
    if results['success']:
        # Сохраняем результаты
        results_file = os.path.join(RESULTS_FOLDER, f"{filename}_results.json")
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        return jsonify({
            'success': True,
            'message': 'Обработка завершена успешно!',
            'results': results['results'],
            'download_url': url_for('download_results', filename=f"{filename}_results.json")
        })
    else:
        return jsonify({
            'success': False,
            'error': results.get('error', 'Неизвестная ошибка'),
            'details': {
                'stdout': results.get('stdout', ''),
                'stderr': results.get('stderr', '')
            }
        })

@app.route('/download/<filename>')
def download_results(filename: str):
    """Скачивание результатов"""
    file_path = os.path.join(RESULTS_FOLDER, filename)
    
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({'error': 'Файл не найден'}), 404

@app.route('/api/status')
def api_status():
    """API статус сервиса"""
    return jsonify({
        'status': 'active',
        'version': '1.0.0',
        'features': [
            'PDF parsing',
            'MCP server generation', 
            'Quality reporting',
            'Multi-format export'
        ],
        'supported_formats': ['PDF'],
        'max_file_size': '50MB'
    })

@app.errorhandler(413)
def too_large(e):
    """Обработка слишком больших файлов"""
    return jsonify({'error': 'Файл слишком большой. Максимальный размер: 50MB'}), 413

@app.errorhandler(500)
def internal_error(e):
    """Обработка внутренних ошибок"""
    return jsonify({'error': 'Внутренняя ошибка сервера'}), 500

if __name__ == '__main__':
    print("🚀 Запуск API Documentation Parser Web Interface...")
    print("📂 Uploads folder:", UPLOAD_FOLDER)
    print("📊 Results folder:", RESULTS_FOLDER)
    print("🌐 Откройте: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=9000)