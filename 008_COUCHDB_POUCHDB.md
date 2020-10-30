# Знакомство с CouchDB + PouchDB

__Цель__: Результат ДЗ - файл с синхронизированными в offline данными из CouchDB. 

В рамках выполнения ДЗ нужно сделать первое offline-first приложение.
- Установить CouchDB или Couchbase – не важно как и куда
- Скачать файл index.html из материалов к занятию
- Создать БД в CouchDB
- Добавить в БД один документ в котором должно быть поле «name», в него запишите свою фамилию.
- Прописать в index.html путь к вашей инсталляции CouchDB или Couchbase
- Запустить index.html и нажать кнопку «sync». Убедиться что ваша фамилия появилась на экране. При необходимости настроить CORS.
- Остановить CouchDB/Couchbase сервер
- Обновить Index.html, нажать sync, убедиться что в нём по прежнему фигурирует Ваша фамилия
- Прислать либо сохраненный из chrome (уже с прочитанной фамилией) index.html, либо опубликовать его, к примеру, на githubpages и прислать ссылку.

## Установить CouchDB

Я использовал `docker-compose.yml` для "Portainer.io" (см. ранее мою заметку о [Portainer](./101_PORTAINER.md)) 

```bash
version: "2"

services:
  otus008:
    container_name: otus008_couchdb
    restart: always
    image: couchdb:latest
    ports:
      - 15984:5984
    volumes:
      - "/media/raid_1_4tb/portainer/data/otus_008/opt/couchdb/data:/opt/couchdb/data"
      - "/media/raid_1_4tb/portainer/data/otus_008/opt/couchdb/etc/local.d:/opt/couchdb/etc/local.d"
    environment:
      - COUCHDB_USER=admin
      - COUCHDB_PASSWORD=user
```

И развернул "CouchDB" __ВРУЧНУЮ__ (далее будет об этом вопрос) в Standalone-режиме `http://192.168.102.99:15984/_utils/#setup`.

Проверил готовность инсталляции `http://192.168.102.99:15984/_utils/#/verifyinstall`.

Все готово

### Воспрос №1 в рамках исполнения пункта

__Как реализовать автоматическое разворачивания CouchDB в Standalone-режиме?__

При установке с использованием Docker Compose возникала ошибка в том, что при запуске у CouchDB не хватало баз:

- _users
- _replicator
- _global_changes

которые необходимы в Standalone-режиме CouchDB.

