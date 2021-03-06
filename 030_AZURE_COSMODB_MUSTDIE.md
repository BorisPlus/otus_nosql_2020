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

    {"code":"Unauthorized","message":"Required Header authorization is missing. 
    Ensure a valid Authorization token is passed.\r\nActivityId: 92c10a96-e68a-4110-a22a-1cd65115b347, 
    Microsoft.Azure.Documents.Common/2.11.0"}
```

Говорит нужен токен авторизации.

Случайным образом нашел, что в некоторых разделах докуметации можно запусить REST запрос из самого брацзера. В разделе Cosmos DB таких кнопок нет, хотя там тоже приводятся методы GET\POST\PUT запросов

Вот тут есть зеленая кнопка "Try It"
https://docs.microsoft.com/en-us/rest/api/authorization/classicadministrators/list

Пофявится фрейм 'Try the REST API with the inputs below'.
и внизу есть нужный заголовок для REST запроса

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Im5PbzNaRHJPRFhF...
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

Мое мнение, пример должен быть более базовым. Разбираться в обращении его к Азуру? Сначала тогда человеку нужно поднять опыт по Flask. Я писал на нем приложения, но это не пример. 
Должен быть более базовый.

Есть еще библиотеки 
https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/cosmos/azure-cosmos#create-a-database

А теперь самое на мой взгляд важное.

Идем в панель учетки, где создали базу данных 

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
import time

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
start = time.time()
meteorites.insert_many(data)
print('Size: ', len(data))
print('Time left: ', time.time() - start, 'sec')
```

Все! Данные загружены программно.

```text
Size:  1000
Time left:  21.05442810058593 sec
```

Я - хз. Столько таргета - модели, рест и гибкость. И в итоге все стандартным только `pymongo` и получилось.

Майкрософт - ты такой... майкрософт.