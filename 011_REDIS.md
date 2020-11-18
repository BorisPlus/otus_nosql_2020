# Redis

Домашнее задание. Необходимо:
- сохранить большой жсон (~20МБ) в виде разных структур:
    - строка 
    - hset 
    - zset 
    - list
- протестировать скорость сохранения и чтения
- предоставить отчет

* настроить редис кластер на 3х нодах с отказоусточивостью, затюнить таймоуты
Критерии оценки: Критерии оценки:
- задание выполнено - 5 баллов
- предложено красивое решение - плюс 1 балл
- предложено рабочее решение, но не устранены недостатки, указанные преподавателем - минус 1 балл
Рекомендуем сдать до: 27.11.2020

/usr/local/etc/redis/redis.conf

## Json Data

[https://data.gov.ru/opendata/7704786030-municipalroutesregister](Реестр муниципальных маршрутов регулярных перевозок пассажиров и багажа автомобильным и наземным электрическим транспортом в городе Москве) и [(данные json(60.29 МБ)](https://data.gov.ru/sites/default/files/opendata/7704786030-MunicipalRoutesRegister/data-2017-07-18T00-00-00-structure-2017-07-18T00-00-00.json)

Структура:
 - "system_object_id":("STRING"),
 - "CarrierName" ("STRING", Наименование юридического лица или индивидуального предпринимателя, осуществляющего перевозки пассажиров по маршруту"),
 - "global_id" ("NUMBER"),
 - "RouteNumber" ("STRING", "Номер маршрута"),
 - "DirectRouteTrack" ("STRING", "Координаты прямого трека маршрута"),
 - "ReverseTrackOfFollowing" ("STRING", "Трасса следования маршрута (обратное направление)"),
 - "is_deleted" ("NUMBER"),
 - "signature_date" ("STRING"),
 - "ReverseRouteTrack" ("STRING", "Координаты обратного трека маршрута"),
 - "TrackOfFollowing" ("STRING", "Трасса следования маршрута (прямое направление)"),
 - "RouteName" ("STRING", "Наименование маршрута"),
 - "ID" ("INTEGER", "Код"),
 - "TypeOfTransport" ("DICTIONARY", "Вид транспорта").
 
## Поставить зависимости

```bash
pip3 install -r ./011.files/req.txt 
```

## Время на вставку даннных

[Cкрипт](011.files/loader.py)

```bash
python3 loader.py 

    string
    STRING: 0.30866003036499023 ms
    https://redis.io/commands/hset
    HSET: 0.30942511558532715 ms
    https://redis.io/commands/zadd
    ZADD: 0.3056464195251465 ms
    https://redis.io/commands/lpush
    LPUSH: 0.32759571075439453 ms
```


