# Azure Cosmos DB

Необходимо:
- одну из облачных БД заполнить данными (любыми из предыдущих дз);
- протестировать скорость запросов.

*сравнить 2-3 облачных NoSQL по скорости загрузки данных и времени выполнения запросов.

## Как я хотел просто программно загрузить данные

Пытаюсь организовать работу c Azure Cosmos DB посредством его RESTFUL Api
https://docs.microsoft.com/ru-ru/rest/api/azure/ 

В документации https://docs.microsoft.com/en-us/rest/api/cosmos-db/#supported-rest-api-versions говорится о необходимости передачи HTTP-заголовка `x-ms-version`.

```text
Supported REST API Versions

The following table lists the supported REST API versions by the Azure Cosmos DB service. 
The version must be specified via the x-ms-version header in every request. If not specified,
 the service defaults to the latest version 2017-02-22.
```

Попробуем получить список баз данных (они заранее созданы вручную мной через веб)

https://docs.microsoft.com/en-us/rest/api/cosmos-db/list-databases

В документации приводится о необходимости еще заголовков https://docs.microsoft.com/en-us/rest/api/cosmos-db/common-cosmosdb-rest-response-headers

```python
import requests

response = requests.get(
    'https://otus.documents.azure.com/dbs',
    headers={
        'x-ms-version': '2018-12-31'
    },
)
print(response.status_code)
print(response.text)
```
вывод таков
```text
401
{"code":"Unauthorized","message":"Required Header authorization is missing. Ensure a valid Authorization token is passed.\r\nActivityId: 92c10a96-e68a-4110-a22a-1cd65115b347, Microsoft.Azure.Documents.Common/2.11.0"}
```

Говорит нужен токен авторизации.

Случайным образом нашел, что в некоторых разделах докуметации можно запусить REST запрос из самого брацзера. В разделе Cosmos DB таких кнопок нет, хотя там тоже приводятся методы GET\POST\PUT запросов

Вот тут есть зеленая кнопка "Try It"
https://docs.microsoft.com/en-us/rest/api/authorization/classicadministrators/list

Пофявится фрейм 'Try the REST API with the inputs below'.
и внизу есть нужный заголовок для REST запроса

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Im5PbzNaRHJPRFhFSzFqS1doWHNsSFJfS1hFZyIsImtpZCI6Im5PbzNaRHJPRFhFSzFqS1doWHNsSFJfS1hFZyJ9.eyJhdWQiOiJodHRwczovL21hbmFnZW1lbnQuY29yZS53aW5kb3dzLm5ldC8iLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC80MWQ5ODM2Ni05MmZjLTQ2ZDAtYTg0NC1jMDk3MjUyYmY1YjYvIiwiaWF0IjoxNjEzMjg3Njg0LCJuYmYiOjE2MTMyODc2ODQsImV4cCI6MTYxMzI5MTU4NCwiYWNyIjoiMSIsImFpbyI6IkFVUUF1LzhUQUFBQTI4Qzg5RjkvdFZtUXJSWXpuOHJ5eWkxc3U5Q2JrczAweGFkVlZjb2E3QUdNNHRDeFA5UUU0c1N5S2hRZzh2WFJlZ21CU2NXU3FPSUlYc3haeWYzZGR3PT0iLCJhbHRzZWNpZCI6IjE6bGl2ZS5jb206MDAwMzAwMDAzODYyQjA3QSIsImFtciI6WyJwd2QiXSwiYXBwaWQiOiI3ZjU5YTc3My0yZWFmLTQyOWMtYTA1OS01MGZjNWJiMjhiNDQiLCJhcHBpZGFjciI6IjIiLCJlbWFpbCI6ImJvcmlzb3YtaWxpYUB5YW5kZXgucnUiLCJmYW1pbHlfbmFtZSI6ItCR0L7RgNC40YHQvtCyIiwiZ2l2ZW5fbmFtZSI6ItCY0LvRjNGPIiwiZ3JvdXBzIjpbIjgwYmYyYjU3LWFkMmEtNGJjNS04OGZjLWExNDI3MjUwYjA1NCJdLCJpZHAiOiJsaXZlLmNvbSIsImlwYWRkciI6Ijc4LjM2L
```

Все понятно. Но не понятно КАК получить Bearer? как автризоваться? Где этот метод API по авторизации?

Имеется раздел https://docs.microsoft.com/ru-ru/rest/api/apimanagement/apimanagementrest/azure-api-management-rest-api-authentication

там ссылка на статью https://docs.microsoft.com/ru-ru/rest/api/apimanagement/apimanagementrest/api-management-rest

честно... меня дальше не хватило.


Иду прям в Cosmos DB. Хочу узнать как с монгой на Python работать.

Раздел "API MongoDB" -> "Краткие руководства" -> "Python"

https://docs.microsoft.com/ru-ru/azure/cosmos-db/create-mongodb-flask

Предлагают для того, чтобы попробовать клонировать репозиторий с Фласк-веб-приложением
```shell
git clone https://github.com/Azure-Samples/CosmosDB-Flask-Mongo-Sample.git
```

Мое мнение, пример должен быть более базовым. Разбираться в обращении его к Аузуру? Сначала тогде человеку нужно полнять опыт по Flask. Честно, я писал не нем приложения, но это не пример. Должен быть более базовым.

Есть еще библиотеки 
https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/cosmos/azure-cosmos#create-a-database

А теперь самое на мой взгляд важное

Идем в панель учетки вашей, где высоздали базу данных 
"Учетная запись Azure Cosmos DB" -> "Быстрый запуск"
"Поздравляем! Учетная запись Azure Cosmos DB для API MongoDB создана."

и видим их предложение "Для работы с Azure Cosmos DB можно использовать существующий драйвер MongoDB Python."
Отлично. Наконец я на программном уровне могу загрузтить туда свою коллекцию, думаю я. 
Но НЕТ!!!!!

Вдруг `pymongo` просит внести дополнительный заголовок в подключение к MongoDB

```
&retrywrites=false
```

Без него работать НЕ будет. Где это сказано, где описано... 

```python
import pymongo
import json

data_file = '../003_MONGODB.files/y77d-th95.json'
with open(data_file) as f:
    data = json.load(f)
    # print(data)

uri = (
    "mongodb://otus:<MY_SECRET>@"
    "otus.mongo.cosmos.azure.com:10255/"
    "?ssl=true&replicaSet=globaldb"
    "&maxIdleTimeMS=120000"
    "&appName=@otus@"
    "&retrywrites=false"  # !!! NEED 
)
client = pymongo.MongoClient(uri)
db = client.meteorites_2020

meteorites = db.meteorites
meteorites.create_index("id", unique=True)
```

Я - хз. Столько таргета - модели, рест и гибкость. И в итоге все стандартным только `pymongo` и получилось.

Майкрософт - ты такой... майкрософт.