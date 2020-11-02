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

__Дополнительно__:
- возврат из Offline в Online

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

1. Удалил пару документов из списка при выключенном сервере, получил остаток
2. Включил ранее остановленный CouchDB
3. Не сразу, но в конце концов документы, удаленные в п.1, исчезли и в CouchDB (без Sync или обновления страницы).


## Материалы по теме

- https://github.com/regnete/howto-couchdb-cluster-docker-compose


## Воспросы 

### 1. по тексту изложения:
#### 1.1 какие логин-пароль по умолчанию?

Их не должно быть, надо еще раз попробовать собрать докер
        
Пробую
 
```bash
version: "2"

services:
  otus008:
    container_name: otus008_couchdb_2
    restart: always
    image: couchdb:latest
    ports:
      - 25984:5984
    volumes:
      - "/media/raid_1_4tb/portainer/data/otus_008_couchdb_2/opt/couchdb/data:/opt/couchdb/data"
      - "/media/raid_1_4tb/portainer/data/otus_008_couchdb_2/opt/couchdb/etc/local.d:/opt/couchdb/etc/local.d"
```

Ошибка в логе

```bash
*************************************************************
ERROR: CouchDB 3.0+ will no longer run in "Admin Party"
       mode. You *MUST* specify an admin user and
       password, either via your own .ini file mapped
       into the container at /opt/couchdb/etc/local.ini
       or inside /opt/couchdb/etc/local.d, or with
       "-e COUCHDB_USER=admin -e COUCHDB_PASSWORD=password"
       to set it via "docker run".
*************************************************************

```

Пробую так

```bash
version: "2"

services:
  otus008_couchdb_2:
    restart: always
    image: couchdb:latest
    ports:
      - 25984:5984
    volumes:
      - "/media/raid_1_4tb/portainer/data/otus_008_couchdb_4/opt/couchdb/data:/opt/couchdb/data"
    environment:
      - COUCHDB_USER=admin
      - COUCHDB_PASSWORD=admin
```

ошибка в логе `because the _users database does not exist`

