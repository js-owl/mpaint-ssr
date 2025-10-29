# Vue.js + FastAPI + Docker Compose

Fullstack приложение с Vue.js фронтендом и FastAPI backend, запущенное через Docker Compose.

## Структура проекта

```
├── frontend/              # Vue.js фронтенд
│   ├── src/
│   │   ├── App.vue       # Главный компонент Vue.js
│   │   └── main.ts       # Точка входа приложения
│   ├── index.html        # HTML шаблон
│   ├── package.json      # Зависимости Node.js
│   ├── tsconfig.json     # Конфигурация TypeScript
│   ├── tsconfig.node.json # Конфигурация TypeScript для Node.js
│   ├── vite.config.ts    # Конфигурация Vite
│   ├── Dockerfile        # Docker образ для сборки фронтенда
│   └── nginx.conf        # Конфигурация nginx
├── backend/              # FastAPI backend
│   ├── main.py          # Основной файл FastAPI приложения
│   └── requirements.txt  # Python зависимости
├── docker-compose.yml    # Docker Compose конфигурация
└── README.md            # Документация
```

## Запуск приложения

### С помощью Docker Compose (рекомендуется)

```bash
# Сборка и запуск
docker-compose up --build

# Запуск в фоновом режиме
docker-compose up -d --build

# Остановка
docker-compose down
```

После запуска:
- **Фронтенд**: http://localhost:8080
- **API**: http://localhost:8080/api/ (через nginx proxy)

### Локальная разработка

#### Фронтенд

```bash
# Перейти в папку frontend
cd frontend

# Установка зависимостей
npm install

# Запуск в режиме разработки
npm run dev

# Сборка для продакшена
npm run build

# Превью собранного приложения
npm run preview
```

#### Backend

```bash
# Перейти в папку backend
cd backend

# Установка зависимостей
pip install -r requirements.txt

# Запуск сервера разработки
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Или с автоперезагрузкой
uvicorn main:app --reload
```

После запуска FastAPI будет доступен по адресу: http://localhost:8000

Документация API (Swagger UI): http://localhost:8000/docs
Альтернативная документация (ReDoc): http://localhost:8000/redoc

## API Endpoints

- `GET /api/` - Hello world endpoint
- `GET /api/health` - Health check endpoint (если добавлен)

Все API запросы проксируются через nginx на `/api/` путь.

## Особенности

### Фронтенд
- ✅ Vue.js 3 с Composition API
- ✅ TypeScript для типизации
- ✅ Vite для быстрой сборки
- ✅ Nginx для статического сервера
- ✅ Docker многоэтапная сборка
- ✅ Оптимизированная конфигурация nginx
- ✅ Сжатие и кэширование
- ✅ Безопасность заголовков

### Backend
- ✅ FastAPI с автоматической документацией
- ✅ CORS middleware для работы с фронтендом
- ✅ Uvicorn ASGI сервер
- ✅ Docker контейнер с Python 3.11

## Команды Docker

```bash
# Просмотр логов всех сервисов
docker-compose logs -f

# Просмотр логов конкретного сервиса
docker-compose logs -f vue-app
docker-compose logs -f api

# Пересборка без кэша
docker-compose build --no-cache

# Перезапуск конкретного сервиса
docker-compose restart vue-app
docker-compose restart api

# Очистка
docker-compose down -v
docker system prune -f
```

## Структура Docker контейнеров

- **c_front** (vue-app): Vue.js приложение, обслуживаемое через nginx на порту 8080
- **c_back** (api): FastAPI backend на порту 8000 (внутренний доступ)
- **vue-network**: Сетевая мостовая сеть для взаимодействия между контейнерами

## Разработка

При разработке рекомендуется:
1. Для фронтенда использовать `npm run dev` (Vite dev server)
2. Для backend использовать `uvicorn main:app --reload` (автоперезагрузка)
3. Настроить прокси в `vite.config.ts` для проксирования API запросов на `http://localhost:8000`
