# Парсер

Для конфигурации используется `.env` файл.

Для подключения к базе добавьте в него переменную `DB_CONNECTION`

Список прокси должен лежать в `proxies.txt`

## Запуск

```sh
cd deploy

docker-compose up
```

## Запуск вручную

Перед запуском вручную рекомендуется отключить автоматический запуск парсера. Для этого достаточно убрать `volume` конфига для `supervisor` в `docker-compose.yml`

Внутри контейнера:

```sh
# парсинг заданной категории
pdm run scrapy crawl kolesa-spider -a 'page=https://kolesa.kz/cars/vaz/'

# парсинг детализации
pdm run scrapy crawl single-spider -a 'detail=https://kolesa.kz/a/show/141671671'
```
~~~~