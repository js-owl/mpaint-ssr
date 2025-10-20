# Vue.js + TypeScript + Nginx + Docker Compose

Простое Vue.js приложение с TypeScript, запущенное в nginx через Docker Compose.

## Структура проекта

```
├── src/
│   ├── App.vue          # Главный компонент Vue.js
│   └── main.ts          # Точка входа приложения
├── index.html           # HTML шаблон
├── package.json         # Зависимости Node.js
├── tsconfig.json        # Конфигурация TypeScript
├── tsconfig.node.json   # Конфигурация TypeScript для Node.js
├── vite.config.ts       # Конфигурация Vite
├── Dockerfile           # Docker образ для сборки
├── nginx.conf           # Конфигурация nginx
├── docker-compose.yml   # Docker Compose конфигурация
└── .dockerignore        # Игнорируемые файлы для Docker
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

### Локальная разработка

```bash
# Установка зависимостей
npm install

# Запуск в режиме разработки
npm run dev

# Сборка для продакшена
npm run build
```

## Доступ к приложению

После запуска приложение будет доступно по адресу: http://localhost:8080

## Особенности

- ✅ Vue.js 3 с Composition API
- ✅ TypeScript для типизации
- ✅ Vite для быстрой сборки
- ✅ Nginx для статического сервера
- ✅ Docker многоэтапная сборка
- ✅ Оптимизированная конфигурация nginx
- ✅ Сжатие и кэширование
- ✅ Безопасность заголовков

## Команды Docker

```bash
# Просмотр логов
docker-compose logs -f

# Пересборка без кэша
docker-compose build --no-cache

# Очистка
docker-compose down -v
docker system prune -f
```
