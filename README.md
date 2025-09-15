# Call Downloader
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.6+-purple.svg)](https://github.com/langchain-ai/langgraph)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-orange.svg)](https://openai.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)
Проект call_downloader выступает как микросервис-прокладка и интеграционный уровень между двумя бизнес-системами и отдельным микросервисом с искусственным интеллектом. Он обеспечивает:
- Приём и обработку аудиофайлов от одного бизнес-приложения
- Надёжное хранение и асинхронную обработку данных
- Взаимодействие с микросервисом ИИ, который выполняет специализированный анализ или обработку аудио,
- Передачу результатов обратно во второе бизнес-приложение.

Таким образом, этот микросервис служит связующим звеном, упрощая интеграцию и разграничивая ответственность между различными бизнес-сервисами и ИИ-компонентом, что повышает масштабируемость и управляемость всей системы.

## Установка и запуск

### Требования

- Docker и Docker Compose
- Git

### Клонирование репозитория
```bash
git clone https://github.com/Wkdk00/call_downloader.git
cd call_downloader
```

### Запуск через Docker Compose
```bash
docker compose up --build
```

## Технологии

### Backend
- **FastAPI** - современный Python фреймворк для веб-API
- **Uvicorn** - ASGI-сервер для запуска FastAPI
- **SQLAlchemy** - ORM для работы с базой данных
- **Alembic** - система миграций базы данных
- **JWT (python-jose)** - аутентификация через JSON Web Tokens
- **BCrypt (passlib)** - хеширование паролей
  
### Frontend
- **Vue.js** - фреймворк для построения пользовательского интерфейса
- **Vue Router** - маршрутизация для SPA
- **Axios** - HTTP-клиент для API запросов
- **Nginx** - веб-сервер для раздачи статических файлов
- **Node.js** - среда выполнения для сборки фронтенда

### Базы данных и очереди
- **PostgreSQL** - реляционная база данных для хранения файлов и пользователей
- **Redis** - in-memory база данных для временного хранения файлов
- **RabbitMQ** - брокер сообщений для обработки очередей

### Мониторинг и метрики
- **Prometheus** - система мониторинга и сбора метрик
- **Grafana** - платформа для визуализации метрик
- **prometheus-fastapi-instrumentator** - инструмент для сбора метрик из FastAPI

### Обработка медиа
- **Mutagen** - библиотека для анализа аудиофайлов (определение длительности MP3)

### Инфраструктура
- **Docker** - контейнеризация приложения
- **Docker Compose** - оркестрация многоконтейнерного приложения
- **Nginx** - reverse proxy и балансировщик нагрузки

### Вспомогательные технологии
- **HTTPX** - асинхронный HTTP-клиент
- **Pydantic** - валидация данных и сериализация
- **FastStream** - фреймворк для работы с RabbitMQ