```text[notice] 2020-11-02T07:04:12.759488Z nonode@nohost <0.254.0> -------- rexi_buffer : cluster stable[notice] 2020-11-02T07:04:13.631844Z nonode@nohost <0.324.0> -------- chttpd_auth_cache changes listener died because the _users database does not exist. Create the database to silence this notice.[error]  2020-11-02T07:04:13.632218Z nonode@nohost emulator -------- Error in process <0.551.0> with exit value:
    {database_does_not_exist,[{mem3_shards,load_shards_from_db,"_users",[{file,"src/mem3_shards.erl"},{line,399}]},{mem3_shards,load_shards_from_disk,1,[{file,"src/mem3_shards.erl"},{line,374}]},{mem3_shards,load_shards_from_disk,2,[{file,"src/mem3_shards.erl"},{line,403}]},{mem3_shards,for_docid,3,[{file,"src/mem3_shards.erl"},{line,96}]},{fabric_doc_open,go,3,[{file,"src/fabric_doc_open.erl"},{line,39}]},{chttpd_auth_cache,ensure_auth_ddoc_exists,2,[{file,"src/chttpd_auth_cache.erl"},{line,198}]},{chttpd_auth_cache,listen_for_changes,1,[{file,"src/chttpd_auth_cache.erl"},{line,145}]}]}
```
[Тут](https://github.com/apache/couchdb-docker/issues/54) говорят так

```bash
curl -X PUT http://192.168.102.99:25984/_users

```

Стучимся браузером `http://192.168.102.99:25984/`

```json
{"couchdb":"Welcome","version":"3.1.1","git_sha":"ce596c65d","uuid":"f6e1c07a9210e4c252ae1c99acd0ff2c","features":["access-ready","partitioned","pluggable-storage-engines","reshard","scheduler"],"vendor":{"name":"The Apache Software Foundation"}}
```

Все норм.

Пробуем

```bash
curl -X PUT http://192.168.102.99:25984/_users
```

Ответ (нужен админ)

```json
{"error":"unauthorized","reason":"You are not a server admin."}
```

Создаем

```bash
curl -X PUT http://admin:admin@192.168.102.99:25984/_users
{"ok":true}
curl -X PUT http://admin:admin@192.168.102.99:25984/_replicator
{"ok":true}
curl -X PUT http://admin:admin@192.168.102.99:25984/_global_changes
{"ok":true}
```

Log докера (вроде без ошибок).

<details><summary>спойлер лога</summary>

```text
[info] 2020-11-02T07:25:03.412848Z nonode@nohost <0.11.0> -------- Application couch_log started on node nonode@nohost
[info] 2020-11-02T07:25:03.427243Z nonode@nohost <0.11.0> -------- Application folsom started on node nonode@nohost
[info] 2020-11-02T07:25:03.476586Z nonode@nohost <0.11.0> -------- Application couch_stats started on node nonode@nohost
[info] 2020-11-02T07:25:03.476638Z nonode@nohost <0.11.0> -------- Application khash started on node nonode@nohost
[info] 2020-11-02T07:25:03.486732Z nonode@nohost <0.11.0> -------- Application couch_event started on node nonode@nohost
[info] 2020-11-02T07:25:03.486774Z nonode@nohost <0.11.0> -------- Application hyper started on node nonode@nohost
[info] 2020-11-02T07:25:03.495927Z nonode@nohost <0.11.0> -------- Application ibrowse started on node nonode@nohost
[info] 2020-11-02T07:25:03.504509Z nonode@nohost <0.11.0> -------- Application ioq started on node nonode@nohost
[info] 2020-11-02T07:25:03.504544Z nonode@nohost <0.11.0> -------- Application mochiweb started on node nonode@nohost
[info] 2020-11-02T07:25:03.511107Z nonode@nohost <0.216.0> -------- Preflight check: Asserting Admin Account
[info] 2020-11-02T07:25:03.515556Z nonode@nohost <0.216.0> -------- Apache CouchDB 3.1.1 is starting.
[info] 2020-11-02T07:25:03.515621Z nonode@nohost <0.217.0> -------- Starting couch_sup
[info] 2020-11-02T07:25:03.596502Z nonode@nohost <0.216.0> -------- Apache CouchDB has started. Time to relax.
[info] 2020-11-02T07:25:03.600326Z nonode@nohost <0.11.0> -------- Application couch started on node nonode@nohost
[info] 2020-11-02T07:25:03.600462Z nonode@nohost <0.11.0> -------- Application ets_lru started on node nonode@nohost
[notice] 2020-11-02T07:25:03.623446Z nonode@nohost <0.249.0> -------- rexi_server : started servers
[notice] 2020-11-02T07:25:03.627526Z nonode@nohost <0.253.0> -------- rexi_buffer : started servers
[info] 2020-11-02T07:25:03.627693Z nonode@nohost <0.11.0> -------- Application rexi started on node nonode@nohost
[notice] 2020-11-02T07:25:03.734674Z nonode@nohost <0.283.0> -------- mem3_reshard_dbdoc start init()
[notice] 2020-11-02T07:25:03.742756Z nonode@nohost <0.285.0> -------- mem3_reshard start init()
[notice] 2020-11-02T07:25:03.742844Z nonode@nohost <0.286.0> -------- mem3_reshard db monitor <0.286.0> starting
[notice] 2020-11-02T07:25:03.746547Z nonode@nohost <0.285.0> -------- mem3_reshard starting reloading jobs
[notice] 2020-11-02T07:25:03.746641Z nonode@nohost <0.285.0> -------- mem3_reshard finished reloading jobs
[info] 2020-11-02T07:25:03.747695Z nonode@nohost <0.11.0> -------- Application mem3 started on node nonode@nohost
[info] 2020-11-02T07:25:03.747774Z nonode@nohost <0.11.0> -------- Application fabric started on node nonode@nohost
[info] 2020-11-02T07:25:03.790699Z nonode@nohost <0.11.0> -------- Application chttpd started on node nonode@nohost
[info] 2020-11-02T07:25:03.808122Z nonode@nohost <0.11.0> -------- Application couch_index started on node nonode@nohost
[info] 2020-11-02T07:25:03.808153Z nonode@nohost <0.11.0> -------- Application couch_mrview started on node nonode@nohost
[info] 2020-11-02T07:25:03.808311Z nonode@nohost <0.11.0> -------- Application couch_plugins started on node nonode@nohost
[info] 2020-11-02T07:25:03.907855Z nonode@nohost <0.11.0> -------- Application couch_replicator started on node nonode@nohost
[info] 2020-11-02T07:25:03.922330Z nonode@nohost <0.11.0> -------- Application couch_peruser started on node nonode@nohost
[info] 2020-11-02T07:25:03.939589Z nonode@nohost <0.11.0> -------- Application ddoc_cache started on node nonode@nohost
[info] 2020-11-02T07:25:03.953713Z nonode@nohost <0.11.0> -------- Application dreyfus started on node nonode@nohost
[info] 2020-11-02T07:25:03.976710Z nonode@nohost <0.11.0> -------- Application global_changes started on node nonode@nohost
[info] 2020-11-02T07:25:03.976739Z nonode@nohost <0.11.0> -------- Application jiffy started on node nonode@nohost
[info] 2020-11-02T07:25:03.990750Z nonode@nohost <0.11.0> -------- Application jwtf started on node nonode@nohost
[info] 2020-11-02T07:25:04.010613Z nonode@nohost <0.11.0> -------- Application ken started on node nonode@nohost
[info] 2020-11-02T07:25:04.026336Z nonode@nohost <0.11.0> -------- Application mango started on node nonode@nohost
[info] 2020-11-02T07:25:04.036817Z nonode@nohost <0.11.0> -------- Application setup started on node nonode@nohost
[info] 2020-11-02T07:25:04.073180Z nonode@nohost <0.11.0> -------- Application smoosh started on node nonode@nohost
[info] 2020-11-02T07:25:04.073298Z nonode@nohost <0.11.0> -------- Application snappy started on node nonode@nohost
[info] 2020-11-02T07:25:04.073334Z nonode@nohost <0.11.0> -------- Application recon started on node nonode@nohost
[notice] 2020-11-02T07:25:08.833653Z nonode@nohost <0.339.0> -------- couch_replicator_clustering : cluster stable
[notice] 2020-11-02T07:25:08.843381Z nonode@nohost <0.366.0> -------- Started replicator db changes listener <0.473.0>
[info] 2020-11-02T07:25:08.844682Z nonode@nohost <0.475.0> -------- open_result error {not_found,no_db_file} for _replicator
[notice] 2020-11-02T07:25:18.623612Z nonode@nohost <0.249.0> -------- rexi_server : cluster stable
[notice] 2020-11-02T07:25:18.624531Z nonode@nohost <0.253.0> -------- rexi_buffer : cluster stable
```

</details>

Но все равно пока от передачи пары логин пароль никуда не деться

```bash
curl -X PUT http://admin:admin@192.168.102.99:25984/otus008test
{"ok":true}

curl -X GET http://192.168.102.99:25984/otus008test
{"error":"unauthorized","reason":"You are not authorized to access this db."}

```

В админке Fauxton пишет 
```text
Database members can access the database. If no members are defined, the database is public. 
```[png](./008_COUCHDB_POUCHDB.files/1.1.png)

Нужно удалить роль `_admin` (снизу справа) и база наконец-то станет публичной и не будет требовать логин-пароль (хоть браузером открывай)

```bash
curl -X GET http://192.168.102.99:25984/otus008test
```

ответ

```json
{"db_name":"otus008test","purge_seq":"0-g1AAAABPeJzLYWBgYMpgTmHgzcvPy09JdcjLz8gvLskBCeexAEmGBiD1HwiyEhlwqEtkSKqHKMgCAIT2GV4","update_seq":"2-g1AAAABPeJzLYWBgYMpgTmHgzcvPy09JdcjLz8gvLskBCeexAEmGBiD1HwiyEhlxqEtkSKqHKMgCAIUbGWA","sizes":{"file":24884,"external":0,"active":0},"props":{},"doc_del_count":0,"doc_count":0,"disk_format_version":8,"compact_running":false,"cluster":{"q":2,"n":1,"w":1,"r":1},"instance_start_time":"0"}
```

Решено.


#### 1.2 как собрать контейнер сразу standalone?

Плохая идея для масштабирования.

Ok. Тогда надо решать п. 1.1, так как standalone именно и решало 1.2

#### 1.3 как разрешить CORS для локальных файлов, работающих автономно, без ВЕБ-сервера?

Это только при *

Ok. 

### 2. как в `index.html` реализовать `ORDER BY` по полю `name` для выводимых документов?

```
Либо использовать /_find передав sort в JSON запросе, 
либо отсортировать на стороне клиента средствами JS. 
Можно ещё использовать функцию map, 
И ещё создать отдельный view с функцией сортировки
```

Отлично!
