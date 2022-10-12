# Парсер

Для конфигуриции используется `.env` файл.

Для подключения с базе добавьте в него переменную `DB_CONNECTION`

Например: `DB_CONNECTION=postgresql://user:password@127.0.0.1:5432/parser`

Список прокси должен лежать в `proxies.txt`

## Запуск

```sh
cd deploy

docker-compose up
```

Внутри контейнера

```sh
# парсинг заданной категории
scrapy crawl kolesa-spider -a 'page=https://kolesa.kz/cars/vaz/'

# парсинг деталей
scrapy crawl single-spider -a 'detail=https://kolesa.kz/a/show/141671671'
```
