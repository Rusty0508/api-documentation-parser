#!/usr/bin/env python3
"""
Enhanced API Endpoints Extractor for Fleethand Documentation
Специально настроен под формат Fleethand API документации
"""

import re
import json
import csv
import os
from typing import Dict, List, Any
from datetime import datetime

class FleethandEndpointExtractor:
    def __init__(self, text_file='extracted_text.txt'):
        self.text_file = text_file
        self.text = self.load_text()
        
        # Создаем папку для результатов
        self.output_dir = 'fleethand_endpoints'
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.endpoints = []
        
    def load_text(self):
        """Загружаем текст документации"""
        with open(self.text_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    def extract_endpoints_by_pattern(self):
        """Извлекаем endpoints по специальному паттерну Fleethand"""
        print("🔍 Ищем endpoints в формате Fleethand...")
        
        # Паттерн: Method \n URL \n METHOD \n /api/path
        pattern = r'Method\s*\n\s*URL\s*\n\s*(GET|POST|PUT|DELETE|PATCH)\s*\n\s*(/api/[^\s\n]+)'
        
        for match in re.finditer(pattern, self.text, re.MULTILINE):
            method = match.group(1)
            path = match.group(2)
            
            # Получаем больше контекста
            start = max(0, match.start() - 1000)
            end = min(len(self.text), match.end() + 3000)
            context = self.text[start:end]
            
            endpoint_data = {
                'id': f"{method}_{path.replace('/', '_')}",
                'method': method,
                'path': path,
                'category': self.detect_category(path),
                'description': self.extract_description(context),
                'parameters': self.extract_parameters(context),
                'request_body': self.extract_request_body(context),
                'response': self.extract_response(context),
                'auth_required': True,  # Все Fleethand endpoints требуют авторизации
                'full_context': context[:2000]  # Сохраняем контекст для анализа
            }
            
            self.endpoints.append(endpoint_data)
        
        print(f"   ✅ Найдено {len(self.endpoints)} endpoints")
    
    def detect_category(self, path):
        """Определяем категорию по пути"""
        categories = {
            'activities': ['activities', 'activity'],
            'drivers': ['drivers', 'driver'],
            'vehicles': ['vehicles', 'vehicle', 'fleet'],
            'reports': ['reports', 'report', 'eco'],
            'tasks': ['tasks', 'task'],
            'fuel': ['fuel', 'refuel'],
            'maintenance': ['maintenance', 'service'],
            'locations': ['locations', 'position', 'gps'],
            'documents': ['documents', 'files', 'attachments'],
            'partners': ['partners', 'partner', 'client'],
            'users': ['users', 'user'],
            'settings': ['settings', 'config']
        }
        
        path_lower = path.lower()
        for category, keywords in categories.items():
            if any(keyword in path_lower for keyword in keywords):
                return category
        return 'general'
    
    def extract_description(self, context):
        """Извлекаем описание endpoint"""
        # Ищем описание перед Method
        desc_patterns = [
            r'([^\n]+)\s*\n\s*Method',
            r'Description[:\s]*([^\n]+)',
            r'Purpose[:\s]*([^\n]+)'
        ]
        
        for pattern in desc_patterns:
            match = re.search(pattern, context, re.IGNORECASE)
            if match:
                desc = match.group(1).strip()
                if len(desc) > 10 and len(desc) < 200:
                    return desc
        
        return "API endpoint"
    
    def extract_parameters(self, context):
        """Извлекаем параметры из контекста"""
        parameters = []
        
        # Ищем секцию Parameters
        param_section_match = re.search(
            r'Parameters?[:\s]*\n(.*?)(?:\n\n|Response|Example|$)',
            context, re.IGNORECASE | re.DOTALL
        )
        
        if param_section_match:
            param_text = param_section_match.group(1)
            
            # Ищем параметры в формате: name - description
            param_matches = re.findall(r'(\w+)\s*[-–:]\s*(.+?)(?:\n|$)', param_text)
            
            for param_name, param_desc in param_matches:
                parameters.append({
                    'name': param_name,
                    'description': param_desc.strip(),
                    'type': self.detect_param_type(param_desc),
                    'required': 'required' in param_desc.lower()
                })
        
        return parameters
    
    def detect_param_type(self, description):
        """Определяем тип параметра по описанию"""
        desc_lower = description.lower()
        
        if 'id' in desc_lower or 'uuid' in desc_lower:
            return 'string'
        elif 'date' in desc_lower or 'time' in desc_lower:
            return 'datetime'
        elif 'number' in desc_lower or 'integer' in desc_lower:
            return 'integer'
        elif 'boolean' in desc_lower or 'true/false' in desc_lower:
            return 'boolean'
        elif 'array' in desc_lower or 'list' in desc_lower:
            return 'array'
        else:
            return 'string'
    
    def extract_request_body(self, context):
        """Извлекаем структуру тела запроса"""
        # Ищем JSON структуры в контексте
        json_matches = re.findall(r'\{[^{}]*\}', context)
        
        if json_matches:
            # Берем самую большую JSON структуру
            largest_json = max(json_matches, key=len)
            try:
                # Пытаемся распарсить как валидный JSON
                return json.loads(largest_json)
            except:
                return largest_json
        
        return None
    
    def extract_response(self, context):
        """Извлекаем пример ответа"""
        # Ищем секцию Response
        response_match = re.search(
            r'Response[:\s]*\n(.*?)(?:\n\n|Parameters|Example|$)',
            context, re.IGNORECASE | re.DOTALL
        )
        
        if response_match:
            response_text = response_match.group(1)
            
            # Ищем JSON в ответе
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except:
                    return json_match.group()
        
        return None
    
    def save_results(self):
        """Сохраняем результаты в разных форматах"""
        print("💾 Сохраняем результаты...")
        
        # JSON для программного использования
        json_path = os.path.join(self.output_dir, 'endpoints.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.endpoints, f, indent=2, ensure_ascii=False)
        
        # CSV для импорта в базы данных
        csv_path = os.path.join(self.output_dir, 'endpoints.csv')
        if self.endpoints:
            fieldnames = ['id', 'method', 'path', 'category', 'description', 'parameters']
            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for endpoint in self.endpoints:
                    csv_row = {
                        'id': endpoint['id'],
                        'method': endpoint['method'],
                        'path': endpoint['path'],
                        'category': endpoint['category'],
                        'description': endpoint['description'],
                        'parameters': json.dumps(endpoint['parameters'])
                    }
                    writer.writerow(csv_row)
        
        # Markdown документация
        md_path = os.path.join(self.output_dir, 'API_ENDPOINTS.md')
        self.generate_markdown_docs(md_path)
        
        # Статистика
        stats_path = os.path.join(self.output_dir, 'statistics.json')
        with open(stats_path, 'w', encoding='utf-8') as f:
            json.dump(self.generate_statistics(), f, indent=2)
        
        print(f"✅ Результаты сохранены в {self.output_dir}/")
        print(f"   • endpoints.json - {len(self.endpoints)} endpoints")
        print(f"   • endpoints.csv - табличный формат")
        print(f"   • API_ENDPOINTS.md - документация")
        print(f"   • statistics.json - статистика")
    
    def generate_markdown_docs(self, output_path):
        """Генерируем Markdown документацию"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Fleethand API Endpoints\n\n")
            f.write(f"Сгенерировано: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Всего endpoints: {len(self.endpoints)}\n\n")
            
            # Группируем по категориям
            categories = {}
            for endpoint in self.endpoints:
                cat = endpoint['category']
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append(endpoint)
            
            # Генерируем документацию по категориям
            for category, endpoints in sorted(categories.items()):
                f.write(f"## {category.title()}\n\n")
                
                for endpoint in endpoints:
                    f.write(f"### {endpoint['method']} {endpoint['path']}\n\n")
                    f.write(f"**Описание:** {endpoint['description']}\n\n")
                    
                    if endpoint['parameters']:
                        f.write("**Параметры:**\n")
                        for param in endpoint['parameters']:
                            f.write(f"- `{param['name']}` ({param['type']}) - {param['description']}\n")
                        f.write("\n")
                    
                    f.write("---\n\n")
    
    def generate_statistics(self):
        """Генерируем статистику"""
        categories = {}
        methods = {}
        
        for endpoint in self.endpoints:
            # Статистика по категориям
            cat = endpoint['category']
            categories[cat] = categories.get(cat, 0) + 1
            
            # Статистика по методам
            method = endpoint['method']
            methods[method] = methods.get(method, 0) + 1
        
        return {
            'total_endpoints': len(self.endpoints),
            'categories': categories,
            'methods': methods,
            'generated_at': datetime.now().isoformat()
        }
    
    def run(self):
        """Запускаем полный процесс извлечения"""
        print("🚀 Запускаем извлечение Fleethand API endpoints...")
        print("=" * 60)
        
        # Извлекаем endpoints
        self.extract_endpoints_by_pattern()
        
        if self.endpoints:
            # Сохраняем результаты
            self.save_results()
            
            # Выводим краткую статистику
            stats = self.generate_statistics()
            print("\n📊 Статистика:")
            print(f"   • Всего endpoints: {stats['total_endpoints']}")
            print(f"   • Категории: {list(stats['categories'].keys())}")
            print(f"   • Методы: {stats['methods']}")
        else:
            print("❌ Endpoints не найдены")
        
        print("=" * 60)
        return self.output_dir

if __name__ == "__main__":
    extractor = FleethandEndpointExtractor('extracted_text.txt')
    extractor.run()