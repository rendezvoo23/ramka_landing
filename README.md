# РАМКА

Лендинг сервиса РАМКА: интерьерная концепция по плану или фотографии квартиры, подбор реальных товаров и ориентир бюджета.

## Запуск

```bash
bun install
bun run dev
```

## Проверка сборки

```bash
bun run build
bun run test:sites
```

## Продакшен

Сборка и два процесса через PM2 на порту `4173` (или `PORT`):

```bash
bun install
bun run build
bunx pm2 start ecosystem.config.cjs
bunx pm2 save
bunx pm2 startup
```

Перезапуск без простоя: `bun run pm2:reload`. Остановка: `bun run pm2:stop`.

Форма раннего доступа встроена через Яндекс Формы. Её адрес настраивается в `src/App.jsx`.
