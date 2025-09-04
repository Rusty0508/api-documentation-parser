# 🚀 API Documentation Parser for MCP Servers

**Интеллектуальный парсер PDF документации API с веб-интерфейсом для создания MCP серверов**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Quality](https://img.shields.io/badge/Quality-HIGH-brightgreen)](FINAL_ACHIEVEMENT_REPORT.md)

## 🎯 Описание

Этот проект автоматически преобразует PDF документацию API в структурированные данные для создания MCP (Model Context Protocol) серверов. С помощью интеллектуальных алгоритмов извлекает endpoints, заголовки, параметры и ответы API.

### ✨ Возможности
- 📄 **Парсинг PDF документации** с высокой точностью
- 🎯 **Автоматическое извлечение** endpoints, headers, parameters, responses
- 🧠 **Интеллектуальная категоризация** API методов (13 категорий)
- 🔧 **Готовые данные для MCP серверов** в формате JSON
- 🌐 **Веб-интерфейс** для загрузки и обработки документов
- 📊 **Детальная отчетность** о качестве парсинга
- ✅ **HIGH качество результатов** (85%+ MCP готовности)

## 🏆 Результаты

### Флагманские показатели:
- ✅ **MCP готовность: 85.5%** (HIGH качество)
- ✅ **Качество titles: 99.2%** 
- ✅ **Качество descriptions: 90.9%**
- ✅ **Headers: 100% покрытие**
- ✅ **Responses: 90.9% покрытие**

### Статистика парсинга:
```
📊 Fleethand API (пример):
├── 121 endpoints извлечено
├── 242 headers обработано
├── 47 parameters найдено
├── 110 responses документировано
└── 13 категорий классифицировано
```

## 🚀 Быстрый старт

### Установка
```bash
git clone https://github.com/your-username/api-doc-parser.git
cd api-doc-parser
pip install -r requirements.txt
```

### Использование через CLI
```bash
# Парсинг PDF документации
python fleethand_ultimate_parser.py

# Результаты будут сохранены в ultimate_final_data/
```

### Веб-интерфейс
```bash
# Запуск веб-сервера
python web_interface.py

# Откройте http://localhost:5000 в браузере
```

## 📁 Структура результатов

```
ultimate_final_data/
├── endpoints_ultimate_final.json      # Все endpoints для MCP tools
├── mcp_server_ultimate_final.json     # Готовый MCP server config
└── quality_report_ultimate_final.json # Отчет о качестве
```

### Пример endpoint:
```json
{
  "operation_id": "get__api_drivers",
  "method": "GET",
  "path": "/api/drivers",
  "summary": "Get drivers information",
  "description": "This method returns information about client drivers",
  "category": "drivers",
  "headers": [
    {
      "name": "apiKey",
      "data_type": "String",
      "required": true,
      "description": "Encoded api key"
    }
  ],
  "parameters": [],
  "responses": [
    {
      "status_code": "200",
      "description": "Successful response",
      "schema": {...}
    }
  ]
}
```

## 🔧 Архитектура

### Ключевые компоненты:
1. **PDF Text Extraction** - Извлечение текста из PDF (PyMuPDF)
2. **Intelligent Parsing** - Множественные алгоритмы анализа
3. **Quality Scoring** - Система оценки качества результатов
4. **MCP Generation** - Автоматическое создание MCP структур
5. **Web Interface** - Удобный веб-интерфейс

### Алгоритмы парсинга:
- 🎯 **Smart Title Detection** - Интеллектуальное определение заголовков
- 📝 **Context-Aware Description Extraction** - Извлечение описаний по контексту
- 🏷️ **Advanced Categorization** - Категоризация по 13 типам
- ✅ **Auto JSON Validation** - Автоматическая валидация и исправление

## 🌟 Особенности

### Интеллектуальные возможности:
- **Построчный парсинг** headers и parameters
- **Множественные стратегии** поиска descriptions
- **Автоисправление JSON** структур
- **Валидация данных** на всех этапах
- **Подробная метрика** качества

### Категории API:
`activities`, `drivers`, `vehicles`, `documents`, `tasks`, `partners`, `orders`, `eco`, `reports`, `tacho`, `locations`, `payments`, `forms`, `general`

## 📊 Веб-интерфейс

### Функциональность:
1. **Загрузка PDF** - Простой drag & drop интерфейс
2. **Настройки парсинга** - Выбор параметров обработки
3. **Прогресс обработки** - Реальное время выполнения
4. **Результаты** - Интерактивное отображение данных
5. **Экспорт** - Скачивание в различных форматах

### Технологии:
- **Backend**: Flask/FastAPI
- **Frontend**: HTML5, CSS3, JavaScript
- **Processing**: Python 3.8+
- **PDF**: PyMuPDF
- **Data**: JSON Schema validation

## 📈 Качество результатов

### Метрики качества:
```
MCP Readiness Score = 
  (Title Quality × 0.20) +
  (Description Quality × 0.30) + 
  (Headers Coverage × 0.15) +
  (Parameters Coverage × 0.15) +
  (Responses Coverage × 0.15) +
  (Average Quality Score × 0.05)
```

### Уровни качества:
- **HIGH**: 85%+ MCP готовности + 60%+ descriptions
- **MEDIUM**: 75%+ MCP готовности + 40%+ descriptions  
- **LOW**: Менее 75% MCP готовности

## 🛠️ Требования

```
Python >= 3.8
PyMuPDF >= 1.23.0
Flask >= 2.0.0 (для веб-интерфейса)
requests >= 2.25.0
dataclasses-json >= 0.5.0
```

## 📝 Лицензия

MIT License - подробности в [LICENSE](LICENSE)

## 🤝 Вклад в проект

Мы приветствуем вклад в развитие проекта! Пожалуйста:

1. Fork репозиторий
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в branch (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📞 Поддержка

Если у вас есть вопросы или предложения:
- 🐛 [Issues](https://github.com/your-username/api-doc-parser/issues)
- 💬 [Discussions](https://github.com/your-username/api-doc-parser/discussions)
- 📧 Email: your-email@example.com

## 🎯 Roadmap

- [ ] Поддержка других форматов документации (Word, HTML)
- [ ] REST API для интеграции
- [ ] Docker контейнеризация
- [ ] Облачное развертывание
- [ ] Поддержка OpenAPI 3.1
- [ ] Machine Learning улучшения

---

**⭐ Понравился проект? Поставьте звездочку!**

*Создано с ❤️ для сообщества разработчиков MCP серверов*