#!/usr/bin/env python3
"""
Smart Knowledge Base Extractor
Извлекает ВСЕ типы знаний из документации и создает отдельные структурированные файлы
"""

import re
import json
import csv
from typing import Dict, List, Any
from datetime import datetime
import os

class SmartKnowledgeExtractor:
    def __init__(self, text_file='extracted_text.txt'):
        self.text_file = text_file
        self.text = self.load_text()
        
        # Создаем папку для всех баз знаний
        self.output_dir = 'fleethand_knowledge_bases'
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Инициализируем все базы знаний
        self.knowledge_bases = {
            'endpoints': [],         # Все API endpoints
            'models': [],           # Модели данных и схемы
            'parameters': [],       # Все параметры детально
            'examples': [],         # Примеры кода и запросов
            'errors': [],          # Коды ошибок и их решения
            'auth': [],            # Методы авторизации
            'webhooks': [],        # Webhook события
            'rate_limits': [],     # Ограничения и лимиты
            'business_rules': [],  # Бизнес-правила и логика
            'glossary': [],        # Словарь терминов
            'workflows': [],       # Типичные сценарии использования
            'integrations': [],    # Интеграции с другими системами
            'permissions': [],     # Роли и разрешения
            'data_types': [],      # Типы данных и форматы
            'validations': []      # Правила валидации
        }
        
        # Статистика извлечения
        self.stats = {}
    
    def load_text(self):
        """Загружаем текст документации"""
        with open(self.text_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    # ========== ИЗВЛЕКАТЕЛИ ЗНАНИЙ ==========
    
    def extract_endpoints(self):
        """1. Извлекаем все API endpoints"""
        print("📍 Извлекаем Endpoints...")
        
        # Паттерны для поиска
        endpoint_pattern = r'(GET|POST|PUT|DELETE|PATCH)\s+(/api/v\d+/[\w/\{\}:-]+)'
        
        # Ищем все endpoints
        for match in re.finditer(endpoint_pattern, self.text):
            method = match.group(1)
            path = match.group(2)
            
            # Получаем контекст вокруг endpoint (500 символов до и 2000 после)
            start = max(0, match.start() - 500)
            end = min(len(self.text), match.end() + 2000)
            context = self.text[start:end]
            
            # Извлекаем детали из контекста
            endpoint_data = {
                'id': f"{method}_{path.replace('/', '_')}",
                'method': method,
                'path': path,
                'category': self.detect_category(path),
                'description': self.extract_description(context),
                'summary': self.extract_summary(context),
                'auth_required': self.detect_auth(context),
                'deprecated': 'deprecated' in context.lower(),
                'request_type': self.extract_request_type(context),
                'response_type': self.extract_response_type(context),
                'tags': self.extract_tags(path, context),
                'related_models': self.extract_related_models(context),
                'complexity': self.assess_complexity(context)
            }
            
            self.knowledge_bases['endpoints'].append(endpoint_data)
        
        print(f"   ✅ Найдено {len(self.knowledge_bases['endpoints'])} endpoints")
    
    def extract_models(self):
        """2. Извлекаем модели данных и схемы"""
        print("📊 Извлекаем Models & Schemas...")
        
        # Паттерны для моделей
        patterns = [
            r'(?:Model|Schema|Type|Interface|Entity):\s*(\w+)',
            r'```(?:json|typescript|javascript)\n(\{[^`]+\})\n```',
            r'"(\w+)":\s*\{[^}]+\}',
        ]
        
        for pattern in patterns:
            for match in re.finditer(pattern, self.text, re.MULTILINE | re.DOTALL):
                # Анализируем найденную структуру
                if '{' in match.group(0):
                    try:
                        # Пытаемся распарсить как JSON
                        json_str = re.search(r'\{.*\}', match.group(0), re.DOTALL).group()
                        model_data = {
                            'model_name': self.extract_model_name(match.group(0)),
                            'structure': json_str,
                            'fields': self.parse_model_fields(json_str),
                            'required_fields': self.extract_required_fields(match.group(0)),
                            'relationships': self.extract_relationships(json_str),
                            'validation_rules': self.extract_validation_rules(match.group(0))
                        }
                        self.knowledge_bases['models'].append(model_data)
                    except:
                        pass
        
        print(f"   ✅ Найдено {len(self.knowledge_bases['models'])} моделей")
    
    def extract_parameters(self):
        """3. Извлекаем все параметры детально"""
        print("🔧 Извлекаем Parameters...")
        
        # Паттерны для параметров
        param_sections = re.findall(
            r'(?:Parameters?|Query Parameters?|Path Parameters?|Body Parameters?)[:\s]*\n((?:[-•*]\s*.+\n?)+)',
            self.text, re.IGNORECASE | re.MULTILINE
        )
        
        for section in param_sections:
            params = re.findall(r'[-•*]\s*`?(\w+)`?\s*[:\-–]\s*(.+?)(?:\n|$)', section)
            for param_name, param_desc in params:
                param_data = {
                    'name': param_name,
                    'description': param_desc.strip(),
                    'type': self.detect_param_type(param_desc),
                    'required': 'required' in param_desc.lower() or 'обязательн' in param_desc.lower(),
                    'default': self.extract_default_value(param_desc),
                    'constraints': self.extract_constraints(param_desc),
                    'examples': self.extract_param_examples(param_desc),
                    'location': self.detect_param_location(section)
                }
                self.knowledge_bases['parameters'].append(param_data)
        
        print(f"   ✅ Найдено {len(self.knowledge_bases['parameters'])} параметров")
    
    def extract_examples(self):
        """4. Извлекаем все примеры кода"""
        print("💻 Извлекаем Examples...")
        
        # Ищем все блоки кода
        code_blocks = re.findall(
            r'(?:Example|Sample|Usage)[:\s]*\n```(\w*)\n(.*?)\n```',
            self.text, re.IGNORECASE | re.DOTALL
        )
        
        for language, code in code_blocks:
            example_data = {
                'type': 'code',
                'language': language or 'json',
                'code': code,
                'title': self.extract_example_title(code),
                'description': self.extract_example_description(code),
                'endpoint': self.detect_related_endpoint(code),
                'category': self.detect_example_category(code)
            }
            self.knowledge_bases['examples'].append(example_data)
        
        # Также ищем CURL примеры
        curl_examples = re.findall(r'curl\s+.*?(?:\n\n|$)', self.text, re.DOTALL)
        for curl in curl_examples:
            self.knowledge_bases['examples'].append({
                'type': 'curl',
                'language': 'bash',
                'code': curl.strip(),
                'endpoint': self.extract_endpoint_from_curl(curl)
            })
        
        print(f"   ✅ Найдено {len(self.knowledge_bases['examples'])} примеров")
    
    def extract_errors(self):
        """5. Извлекаем коды ошибок и их решения"""
        print("❌ Извлекаем Error Codes...")
        
        # Паттерны для ошибок
        error_sections = re.findall(
            r'(?:Error Codes?|HTTP Status|Status Codes?)[:\s]*\n((?:[-•*]\s*.+\n?)+)',
            self.text, re.IGNORECASE | re.MULTILINE
        )
        
        # Также ищем отдельные упоминания кодов
        error_codes = re.findall(r'\b([4-5]\d{2})\b\s*[:\-–]\s*(.+?)(?:\n|$)', self.text)
        
        for code, description in error_codes:
            error_data = {
                'code': code,
                'description': description.strip(),
                'type': self.classify_error_type(code),
                'solution': self.extract_solution(description),
                'retry_able': self.is_retryable(code),
                'user_message': self.generate_user_message(code, description)
            }
            self.knowledge_bases['errors'].append(error_data)
        
        print(f"   ✅ Найдено {len(self.knowledge_bases['errors'])} кодов ошибок")
    
    def extract_auth(self):
        """6. Извлекаем методы авторизации"""
        print("🔐 Извлекаем Authentication...")
        
        auth_sections = re.findall(
            r'(?:Authentication|Authorization|Security|API Key|Token)[:\s]*(.+?)(?:\n\n|$)',
            self.text, re.IGNORECASE | re.DOTALL
        )
        
        for section in auth_sections:
            auth_data = {
                'method': self.detect_auth_method(section),
                'description': section.strip()[:500],
                'headers': self.extract_auth_headers(section),
                'token_type': self.detect_token_type(section),
                'expiration': self.extract_token_expiration(section),
                'refresh_mechanism': self.extract_refresh_mechanism(section),
                'example': self.extract_auth_example(section)
            }
            self.knowledge_bases['auth'].append(auth_data)
        
        print(f"   ✅ Найдено {len(self.knowledge_bases['auth'])} методов авторизации")
    
    def extract_webhooks(self):
        """7. Извлекаем webhooks и события"""
        print("🪝 Извлекаем Webhooks...")
        
        webhook_patterns = [
            r'(?:Webhook|Event|Notification)[:\s]*`?(\w+)`?',
            r'(?:event_type|eventType)["\']:\s*["\'](\w+)["\']'
        ]
        
        for pattern in webhook_patterns:
            for match in re.finditer(pattern, self.text):
                event_name = match.group(1)
                context = self.text[max(0, match.start()-300):min(len(self.text), match.end()+300)]
                
                webhook_data = {
                    'event_name': event_name,
                    'description': self.extract_description(context),
                    'payload': self.extract_webhook_payload(context),
                    'retry_policy': self.extract_retry_policy(context),
                    'headers': self.extract_webhook_headers(context)
                }
                self.knowledge_bases['webhooks'].append(webhook_data)
        
        print(f"   ✅ Найдено {len(self.knowledge_bases['webhooks'])} webhooks")
    
    def extract_business_rules(self):
        """8. Извлекаем бизнес-правила и ограничения"""
        print("📋 Извлекаем Business Rules...")
        
        # Паттерны для правил
        rule_patterns = [
            r'(?:Rule|Requirement|Constraint|Limitation|Note|Important)[:\s]*(.+?)(?:\n|$)',
            r'(?:must|should|cannot|limited to|maximum|minimum)\s+(.+?)(?:\.|$)'
        ]
        
        for pattern in rule_patterns:
            for match in re.finditer(pattern, self.text, re.IGNORECASE):
                rule = match.group(1).strip()
                if len(rule) > 20 and len(rule) < 500:
                    rule_data = {
                        'rule': rule,
                        'category': self.classify_rule(rule),
                        'severity': self.assess_rule_severity(rule),
                        'affected_endpoints': self.find_affected_endpoints(rule)
                    }
                    self.knowledge_bases['business_rules'].append(rule_data)
        
        print(f"   ✅ Найдено {len(self.knowledge_bases['business_rules'])} бизнес-правил")
    
    def extract_workflows(self):
        """9. Извлекаем типичные сценарии использования"""
        print("🔄 Извлекаем Workflows...")
        
        # Ищем последовательности вызовов
        workflow_patterns = [
            r'(?:Workflow|Process|Steps?|Scenario)[:\s]*\n((?:\d+\..*\n)+)',
            r'(?:First|Then|Finally|After that)[,\s]+(.+?)(?:\.|$)'
        ]
        
        for pattern in workflow_patterns:
            for match in re.finditer(pattern, self.text, re.MULTILINE):
                workflow_data = {
                    'workflow': match.group(0),
                    'steps': self.parse_workflow_steps(match.group(0)),
                    'endpoints_sequence': self.extract_endpoints_sequence(match.group(0)),
                    'category': self.detect_workflow_category(match.group(0))
                }
                self.knowledge_bases['workflows'].append(workflow_data)
        
        print(f"   ✅ Найдено {len(self.knowledge_bases['workflows'])} workflows")
    
    # ========== ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ==========
    
    def detect_category(self, path):
        """Определяем категорию endpoint по пути"""
        categories = {
            'fleet': ['fleet', 'vehicle', 'car', 'truck'],
            'driver': ['driver', 'operator', 'user'],
            'task': ['task', 'job', 'assignment'],
            'report': ['report', 'analytics', 'statistics'],
            'maintenance': ['maintenance', 'service', 'repair'],
            'fuel': ['fuel', 'gas', 'consumption'],
            'route': ['route', 'trip', 'journey'],
            'location': ['location', 'position', 'gps'],
            'document': ['document', 'file', 'attachment']
        }
        
        path_lower = path.lower()
        for category, keywords in categories.items():
            if any(keyword in path_lower for keyword in keywords):
                return category
        return 'general'
    
    def extract_description(self, context):
        """Извлекаем описание из контекста"""
        desc_pattern = r'(?:Description|Summary)[:\s]*(.+?)(?:\n\n|Parameters?|Example|$)'
        match = re.search(desc_pattern, context, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()[:500]
        
        # Берем первое предложение после endpoint
        sentences = re.split(r'[.!?]\s+', context)
        if sentences:
            return sentences[0].strip()[:500]
        return ""
    
    def extract_summary(self, context):
        """Извлекаем краткое описание"""
        # Берем первое предложение
        first_sentence = re.search(r'^[^.!?]+[.!?]', context.strip())
        if first_sentence:
            return first_sentence.group(0).strip()
        return ""
    
    def detect_auth(self, context):
        """Определяем требуется ли авторизация"""
        auth_indicators = ['authorization', 'authenticated', 'api key', 'token', 'bearer']
        no_auth_indicators = ['public', 'no authentication', 'anonymous']
        
        context_lower = context.lower()
        if any(indicator in context_lower for indicator in no_auth_indicators):
            return False
        if any(indicator in context_lower for indicator in auth_indicators):
            return True
        return True  # По умолчанию считаем что нужна
    
    def assess_complexity(self, context):
        """Оцениваем сложность endpoint"""
        # Простая эвристика: количество параметров и вложенность
        param_count = len(re.findall(r'[-•]\s*`?\w+`?', context))
        nested_objects = len(re.findall(r'\{[^}]*\{', context))
        
        if param_count < 3 and nested_objects == 0:
            return 'simple'
        elif param_count < 7 and nested_objects < 2:
            return 'medium'
        else:
            return 'complex'
    
    # ========== СОХРАНЕНИЕ РЕЗУЛЬТАТОВ ==========
    
    def save_all_knowledge_bases(self):
        """Сохраняем все базы знаний в разные форматы"""
        print("\n💾 Сохраняем базы знаний...")
        
        for kb_name, kb_data in self.knowledge_bases.items():
            if not kb_data:
                continue
                
            # JSON формат
            json_path = os.path.join(self.output_dir, f'{kb_name}.json')
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(kb_data, f, indent=2, ensure_ascii=False)
            
            # CSV формат (для импорта в Notion)
            csv_path = os.path.join(self.output_dir, f'{kb_name}.csv')
            if kb_data:
                keys = kb_data[0].keys()
                with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=keys)
                    writer.writeheader()
                    writer.writerows(kb_data)
            
            print(f"   ✅ {kb_name}: {len(kb_data)} записей → {json_path}")
        
        # Создаем мастер-файл со всей информацией
        master_data = {
            'api_name': 'Fleethand API',
            'version': self.extract_api_version(),
            'base_url': self.extract_base_url(),
            'generated_at': datetime.now().isoformat(),
            'statistics': self.generate_statistics(),
            'knowledge_bases': {
                name: f"{name}.json" for name in self.knowledge_bases.keys()
            }
        }
        
        with open(os.path.join(self.output_dir, 'master.json'), 'w', encoding='utf-8') as f:
            json.dump(master_data, f, indent=2)
        
        print(f"\n📊 Статистика извлечения:")
        for kb_name, kb_data in self.knowledge_bases.items():
            if kb_data:
                print(f"   • {kb_name}: {len(kb_data)} записей")
    
    def extract_api_version(self):
        """Извлекаем версию API"""
        version_match = re.search(r'/v(\d+)/', self.text)
        if version_match:
            return f"v{version_match.group(1)}"
        return "v1"
    
    def extract_base_url(self):
        """Извлекаем базовый URL"""
        url_match = re.search(r'https?://[^\s]+/api', self.text)
        if url_match:
            return url_match.group(0)
        return "https://api.fleethand.com"
    
    def generate_statistics(self):
        """Генерируем статистику"""
        return {
            'total_endpoints': len(self.knowledge_bases['endpoints']),
            'total_models': len(self.knowledge_bases['models']),
            'total_parameters': len(self.knowledge_bases['parameters']),
            'total_examples': len(self.knowledge_bases['examples']),
            'total_errors': len(self.knowledge_bases['errors']),
            'categories': list(set(e.get('category', '') for e in self.knowledge_bases['endpoints']))
        }
    
    # Дополнительные helper методы
    def detect_param_type(self, description):
        """Определяем тип параметра"""
        type_keywords = {
            'string': ['string', 'text', 'str'],
            'integer': ['integer', 'int', 'number'],
            'boolean': ['boolean', 'bool', 'true/false'],
            'array': ['array', 'list', '[]'],
            'object': ['object', 'dict', '{}'],
            'datetime': ['datetime', 'date', 'timestamp'],
            'uuid': ['uuid', 'guid', 'id']
        }
        
        desc_lower = description.lower()
        for type_name, keywords in type_keywords.items():
            if any(kw in desc_lower for kw in keywords):
                return type_name
        return 'string'
    
    def classify_error_type(self, code):
        """Классифицируем тип ошибки по коду"""
        code = int(code)
        if 400 <= code < 500:
            return 'client_error'
        elif 500 <= code < 600:
            return 'server_error'
        return 'unknown'
    
    def is_retryable(self, code):
        """Определяем можно ли повторить запрос"""
        retryable_codes = [408, 429, 502, 503, 504]
        return int(code) in retryable_codes
    
    def run(self):
        """Запускаем полный процесс извлечения"""
        print("🧠 Начинаем извлечение знаний из документации...")
        print("=" * 60)
        
        # Извлекаем все типы знаний
        self.extract_endpoints()
        self.extract_models()
        self.extract_parameters()
        self.extract_examples()
        self.extract_errors()
        self.extract_auth()
        self.extract_webhooks()
        self.extract_business_rules()
        self.extract_workflows()
        
        # Сохраняем результаты
        self.save_all_knowledge_bases()
        
        print("=" * 60)
        print("✨ Готово! Все базы знаний созданы в папке:", self.output_dir)
        print("\n📁 Созданные файлы:")
        for file in os.listdir(self.output_dir):
            print(f"   • {file}")
        
        return self.output_dir

    # Дополнительные методы-заглушки (нужно реализовать по необходимости)
    def extract_request_type(self, context): return "application/json"
    def extract_response_type(self, context): return "application/json"
    def extract_tags(self, path, context): return []
    def extract_related_models(self, context): return []
    def extract_model_name(self, text): return "Model"
    def parse_model_fields(self, json_str): return []
    def extract_required_fields(self, text): return []
    def extract_relationships(self, json_str): return []
    def extract_validation_rules(self, text): return []
    def extract_default_value(self, desc): return None
    def extract_constraints(self, desc): return []
    def extract_param_examples(self, desc): return []
    def detect_param_location(self, section): return "query"
    def extract_example_title(self, code): return "Example"
    def extract_example_description(self, code): return ""
    def detect_related_endpoint(self, code): return None
    def detect_example_category(self, code): return "general"
    def extract_endpoint_from_curl(self, curl): return None
    def extract_solution(self, desc): return ""
    def generate_user_message(self, code, desc): return desc
    def detect_auth_method(self, section): return "Bearer Token"
    def extract_auth_headers(self, section): return {}
    def detect_token_type(self, section): return "JWT"
    def extract_token_expiration(self, section): return "3600"
    def extract_refresh_mechanism(self, section): return ""
    def extract_auth_example(self, section): return ""
    def extract_webhook_payload(self, context): return {}
    def extract_retry_policy(self, context): return ""
    def extract_webhook_headers(self, context): return {}
    def classify_rule(self, rule): return "general"
    def assess_rule_severity(self, rule): return "medium"
    def find_affected_endpoints(self, rule): return []
    def parse_workflow_steps(self, text): return []
    def extract_endpoints_sequence(self, text): return []
    def detect_workflow_category(self, text): return "general"

if __name__ == "__main__":
    extractor = SmartKnowledgeExtractor('extracted_text.txt')
    extractor.run()