Исходя из документации [https://hub.docker.com/_/couchdb](https://hub.docker.com/_/couchdb)

```text
If you choose not to use the Cluster Setup wizard or API, 
you will have to create _global_changes, _replicator and _users manually.
```

и [https://docs.couchdb.org/en/stable/install/docker.html](https://docs.couchdb.org/en/stable/install/docker.html)

```text
Your installation is not complete. Be sure to complete the Setup steps 
for a single node or clustered installation.
```

и [https://docs.couchdb.org/en/stable/setup/single-node.html](https://docs.couchdb.org/en/stable/setup/single-node.html)

```text
 if you don’t want to use the Setup Wizard or set that value, 
 and run 3.x as a single node with a server administrator already configured 
 via config file (https://docs.couchdb.org/en/stable/config/auth.html#config-admins), 
 make sure to create the three system databases manually on startup:
    > curl -X PUT http://127.0.0.1:5984/_users
    > curl -X PUT http://127.0.0.1:5984/_replicator
    > curl -X PUT http://127.0.0.1:5984/_global_changes
```

необходимо создать их самостоятельно, инициализировав CouchDB для работы в Standalone-режиме (Configure a Single Node) 
через ВЕБ-интерфейс (кнопкой, `http://192.168.102.99:15984/_utils/#setup`).
 
Я __НЕ СМОГ__ каким-либо образом это автоматизировать с использованием `docker-compose.yml`. Пожалуйста, подскажите (как?).

Вариации в `docker-compose.yml` на тему 
```
    command: '/bin/bash -x -c "curl -X PUT http://user:user@localhost:5984/_users"'
    command: '/bin/bash -x -c "curl -X PUT http://user:user@localhost:5984/_replicator"'
    command: '/bin/bash -x -c "curl -X PUT http://user:user@localhost:5984/_global_changes"'
```
мне не помогли.


### Воспрос №2 в рамках исполнения пункта

__Какие по-умолчанию логин и пароль администратора CouchDB?__ 

Изначально, логины-пароли, какие-либо из опубликованных в документации, к экземпляру CouchDB не подходили.
Имеется возможность сброса пароля, но это через досуп к файлу в контейнере (сдишком много возни).
Но проще оказалось (пере-)определить в `docker-compose.yml` значения соотвествующих переменных окружения

```bash
    ...
    environment:
      - COUCHDB_USER=admin
      - COUCHDB_PASSWORD=user
```
хотя логин-пароль по умолчанию хотелось бы знать (какой он?).


## Скачать файл index.html из материалов к занятию

Скачал

## Создать БД в CouchDB

Создал БД через REST API:
```bash
curl -X PUT http://admin:user@192.168.102.99:15984/database
```
Ответ на команду:
```text
{"ok":true}
```

Через Веб-интерфейс проверил наличия созданной БД в списке:

```bash
http://192.168.102.99:15984/_utils/#/_all_dbs
```

## Добавить в БД один документ в котором должно быть поле «name», в него запишите свою фамилию.

Добавил через REST API:
```bash
curl -X PUT http://admin:user@192.168.102.99:15984/database/001 -d '{"name":"Pupkin","course":"Otus2020-NoSQL"}'
```
Ответ на команду:
```text
{"ok":true,"id":"001","rev":"1-0c8c59a6959ba21e7a645d4077862075"}
```
_Заметка_: 
```
в качестве `id` документа может быть произвольное значение, например, `database/id_1`. 
Только с пробельными символами в `id`, напрмер, `database/"a b"` -  не вышло.
```

## Прописать в index.html путь к вашей инсталляции CouchDB или Couchbase

Прописал
```text
    new PouchDB('http://admin:user@192.168.102.99:15984/database')
```

## Запустить index.html и нажать кнопку «sync». Убедиться что ваша фамилия появилась на экране. При необходимости настроить CORS.


### Взял смелость добавить интерактивности 

Поправил немного код JS

```bash
addBtn.addEventListener('click', () => {
    const item = { name: new Date()}
    DBS.Local.post(item)
    <!-- Добавил: Обновит список сразу, без нажатия Sync -->
    fetch()
})

removeBtn.addEventListener('click', () => {
    const item = data.pop()
    if (! item) return
    DBS.Local.remove(item)
    <!-- Добавил: Обновит список сразу, без нажатия Sync -->
    fetch()
})

<!-- Добавит интерактивности при Offline -->
    .on('change', ({ change }) => {
        const doc = change.docs[0]
        console.log('change doc', doc)
        if (doc._deleted) {
          data = data.filter(item => item._id != doc._id)
          <!-- Перенес сюда строку -->
          render(data)
        } else {
          data = data.concat(doc)
        }
      <!-- Перенес отсюда исходную строку -->
      })

<!-- Добавил: Отрисует данные сразу при загрузке страницы -->
fetch()
```

### Включил CORS

Включил `http://192.168.102.99:15984/_utils/#_config/nonode@nohost/cors` для `All domains ( * )`, 
потому что для файла, открытого локально на компе (без запуска через веб сервер на localhost домене), 
не смог (а это вообще возможно?) задать принудительно `file:///home` (Please enter a valid domain, starting with http/https.)

## Остановить CouchDB/Couchbase сервер

Остановил контейнер

## Обновить Index.html, нажать sync, убедиться что в нём по прежнему фигурирует Ваша фамилия

Обновил страницу. Убедился, что в списке записей по прежнему фигурирует моя фамилия. 
Нажимать Sync нет необходимости в силу внесенных мной изменений в JS. Но нажал - все осталось.

## Прислать либо сохраненный из chrome (уже с прочитанной фамилией) index.html, либо опубликовать его, к примеру, на githubpages и прислать ссылку.

[PouchDB.html](./008_COUCHDB_POUCHDB.files/PouchDB.html)
![png](./008_COUCHDB_POUCHDB.files/PouchDB.png)

## Дополнительно

### Проверка выхода из Оффлайн-режима

1. Удадли пару документов из списка при выключенном сервере, получил остаток
2. Включил ранее остановленный CouchDB
3. Не сразу, но в конце концов документы, удаленные в п.1, удалились и в CouchDB (без Sync или обновления страницы).


## Материалы по теме

- https://github.com/regnete/howto-couchdb-cluster-docker-compose


## Воспросы 

 - по тексту изложения:
    - какие логин-пароль по умолчанию?
    - как собрать контейнер сразу standalone?
    - как разрешить CORS для локальных файлов, работающих автономно, без ВЕБ-сервера?
 - как в `index.html` реализовать `ORDER BY` по полю `name` для выводимых документов?
