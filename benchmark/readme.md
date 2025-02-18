# Выбор хранилища

## Установка зависимостей
```angular2html
pip install -r requirements.txt
```

## OLAP хранилище
Для исследования по выбору OLAP хранилища выбрано 2 БД: Vertica и ClickHouse.
Результаты анализа можно найти в `ugc/benchmark/OLAP_research/reasearch.ipynb`.
Хранилище будет использовано для хранения данных о просмотре фильмов пользователем.

## Хранилище для пользовательских данных

### MongoDB

```angular2html
cd ugc/benchmark/storage/MongoDB
docker-compose up -d

<!-- Настройка кластера -->
bash configuration.sh

<!--Настройка БД и коллекций -->
bash database.sh
```

### ClickHouse
```angular2html
cd ugc/benchmark/storage/Clickhouse
docker-compose up -d
```

## Рабочие файлы
Файл для генерации данных: `ugc/benchmark/storage/data_generation.ipynb`.

Файл для тестирования: `ugc/benchmark/storage/research.ipynb`.



## Результаты тестирования
### INSERT


| INSERT  (batch)       | MongoDB  | ClickHouse |
|-----------------------|----------|------------|
| Rating    (200k/500k) | 1min 26s | 44.5 s     |
| Review      (100k)    | 8.2 s    | 2.57 s     |
| Bookmarks   (100k)    | 13.8 s   | 1.16 s     |


Загрузка 100000 ед. данных по одной строке.

| MongoDB | ClickHouse |
|---------|------------|
| 4min 3s | ~20min     |

### SELECT


1. Средний рейтинг по конкретному фильму.

| MongoDB | ClickHouse |
|---------|------------|
| 491 ms  | 130 ms     |


2. Закладки конкретного пользователя (В MongoDB 200к записей, в ClickHouse 500к).

| MongoDB | ClickHouse |
|---------|------------|
| 26.7 ms | 32.9 ms    |

3. Количество положительных отметок у конкретного фильма.

| MongoDB | ClickHouse |
|---------|------------|
| 726 ms  | 212 ms     |

### SELECT ALL

| SELECT  (*)           | MongoDB | ClickHouse |
|-----------------------|---------|------------|
| Rating    (200k/500k) | 30.8 s  | 3min 2s    |
| Review      (100k)    | 3.12 s  | 1.05 s     |
| Bookmarks   (100k)    | 973 ms  | 908 ms     |


### INSERT AND SELECT

| MongoDB | ClickHouse |
|---------|------------|
| 198 ms  | 89.9 ms    |




## Выбор БД
Рассмотрим все случаи.

Есть три задачи, под которые выбирается оптимальная база данных.

#### Закладки пользователя
В рамках данной задачи предполагаем следующее: 
* В сутки добавляется незначительное количество закладок.
* Пользователь должен моментально видеть, что фильм добавлен в закладки.

Основываясь на данных ограничениях, видно, что предпочтительнее использовать MongoDB, 
поскольку загрузка единицы данных занимает в ~5-6 раз меньше времени, чем Clickhouse.
Хотя MongoDB ищет данные одному полю чуть медленней, пользователь это не увидит, 
поскольку разница минимальна.



#### Рейтинги
В рамках данной задачи предполагаем следующее: 
* В сутки оценивается незначительное количество фильмов.
* Пользователю необходимо сразу видеть свою оценку фильма.
* Средний рейтинг должен рассчитываться очень быстро.
* Количество положительных/отрицательных отметок у конкретного фильма.

Исходя из первых 2х пунктов, опираемся на предыдущий вывод: MongoDB подходит лучше/на уровне с Clickhouse.
По последним 2м пунктам лучший выбор - Clickhouse, поскольку при большом объеме данных работает минимум в 5 раз быстрее 
Clickhouse, не выходя за рамки начального ограничения в 200ms.

#### Рецензии
В рамках данной задачи предполагаем следующее:
* В сутки добавляется незначительное количество рецензий.
* Необязательно моментально отображать рецензию.

Как и в первом случае MongoDB и ClickHouse практически эквивалентны по использованию.

В том числе, что касается загрузки и считывания данных друг за другом, ClickHouse также работает быстрее, хотя и обе БД укладываются в ограничения в 200ms.

Однако как используемая БД будет MongoDB в целях более глубокого освоения.



