#!/usr/bin/env python3
"""
Complete Knowledge Base Extractor для Fleethand API
Извлекает ВСЕ 15 типов знаний из документации
"""

import re
import json
import csv
from typing import Dict, List, Any
from datetime import datetime
import os

class CompleteFleethandExtractor:
    def __init__(self, text_file='extracted_text.txt'):
        self.text_file = text_file
        self.text = self.load_text()
        
        # Создаем папку для всех баз знаний
        self.output_dir = 'complete_knowledge_bases'
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
    
    def load_text(self):
        """Загружаем текст документации"""
        with open(self.text_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    def extract_endpoints(self):
        """1. Извлекаем все API endpoints"""
        print("📍 Извлекаем Endpoints...")
        
        # Используем улучшенный паттерн для Fleethand
        pattern = r'Method\s*\n\s*URL\s*\n\s*(GET|POST|PUT|DELETE|PATCH)\s*\n\s*(/api/[^\s\n]+)'
        
        for match in re.finditer(pattern, self.text, re.MULTILINE):
            method = match.group(1)
            path = match.group(2)
            
            # Получаем контекст
            start = max(0, match.start() - 1000)
            end = min(len(self.text), match.end() + 2000)
            context = self.text[start:end]
            
            endpoint_data = {
                'id': f"{method}_{path.replace('/', '_').replace('-', '_')}",
                'method': method,
                'path': path,
                'category': self.detect_category(path),
                'description': self.extract_description(context),
                'summary': self.extract_summary(context),
                'auth_required': True,
                'deprecated': 'deprecated' in context.lower(),
                'request_content_type': 'application/json',
                'response_content_type': 'application/json',
                'tags': self.extract_tags(path, context),
                'complexity': self.assess_complexity(context),
                'parameters': self.extract_endpoint_parameters(context),
                'request_body': self.extract_request_body(context),
                'response_example': self.extract_response_example(context)
            }
            
            self.knowledge_bases['endpoints'].append(endpoint_data)
        
        print(f"   ✅ Найдено {len(self.knowledge_bases['endpoints'])} endpoints")
    
    def extract_models(self):
        """2. Извлекаем модели данных"""
        print("📊 Извлекаем Models & Schemas...")
        
        # Ищем JSON структуры в документации
        json_patterns = [
            r'\{[^{}]*"[^"]*"\s*:[^{}]*\}',  # Простые объекты
            r'\{[^{}]*\{[^{}]*\}[^{}]*\}',   # Вложенные объекты
            r'\[[^\[\]]*\{[^{}]*\}[^\[\]]*\]' # Массивы объектов
        ]
        
        model_id = 1
        for pattern in json_patterns:
            for match in re.finditer(pattern, self.text, re.DOTALL):
                json_str = match.group(0)
                
                if len(json_str) > 50 and len(json_str) < 2000:  # Разумные размеры
                    try:
                        # Пытаемся понять что это за модель
                        context = self.text[max(0, match.start()-200):min(len(self.text), match.end()+200)]
                        
                        model_data = {
                            'id': f'model_{model_id}',
                            'model_name': self.extract_model_name(context, json_str),
                            'structure': json_str,
                            'fields': self.parse_json_fields(json_str),
                            'category': self.detect_model_category(context),
                            'usage_context': context[:300],
                            'is_request': 'request' in context.lower(),
                            'is_response': 'response' in context.lower(),
                            'validation_rules': self.extract_validation_from_context(context)
                        }
                        
                        self.knowledge_bases['models'].append(model_data)
                        model_id += 1
                    except Exception as e:
                        continue
        
        print(f"   ✅ Найдено {len(self.knowledge_bases['models'])} моделей")
    
    def extract_parameters(self):
        """3. Детально извлекаем параметры"""
        print("🔧 Извлекаем Parameters...")
        
        # Ищем все упоминания параметров в тексте
        param_patterns = [
            r'(\w+Id)\s*[-–:]\s*([^.\n]+)',  # ID параметры
            r'(\w+)\s*\(([^)]+)\)\s*[-–:]\s*([^.\n]+)', # Параметры с типами
            r'`(\w+)`\s*[-–:]\s*([^.\n]+)', # Параметры в backticks
            r'(\w+)\s*parameter\s*[-–:]\s*([^.\n]+)', # Явные параметры
        ]
        
        param_id = 1
        for pattern in param_patterns:
            for match in re.finditer(pattern, self.text, re.IGNORECASE):
                if len(match.groups()) >= 2:
                    param_name = match.group(1)
                    param_desc = match.groups()[-1]
                    param_type = match.group(2) if len(match.groups()) > 2 else None
                    
                    if len(param_name) > 2 and len(param_desc) > 5:
                        param_data = {
                            'id': f'param_{param_id}',
                            'name': param_name,
                            'description': param_desc.strip()[:200],
                            'type': param_type or self.detect_param_type(param_desc),
                            'required': self.is_param_required(param_desc),
                            'location': self.detect_param_location(param_desc),
                            'example': self.extract_param_example(param_desc),
                            'validation': self.extract_param_validation(param_desc),
                            'default_value': self.extract_default_value(param_desc)
                        }
                        
                        self.knowledge_bases['parameters'].append(param_data)
                        param_id += 1
        
        print(f"   ✅ Найдено {len(self.knowledge_bases['parameters'])} параметров")
    
    def extract_examples(self):
        """4. Извлекаем примеры кода"""
        print("💻 Извлекаем Examples...")
        
        # Ищем различные типы примеров
        example_patterns = [
            (r'curl\s+.*?(?=\n\n|\nMethod|\n[A-Z])', 'curl'),
            (r'```json\n(.*?)\n```', 'json'),
            (r'```\n(.*?)\n```', 'code'),
            (r'Example[:\s]*\n([^=]+?)(?=\n=|\nMethod|\n[A-Z])', 'example'),
            (r'Response[:\s]*\n([^=]+?)(?=\n=|\nMethod|\n[A-Z])', 'response')
        ]
        
        example_id = 1
        for pattern, example_type in example_patterns:
            for match in re.finditer(pattern, self.text, re.DOTALL | re.IGNORECASE):
                example_text = match.group(1) if len(match.groups()) > 0 else match.group(0)
                example_text = example_text.strip()
                
                if len(example_text) > 20 and len(example_text) < 5000:
                    # Получаем контекст для понимания к какому endpoint относится
                    context = self.text[max(0, match.start()-500):min(len(self.text), match.end()+100)]
                    
                    example_data = {
                        'id': f'example_{example_id}',
                        'type': example_type,
                        'content': example_text,
                        'title': self.extract_example_title(context),
                        'related_endpoint': self.find_related_endpoint(context),
                        'category': self.detect_example_category(context),
                        'language': self.detect_language(example_text),
                        'description': self.extract_example_description(context)
                    }
                    
                    self.knowledge_bases['examples'].append(example_data)
                    example_id += 1
        
        print(f"   ✅ Найдено {len(self.knowledge_bases['examples'])} примеров")
    
    def extract_errors(self):
        """5. Извлекаем коды ошибок"""
        print("❌ Извлекаем Error Codes...")
        
        # Ищем HTTP коды и описания ошибок
        error_patterns = [
            r'\b([4-5]\d{2})\s*[-–:]\s*([^.\n]+)',  # HTTP коды
            r'error[:\s]*([^.\n]+)', # Общие ошибки
            r'Error[:\s]*([^.\n]+)', # Ошибки с заглавной буквы
            r'failed[:\s]*([^.\n]+)', # Сбои
        ]
        
        error_id = 1
        for pattern in error_patterns:
            for match in re.finditer(pattern, self.text, re.IGNORECASE):
                if len(match.groups()) >= 2:
                    error_code = match.group(1)
                    error_desc = match.group(2)
                elif len(match.groups()) == 1:
                    error_code = f'ERR_{error_id:03d}'
                    error_desc = match.group(1)
                else:
                    continue
                
                if len(error_desc.strip()) > 10:
                    error_data = {
                        'id': f'error_{error_id}',
                        'code': error_code,
                        'description': error_desc.strip()[:200],
                        'type': self.classify_error_type(error_code),
                        'severity': self.assess_error_severity(error_desc),
                        'retryable': self.is_retryable_error(error_code),
                        'solution': self.suggest_solution(error_desc),
                        'category': self.categorize_error(error_desc)
                    }
                    
                    self.knowledge_bases['errors'].append(error_data)
                    error_id += 1
        
        print(f"   ✅ Найдено {len(self.knowledge_bases['errors'])} ошибок")
    
    def extract_auth(self):
        """6. Извлекаем информацию об авторизации"""
        print("🔐 Извлекаем Authentication...")
        
        # Ищем упоминания авторизации и ключей
        auth_patterns = [
            r'(API[_\s]?[Kk]ey|Token|Bearer|Authorization)[:\s]*([^.\n]+)',
            r'(authentication|authorization)[:\s]*([^.\n]+)',
            r'(key|token|bearer)[:\s]*([^.\n]+)',
        ]
        
        auth_id = 1
        for pattern in auth_patterns:
            for match in re.finditer(pattern, self.text, re.IGNORECASE):
                auth_type = match.group(1)
                auth_desc = match.group(2)
                
                if len(auth_desc.strip()) > 5:
                    auth_data = {
                        'id': f'auth_{auth_id}',
                        'method': auth_type,
                        'description': auth_desc.strip()[:300],
                        'type': self.detect_auth_type(auth_type, auth_desc),
                        'header_name': self.extract_header_name(auth_desc),
                        'format': self.extract_auth_format(auth_desc),
                        'example': self.extract_auth_example(auth_desc)
                    }
                    
                    self.knowledge_bases['auth'].append(auth_data)
                    auth_id += 1
        
        print(f"   ✅ Найдено {len(self.knowledge_bases['auth'])} методов авторизации")
    
    def extract_webhooks(self):
        """7. Извлекаем webhooks и события"""
        print("🪝 Извлекаем Webhooks...")
        
        webhook_patterns = [
            r'(webhook|event|notification|callback)[:\s]*([^.\n]+)',
            r'(event[_\s]?type|eventType)[:\s]*([^.\n]+)',
        ]
        
        webhook_id = 1
        for pattern in webhook_patterns:
            for match in re.finditer(pattern, self.text, re.IGNORECASE):
                webhook_type = match.group(1)
                webhook_desc = match.group(2)
                
                if len(webhook_desc.strip()) > 10:
                    webhook_data = {
                        'id': f'webhook_{webhook_id}',
                        'event_name': webhook_type,
                        'description': webhook_desc.strip()[:300],
                        'trigger': self.extract_webhook_trigger(webhook_desc),
                        'payload': self.extract_webhook_payload(webhook_desc),
                        'frequency': self.extract_webhook_frequency(webhook_desc)
                    }
                    
                    self.knowledge_bases['webhooks'].append(webhook_data)
                    webhook_id += 1
        
        print(f"   ✅ Найдено {len(self.knowledge_bases['webhooks'])} webhooks")
    
    def extract_rate_limits(self):
        """8. Извлекаем ограничения и лимиты"""
        print("⏱️ Извлекаем Rate Limits...")
        
        limit_patterns = [
            r'(limit|maximum|max|minimum|min|rate)[:\s]*([^.\n]+)',
            r'(\d+)\s*(per|/)\s*(second|minute|hour|day|request)',
            r'(timeout|delay)[:\s]*([^.\n]+)',
        ]
        
        limit_id = 1
        for pattern in limit_patterns:
            for match in re.finditer(pattern, self.text, re.IGNORECASE):
                if 'limit' in match.group(0).lower() or 'rate' in match.group(0).lower():
                    limit_data = {
                        'id': f'limit_{limit_id}',
                        'type': match.group(1),
                        'description': match.group(0)[:200],
                        'value': self.extract_limit_value(match.group(0)),
                        'unit': self.extract_limit_unit(match.group(0)),
                        'scope': self.extract_limit_scope(match.group(0))
                    }
                    
                    self.knowledge_bases['rate_limits'].append(limit_data)
                    limit_id += 1
        
        print(f"   ✅ Найдено {len(self.knowledge_bases['rate_limits'])} лимитов")
    
    def extract_business_rules(self):
        """9. Извлекаем бизнес-правила"""
        print("📋 Извлекаем Business Rules...")
        
        rule_patterns = [
            r'(must|should|cannot|required|mandatory|optional)[:\s]*([^.\n]+)',
            r'(rule|constraint|limitation|requirement)[:\s]*([^.\n]+)',
            r'(note|important|warning)[:\s]*([^.\n]+)',
        ]
        
        rule_id = 1
        for pattern in rule_patterns:
            for match in re.finditer(pattern, self.text, re.IGNORECASE):
                rule_type = match.group(1)
                rule_desc = match.group(2)
                
                if len(rule_desc.strip()) > 20:
                    rule_data = {
                        'id': f'rule_{rule_id}',
                        'type': rule_type,
                        'description': rule_desc.strip()[:300],
                        'severity': self.assess_rule_severity(rule_type),
                        'category': self.categorize_rule(rule_desc),
                        'enforcement': self.detect_rule_enforcement(rule_type)
                    }
                    
                    self.knowledge_bases['business_rules'].append(rule_data)
                    rule_id += 1
        
        print(f"   ✅ Найдено {len(self.knowledge_bases['business_rules'])} правил")
    
    def extract_glossary(self):
        """10. Создаем словарь терминов"""
        print("📖 Извлекаем Glossary...")
        
        # Собираем важные термины из API paths и описаний
        terms = set()
        
        # Из путей API
        for endpoint in self.knowledge_bases['endpoints']:
            path_parts = endpoint['path'].split('/')
            for part in path_parts:
                if len(part) > 3 and part.isalpha():
                    terms.add(part)
        
        # Частые термины в документации
        common_terms = [
            'vehicle', 'driver', 'fleet', 'task', 'activity', 'document',
            'report', 'location', 'partner', 'user', 'assignment', 'fuel',
            'maintenance', 'route', 'trip', 'status', 'position'
        ]
        
        for term in common_terms:
            if term in self.text.lower():
                terms.add(term)
        
        term_id = 1
        for term in sorted(terms):
            # Находим контекст где термин упоминается
            pattern = rf'\b{re.escape(term)}\b[^.\n]*'
            matches = re.findall(pattern, self.text, re.IGNORECASE)
            
            if matches:
                definition = matches[0][:200]
                
                glossary_data = {
                    'id': f'term_{term_id}',
                    'term': term,
                    'definition': definition,
                    'category': self.categorize_term(term),
                    'usage_count': len(matches),
                    'related_endpoints': self.find_related_endpoints_for_term(term)
                }
                
                self.knowledge_bases['glossary'].append(glossary_data)
                term_id += 1
        
        print(f"   ✅ Найдено {len(self.knowledge_bases['glossary'])} терминов")
    
    def extract_workflows(self):
        """11. Извлекаем workflows и сценарии"""
        print("🔄 Извлекаем Workflows...")
        
        # Ищем последовательности действий
        workflow_patterns = [
            r'(first|then|next|after|finally)[:\s]*([^.\n]+)',
            r'(step\s*\d+)[:\s]*([^.\n]+)',
            r'(workflow|process|scenario)[:\s]*([^.\n]+)',
        ]
        
        workflow_id = 1
        for pattern in workflow_patterns:
            for match in re.finditer(pattern, self.text, re.IGNORECASE):
                step_indicator = match.group(1)
                step_desc = match.group(2)
                
                if len(step_desc.strip()) > 15:
                    workflow_data = {
                        'id': f'workflow_{workflow_id}',
                        'step_indicator': step_indicator,
                        'description': step_desc.strip()[:300],
                        'order': self.extract_step_order(step_indicator),
                        'category': self.categorize_workflow(step_desc),
                        'related_endpoints': self.find_endpoints_in_text(step_desc)
                    }
                    
                    self.knowledge_bases['workflows'].append(workflow_data)
                    workflow_id += 1
        
        print(f"   ✅ Найдено {len(self.knowledge_bases['workflows'])} workflow шагов")
    
    def extract_integrations(self):
        """12. Извлекаем информацию об интеграциях"""
        print("🔗 Извлекаем Integrations...")
        
        integration_patterns = [
            r'(integration|connect|sync|import|export)[:\s]*([^.\n]+)',
            r'(third[_\s]?party|external)[:\s]*([^.\n]+)',
        ]
        
        integration_id = 1
        for pattern in integration_patterns:
            for match in re.finditer(pattern, self.text, re.IGNORECASE):
                integration_type = match.group(1)
                integration_desc = match.group(2)
                
                if len(integration_desc.strip()) > 20:
                    integration_data = {
                        'id': f'integration_{integration_id}',
                        'type': integration_type,
                        'description': integration_desc.strip()[:300],
                        'direction': self.detect_integration_direction(integration_desc),
                        'format': self.detect_integration_format(integration_desc)
                    }
                    
                    self.knowledge_bases['integrations'].append(integration_data)
                    integration_id += 1
        
        print(f"   ✅ Найдено {len(self.knowledge_bases['integrations'])} интеграций")
    
    def extract_permissions(self):
        """13. Извлекаем роли и разрешения"""
        print("👥 Извлекаем Permissions...")
        
        permission_patterns = [
            r'(role|permission|access|privilege)[:\s]*([^.\n]+)',
            r'(admin|user|manager|operator)[:\s]*([^.\n]+)',
        ]
        
        permission_id = 1
        for pattern in permission_patterns:
            for match in re.finditer(pattern, self.text, re.IGNORECASE):
                permission_type = match.group(1)
                permission_desc = match.group(2)
                
                if len(permission_desc.strip()) > 10:
                    permission_data = {
                        'id': f'permission_{permission_id}',
                        'type': permission_type,
                        'description': permission_desc.strip()[:300],
                        'level': self.detect_permission_level(permission_type),
                        'scope': self.detect_permission_scope(permission_desc)
                    }
                    
                    self.knowledge_bases['permissions'].append(permission_data)
                    permission_id += 1
        
        print(f"   ✅ Найдено {len(self.knowledge_bases['permissions'])} разрешений")
    
    def extract_data_types(self):
        """14. Извлекаем типы данных"""
        print("🏗️ Извлекаем Data Types...")
        
        # Собираем типы из параметров и моделей
        data_types = set()
        
        for param in self.knowledge_bases['parameters']:
            if param.get('type'):
                data_types.add(param['type'])
        
        # Добавляем стандартные типы API
        standard_types = [
            'string', 'integer', 'boolean', 'array', 'object',
            'datetime', 'uuid', 'email', 'url', 'phone'
        ]
        
        type_id = 1
        for data_type in sorted(data_types.union(standard_types)):
            type_data = {
                'id': f'type_{type_id}',
                'name': data_type,
                'description': self.describe_data_type(data_type),
                'format': self.get_type_format(data_type),
                'validation': self.get_type_validation(data_type),
                'examples': self.get_type_examples(data_type)
            }
            
            self.knowledge_bases['data_types'].append(type_data)
            type_id += 1
        
        print(f"   ✅ Найдено {len(self.knowledge_bases['data_types'])} типов данных")
    
    def extract_validations(self):
        """15. Извлекаем правила валидации"""
        print("✅ Извлекаем Validations...")
        
        validation_patterns = [
            r'(valid|invalid|validate|validation)[:\s]*([^.\n]+)',
            r'(format|pattern|regex)[:\s]*([^.\n]+)',
            r'(length|size|range)[:\s]*([^.\n]+)',
        ]
        
        validation_id = 1
        for pattern in validation_patterns:
            for match in re.finditer(pattern, self.text, re.IGNORECASE):
                validation_type = match.group(1)
                validation_desc = match.group(2)
                
                if len(validation_desc.strip()) > 10:
                    validation_data = {
                        'id': f'validation_{validation_id}',
                        'type': validation_type,
                        'description': validation_desc.strip()[:300],
                        'rule': self.extract_validation_rule(validation_desc),
                        'error_message': self.extract_validation_error(validation_desc)
                    }
                    
                    self.knowledge_bases['validations'].append(validation_data)
                    validation_id += 1
        
        print(f"   ✅ Найдено {len(self.knowledge_bases['validations'])} правил валидации")
    
    # ========== ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ==========
    
    def detect_category(self, path):
        """Определяем категорию endpoint"""
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
        }
        
        path_lower = path.lower()
        for category, keywords in categories.items():
            if any(keyword in path_lower for keyword in keywords):
                return category
        return 'general'
    
    def save_all_knowledge_bases(self):
        """Сохраняем все базы знаний"""
        print("\n💾 Сохраняем все 15 баз знаний...")
        
        total_records = 0
        for kb_name, kb_data in self.knowledge_bases.items():
            if kb_data:
                # JSON формат
                json_path = os.path.join(self.output_dir, f'{kb_name}.json')
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(kb_data, f, indent=2, ensure_ascii=False)
                
                # CSV формат
                csv_path = os.path.join(self.output_dir, f'{kb_name}.csv')
                if kb_data:
                    keys = kb_data[0].keys()
                    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.DictWriter(f, fieldnames=keys)
                        writer.writeheader()
                        writer.writerows(kb_data)
                
                print(f"   ✅ {kb_name}: {len(kb_data)} записей")
                total_records += len(kb_data)
            else:
                print(f"   ⚠️ {kb_name}: пустая база")
        
        # Создаем мастер-файл
        master_data = {
            'api_name': 'Fleethand API',
            'version': 'v1',
            'generated_at': datetime.now().isoformat(),
            'total_records': total_records,
            'knowledge_bases': {
                name: {
                    'file': f"{name}.json",
                    'count': len(data),
                    'description': self.get_kb_description(name)
                } for name, data in self.knowledge_bases.items()
            }
        }
        
        with open(os.path.join(self.output_dir, 'master.json'), 'w', encoding='utf-8') as f:
            json.dump(master_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 Итого: {total_records} записей в {len([kb for kb in self.knowledge_bases.values() if kb])} базах знаний")
        return total_records
    
    def get_kb_description(self, kb_name):
        """Описания баз знаний"""
        descriptions = {
            'endpoints': 'Все API методы с полной информацией',
            'models': 'Структуры данных и схемы',
            'parameters': 'Детальное описание всех параметров',
            'examples': 'Примеры кода и использования',
            'errors': 'Коды ошибок и их решения',
            'auth': 'Методы авторизации',
            'webhooks': 'События и уведомления',
            'rate_limits': 'Ограничения API',
            'business_rules': 'Бизнес-логика и правила',
            'glossary': 'Словарь терминов',
            'workflows': 'Сценарии использования',
            'integrations': 'Интеграции',
            'permissions': 'Роли и права',
            'data_types': 'Типы данных',
            'validations': 'Правила валидации'
        }
        return descriptions.get(kb_name, 'Дополнительная информация')
    
    def run(self):
        """Запускаем полный процесс извлечения всех 15 баз знаний"""
        print("🧠 Полное извлечение знаний из Fleethand API документации...")
        print("=" * 70)
        
        # Извлекаем все типы знаний
        self.extract_endpoints()        # 1
        self.extract_models()          # 2
        self.extract_parameters()      # 3
        self.extract_examples()        # 4
        self.extract_errors()          # 5
        self.extract_auth()            # 6
        self.extract_webhooks()        # 7
        self.extract_rate_limits()     # 8
        self.extract_business_rules()  # 9
        self.extract_glossary()        # 10
        self.extract_workflows()       # 11
        self.extract_integrations()    # 12
        self.extract_permissions()     # 13
        self.extract_data_types()      # 14
        self.extract_validations()     # 15
        
        # Сохраняем все результаты
        total_records = self.save_all_knowledge_bases()
        
        print("=" * 70)
        print("✨ Готово! Все 15 специализированных баз знаний созданы!")
        print(f"📁 Папка: {self.output_dir}/")
        print(f"📊 Общее количество записей: {total_records}")
        
        return self.output_dir

    # Минимальные реализации helper методов
    def extract_description(self, context): 
        return "API endpoint"
    def extract_summary(self, context): 
        return "API method"
    def extract_tags(self, path, context): 
        return [self.detect_category(path)]
    def assess_complexity(self, context): 
        return "medium"
    def extract_endpoint_parameters(self, context): 
        return []
    def extract_request_body(self, context): 
        return None
    def extract_response_example(self, context): 
        return None
    def extract_model_name(self, context, json_str): 
        return "DataModel"
    def parse_json_fields(self, json_str): 
        return []
    def detect_model_category(self, context): 
        return "general"
    def extract_validation_from_context(self, context): 
        return []
    def detect_param_type(self, desc): 
        return "string"
    def is_param_required(self, desc): 
        return False
    def detect_param_location(self, desc): 
        return "query"
    def extract_param_example(self, desc): 
        return None
    def extract_param_validation(self, desc): 
        return []
    def extract_default_value(self, desc): 
        return None
    def extract_example_title(self, context): 
        return "Example"
    def find_related_endpoint(self, context): 
        return None
    def detect_example_category(self, context): 
        return "general"
    def detect_language(self, text): 
        return "json"
    def extract_example_description(self, context): 
        return ""
    def classify_error_type(self, code): 
        return "unknown"
    def assess_error_severity(self, desc): 
        return "medium"
    def is_retryable_error(self, code): 
        return False
    def suggest_solution(self, desc): 
        return ""
    def categorize_error(self, desc): 
        return "general"
    def detect_auth_type(self, auth_type, desc): 
        return "API_KEY"
    def extract_header_name(self, desc): 
        return "Authorization"
    def extract_auth_format(self, desc): 
        return "Bearer {token}"
    def extract_auth_example(self, desc): 
        return ""
    def extract_webhook_trigger(self, desc): 
        return "unknown"
    def extract_webhook_payload(self, desc): 
        return {}
    def extract_webhook_frequency(self, desc): 
        return "on_event"
    def extract_limit_value(self, text): 
        return "unknown"
    def extract_limit_unit(self, text): 
        return "requests"
    def extract_limit_scope(self, text): 
        return "global"
    def assess_rule_severity(self, rule_type): 
        return "medium"
    def categorize_rule(self, desc): 
        return "general"
    def detect_rule_enforcement(self, rule_type): 
        return "soft"
    def categorize_term(self, term): 
        return "general"
    def find_related_endpoints_for_term(self, term): 
        return []
    def extract_step_order(self, indicator): 
        return 1
    def categorize_workflow(self, desc): 
        return "general"
    def find_endpoints_in_text(self, text): 
        return []
    def detect_integration_direction(self, desc): 
        return "bidirectional"
    def detect_integration_format(self, desc): 
        return "JSON"
    def detect_permission_level(self, perm_type): 
        return "user"
    def detect_permission_scope(self, desc): 
        return "resource"
    def describe_data_type(self, data_type): 
        return f"Data type: {data_type}"
    def get_type_format(self, data_type): 
        return "standard"
    def get_type_validation(self, data_type): 
        return []
    def get_type_examples(self, data_type): 
        return []
    def extract_validation_rule(self, desc): 
        return "unknown"
    def extract_validation_error(self, desc): 
        return "Invalid input"

if __name__ == "__main__":
    extractor = CompleteFleethandExtractor('extracted_text.txt')
    extractor.run()