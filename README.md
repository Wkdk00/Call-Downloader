# Call Downloader
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red.svg)](https://sqlalchemy.org)
[![Alembic](https://img.shields.io/badge/Alembic-1.12+-yellow.svg)](https://alembic.sqlalchemy.org)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.3+-brightgreen.svg)](https://vuejs.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://postgresql.org)
[![Redis](https://img.shields.io/badge/Redis-7.2+-red.svg)](https://redis.io)
[![RabbitMQ](https://img.shields.io/badge/RabbitMQ-3.12+-ff6a00.svg)](https://rabbitmq.com)
[![Prometheus](https://img.shields.io/badge/Prometheus-2.47+-e6522c.svg)](https://prometheus.io)
[![Grafana](https://img.shields.io/badge/Grafana-10.1+-orange.svg)](https://grafana.com)
[![Docker](https://img.shields.io/badge/Docker-24.0+-blue.svg)](https://docker.com)
[![Docker Compose](https://img.shields.io/badge/Docker%20Compose-2.22+-blue.svg)](https://docs.docker.com/compose/)
[![HTTPX](https://img.shields.io/badge/HTTPX-0.25+-green.svg)](https://www.python-httpx.org)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.4+-blue.svg)](https://pydantic-docs.helpmanual.io)
[![FastStream](https://img.shields.io/badge/FastStream-0.3.5+-8A2BE2.svg)](https://faststream.airt.ai)

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
