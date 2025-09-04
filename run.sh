#!/bin/bash

# Загружаем переменные окружения
source .env

# Активируем виртуальную среду
source venv/bin/activate

# Копируем PDF файл (укажите правильный путь)
# cp /путь/к/вашему/documentation.pdf ./documentation.pdf

# Запускаем парсер
python3 fleethead_parser.py