# UGC


## Additional services
Для того, чтобы ручки обрабатывались успешно (авторизация, проверка наличия фильма), необходимо запустить сервисы аутентификации и авторизации:
1. https://github.com/elina-chertova/movies_auth, auth
2. https://github.com/elina-chertova/movies_async_api

* Auth - 127.0.0.1/5000

* Movies - 127.0.0.1/8004

## Documentation
```angular2html
http://0.0.0.0:8003/api/openapi
```

## Testing

After launching Clickhouse + UGC service + ETL + Auth + Movies, run
```angular2html
pytest .
```

