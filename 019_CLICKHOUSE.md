# Clickhouse

Необходимо, используя туториал https://clickhouse.tech/docs/ru/getting-started/tutorial/ :
- развернуть БД;
- выполнить импорт тестовой БД;
- выполнить несколько запросов и оценить скорость выполнения.

В принципе результата запроса count(*) будет достаточно для ДЗ

Для тех кто хочет «усложнить себе жизнь»:
- запрос с фильтром по дате и группировкой по счетчику
- загрузить то же самое в PostgreSQL и сравнить
- развернуть ClickHouse ни с одним хостом, а кластером

__ВНИМАНИЕ__: в отчете заменил значания моих идентификаторов в Яндекс.Облаке на их "<ШАБЛОНЫ>"

## Реализация

Исходил из предложенного в https://cloud.yandex.ru/docs/cli/quickstart

### Это можно пропустить, обращая внимание только на "ВНИМАНИЕ"


```bash
curl https://storage.yandexcloud.net/yandexcloud-yc/install.sh | bash
```

__ВНИМАНИЕ__: в доке вроде нет, но после приведенной выше команды нужно `source "/home/<USER>/.bashrc"`.

https://oauth.yandex.ru/authorize?response_type=token&client_id=<МОЙ_КЛИЕНТ_ИД> 

В итоге вернет <МОЙ_ТОКЕН>

```bash
yc init

Welcome! This command will take you through the configuration process.
Pick desired action:
 [1] Re-initialize this profile 'test' with new settings 
 [2] Create a new profile
 [3] Switch to and re-initialize existing profile: 'default'
Please enter your numeric choice: 1
Please go to https://oauth.yandex.ru/authorize?response_type=token&client_id=<МОЙ_КЛИЕНТ_ИД> in order to obtain OAuth token.

Please enter OAuth token: <МОЙ_ТОКЕН>
Please select cloud to use: 
 [1] cloud-<YANDEX-ACCOUNT> (id = <CLOUD_ID_1>)
 [2] cloud-<YANDEX-ACCOUNT> (id = <CLOUD_ID_2>)
Please enter your numeric choice: 1
Your current cloud has been set to 'cloud-<YANDEX-ACCOUNT>' (id = <CLOUD_ID_1>).
Please choose folder to use:
 [1] default (id = <FOLDER_ID_2>)
 [2] Create a new folder
Please enter your numeric choice: 1
Your current folder has been set to 'default' (id = <FOLDER_ID_2>).
Do you want to configure a default Compute zone? [Y/n] Y
Please enter 'yes' or 'no': yes
Which zone do you want to use as a profile default?
 [1] ru-central1-a
 [2] ru-central1-b
 [3] ru-central1-c
 [4] Don't set default zone
Please enter your numeric choice: 1
Your profile default Compute zone has been set to 'ru-central1-a'.
```

Кластеров еще __НЕТ__, норм.

```bash
yc clickhouse cluster list
+----+------+------------+--------+--------+
| ID | NAME | CREATED AT | HEALTH | STATUS |
+----+------+------------+--------+--------+
+----+------+------------+--------+--------+

yc vpc subnet list
+----------------------+-----------------------+----------------------+----------------+---------------+-----------------+
|          ID          |         NAME          |      NETWORK ID      | ROUTE TABLE ID |     ZONE      |      RANGE      |
+----------------------+-----------------------+----------------------+----------------+---------------+-----------------+
| b0ch9cjskbb29h0qdnpb | default-ru-central1-c | enpro8qb0osobp7gmlg9 |                | ru-central1-c | [10.128.0.0/24] |
| e2l3m24i7rb9p89kbiui | default-ru-central1-b | enpro8qb0osobp7gmlg9 |                | ru-central1-b | [10.129.0.0/24] |
| e9bj8iga05joiktagkr6 | default-ru-central1-a | enpro8qb0osobp7gmlg9 |                | ru-central1-a | [10.130.0.0/24] |
+----------------------+-----------------------+----------------------+----------------+---------------+-----------------+

yc clickhouse cluster create --name <CLUSTER_NAME> --environment=production --network-name default --clickhouse-resource-preset s2.micro --host type=clickhouse,zone-id=ru-central1-a,subnet-id=e9bj8iga05joiktagkr6,assign-public-ip --clickhouse-disk-size 10 --clickhouse-disk-type network-ssd --user name=otus,password=<password> --database name=development

https://console.cloud.yandex.ru/folders/<FOLDER_ID_2>/managed-clickhouse/cluster/<CLUSTER_ID>?section=hosts&hostName=<HOST_NAME>.mdb.yandexcloud.net

<HOST_NAME>

```
<details>
<summary> Спойлер лога </summary>

```
done (4m47s)
id: <CLUSTER_ID>
folder_id: <FOLDER_ID_2>
created_at: "2020-12-16T20:14:31.654409Z"
name: <CLUSTER_NAME>
environment: PRODUCTION
monitoring:
- name: Console
  description: Console charts
  link: https://console.cloud.yandex.ru/folders/<FOLDER_ID_2>/managed-clickhouse/cluster/<CLUSTER_ID>?section=monitoring
config:
  version: "20.8"
  clickhouse:
    config:
      effective_config:
        log_level: DEBUG
        merge_tree:
          replicated_deduplication_window: "100"
          replicated_deduplication_window_seconds: "604800"
          parts_to_delay_insert: "150"
          parts_to_throw_insert: "300"
          max_replicated_merges_in_queue: "16"
          number_of_free_entries_in_pool_to_lower_max_size_of_merge: "8"
          max_bytes_to_merge_at_min_space_in_pool: "1048576"
        kafka: {}
        rabbitmq: {}
        max_connections: "4096"
        max_concurrent_queries: "500"
        keep_alive_timeout: "3"
        uncompressed_cache_size: "8589934592"
        mark_cache_size: "5368709120"
        max_table_size_to_drop: "53687091200"
        max_partition_size_to_drop: "53687091200"
        builtin_dictionaries_reload_interval: "3600"
        timezone: Europe/Moscow
        query_log_retention_size: "1073741824"
        query_log_retention_time: "2592000000"
        query_thread_log_enabled: true
        query_thread_log_retention_size: "536870912"
        query_thread_log_retention_time: "2592000000"
        part_log_retention_size: "536870912"
        part_log_retention_time: "2592000000"
        metric_log_enabled: true
        metric_log_retention_size: "536870912"
        metric_log_retention_time: "2592000000"
        trace_log_enabled: true
        trace_log_retention_size: "536870912"
        trace_log_retention_time: "2592000000"
        text_log_enabled: false
        text_log_retention_size: "536870912"
        text_log_retention_time: "2592000000"
        text_log_level: TRACE
      user_config: {}
      default_config:
        log_level: DEBUG
        merge_tree:
          replicated_deduplication_window: "100"
          replicated_deduplication_window_seconds: "604800"
          parts_to_delay_insert: "150"
          parts_to_throw_insert: "300"
          max_replicated_merges_in_queue: "16"
          number_of_free_entries_in_pool_to_lower_max_size_of_merge: "8"
          max_bytes_to_merge_at_min_space_in_pool: "1048576"
        kafka: {}
        rabbitmq: {}
        max_connections: "4096"
        max_concurrent_queries: "500"
        keep_alive_timeout: "3"
        uncompressed_cache_size: "8589934592"
        mark_cache_size: "5368709120"
        max_table_size_to_drop: "53687091200"
        max_partition_size_to_drop: "53687091200"
        builtin_dictionaries_reload_interval: "3600"
        timezone: Europe/Moscow
        query_log_retention_size: "1073741824"
        query_log_retention_time: "2592000000"
        query_thread_log_enabled: true
        query_thread_log_retention_size: "536870912"
        query_thread_log_retention_time: "2592000000"
        part_log_retention_size: "536870912"
        part_log_retention_time: "2592000000"
        metric_log_enabled: true
        metric_log_retention_size: "536870912"
        metric_log_retention_time: "2592000000"
        trace_log_enabled: true
        trace_log_retention_size: "536870912"
        trace_log_retention_time: "2592000000"
        text_log_enabled: false
        text_log_retention_size: "536870912"
        text_log_retention_time: "2592000000"
        text_log_level: TRACE
    resources:
      resource_preset_id: s2.micro
      disk_size: "10737418240"
      disk_type_id: network-ssd
  zookeeper:
    resources: {}
  backup_window_start:
    hours: 22
  access: {}
  cloud_storage: {}
  sql_database_management: false
  sql_user_management: false
network_id: enpro8qb0osobp7gmlg9
maintenance_window:
  anytime: {}

```
</details>

Кластер __теперь__ создан:

```bash
yc ––cluster-name <CLUSTER_NAME> database list
...
yc managed-clickhouse cluster <CLUSTER_NAME> database list
...
yc managed-clickhouse cluster list
...

yc clickhouse --cluster-name <CLUSTER_NAME> database list

+-------------+----------------------+
|    NAME     |      CLUSTER ID      |
+-------------+----------------------+
| development | <CLUSTER_ID>         |
+-------------+----------------------+
```

Устанвливаем клиент

```bash
echo "deb https://repo.clickhouse.tech/deb/stable/ main/" | sudo tee \
/etc/apt/sources.list.d/clickhouse.list 
yc config profile create test
```

Сертификаты

```bash
mkdir -p ~/.clickhouse-client /usr/local/share/ca-certificates/Yandex && \
wget "https://storage.yandexcloud.net/cloud-certs/CA.pem" -O /usr/local/share/ca-certificates/Yandex/YandexInternalRootCA.crt && \
wget "https://storage.yandexcloud.net/mdb/clickhouse-client.conf.example" -O ~/.clickhouse-client/config.xml
```

```text
--2020-12-16 23:31:45--  https://storage.yandexcloud.net/cloud-certs/CA.pem
Распознаётся storage.yandexcloud.net (storage.yandexcloud.net)… 213.180.193.243, 2a02:6b8::1d9
Подключение к storage.yandexcloud.net (storage.yandexcloud.net)|213.180.193.243|:443... соединение установлено.
HTTP-запрос отправлен. Ожидание ответа… 200 OK
Длина: 3579 (3,5K) [application/x-x509-ca-cert]
Сохранение в: «/usr/local/share/ca-certificates/Yandex/YandexInternalRootCA.crt»

/usr/local/share/ca-certificates/Yandex/Y 100%[===========>]   3,50K  --.-KB/s    за 0s      

2020-12-16 23:31:46 (32,9 MB/s) - «/usr/local/share/ca-certificates/Yandex/YandexInternalRootCA.crt» сохранён [3579/3579]

--2020-12-16 23:31:46--  https://storage.yandexcloud.net/mdb/clickhouse-client.conf.example
Распознаётся storage.yandexcloud.net (storage.yandexcloud.net)… 213.180.193.243, 2a02:6b8::1d9
Подключение к storage.yandexcloud.net (storage.yandexcloud.net)|213.180.193.243|:443... соединение установлено.
HTTP-запрос отправлен. Ожидание ответа… 200 OK
Длина: 497 [application/x-www-form-urlencoded]
Сохранение в: «/root/.clickhouse-client/config.xml»

/root/.clickhouse-client/config.xml       100%[===========>]     497  --.-KB/s    за 0s      

2020-12-16 23:31:46 (3,48 MB/s) - «/root/.clickhouse-client/config.xml» сохранён [497/497]
```

```bash
ls
config  create  profile  test  yc
```

### Подключаемся

```bash
clickhouse-client --host <HOST_NAME>.mdb.yandexcloud.net \
--secure \
--user otus \
--database development \
--port 9440 \
--ask-password

ClickHouse client version 18.16.1.
Password for user otus: 
Connecting to database development at <HOST_NAME>.mdb.yandexcloud.net:9440 as user otus.
Connected to ClickHouse server version 20.8.9 revision 54438.

<HOST_NAME>.mdb.yandexcloud.net :) 
```

__ВНИМАНИЕ__: через несколько дней, когда я решил продолжить эту ДЗ,   выдалось

```text
Code: 210. DB::NetException: SSL Exception: error:1416F086:SSL routines:tls_process_server_certificate:certificate verify failed (<HOST_NAME>.mdb.yandexcloud.net:9440, 84.201.135.196)
```

Зашел в Yandex.Cloud в `Managed Service for ClickHouse`->`Кластеры` и нажал `Подключиться`, во вкладке `Shell`. Грубо говоря, повторил действия из текущего отчета в части касающейся "Сертификаты"

```text
Connecting to database development at <HOST_NAME>.mdb.yandexcloud.net:9440 as user otus.
Connected to ClickHouse server version 20.8.9 revision 54438.

<HOST_NAME>.mdb.yandexcloud.net :) 
```

":)" - означает успешно подключились шеллом.

#### Проверка подключения на Python

Пока только ради [теста](./ch_test_select.py), далее это будет использовано в замере производительности выборки "СН vs. PG"

```python
import requests

def request(password):
    url = 'https://{host}:8443/?database={db}&query={query}'.format(
        host='<HOST_NAME>.mdb.yandexcloud.net',
        db='development',
        query='SELECT now()')
    auth = {
        'X-ClickHouse-User': 'otus',
        'X-ClickHouse-Key': password,
    }

    res = requests.get(
        url,
        headers=auth,
        verify='/usr/local/share/ca-certificates/Yandex/YandexInternalRootCA.crt')
    res.raise_for_status()
    return res.text

if __name__ == '__main__':
    password = input('Enter password: ')
    print(request(password))
```

### Набор данных из презентации Олега

```bash
curl https://clickhouse-datasets.s3.yandex.net/visits/tsv/visits_v1.tsv.xz | unxz --threads=`nproc` > visits_v1.tsv
```

```sqlite-sql
CREATE TABLE development.visits_v1
(
    CounterID UInt32, 
    StartDate Date, 
    Sign Int8, 
    IsNew UInt8, 
    VisitID UInt64, 
    UserID UInt64, 
    StartTime DateTime, 
    Duration UInt32, 
    UTCStartTime DateTime, 
    PageViews Int32, 
    Hits Int32, 
    IsBounce UInt8, 
    Referer String, 
    StartURL String, 
    RefererDomain String, 
    StartURLDomain String, 
    EndURL String, 
    LinkURL String, 
    IsDownload UInt8, 
    TraficSourceID Int8, 
    SearchEngineID UInt16, 
    SearchPhrase String, 
    AdvEngineID UInt8, 
    PlaceID Int32, 
    RefererCategories Array(UInt16), 
    URLCategories Array(UInt16), 
    URLRegions Array(UInt32), 
    RefererRegions Array(UInt32), 
    IsYandex UInt8, 
    GoalReachesDepth Int32, 
    GoalReachesURL Int32, 
    GoalReachesAny Int32, 
    SocialSourceNetworkID UInt8, 
    SocialSourcePage String, 
    MobilePhoneModel String, 
    ClientEventTime DateTime, 
    RegionID UInt32, 
    ClientIP UInt32, 
    ClientIP6 FixedString(16), 
    RemoteIP UInt32, 
    RemoteIP6 FixedString(16), 
    IPNetworkID UInt32, 
    SilverlightVersion3 UInt32, 
    CodeVersion UInt32, 
    ResolutionWidth UInt16, 
    ResolutionHeight UInt16, 
    UserAgentMajor UInt16, 
    UserAgentMinor UInt16, 
    WindowClientWidth UInt16, 
    WindowClientHeight UInt16, 
    SilverlightVersion2 UInt8, 
    SilverlightVersion4 UInt16, 
    FlashVersion3 UInt16, 
    FlashVersion4 UInt16, 
    ClientTimeZone Int16, 
    OS UInt8, 
    UserAgent UInt8, 
    ResolutionDepth UInt8, 
    FlashMajor UInt8, 
    FlashMinor UInt8, 
    NetMajor UInt8, 
    NetMinor UInt8, 
    MobilePhone UInt8, 
    SilverlightVersion1 UInt8, 
    Age UInt8, 
    Sex UInt8, 
    Income UInt8, 
    JavaEnable UInt8, 
    CookieEnable UInt8, 
    JavascriptEnable UInt8, 
    IsMobile UInt8, 
    BrowserLanguage UInt16, 
    BrowserCountry UInt16, 
    Interests UInt16, 
    Robotness UInt8, 
    GeneralInterests Array(UInt16), 
    Params Array(String), 
    Goals Nested(
        ID UInt32, 
        Serial UInt32, 
        EventTime DateTime, 
        Price Int64, 
        OrderID String, 
        CurrencyID UInt32
    ), 
    WatchIDs Array(UInt64), 
    ParamSumPrice Int64, 
    ParamCurrency FixedString(3), 
    ParamCurrencyID UInt16, 
    ClickLogID UInt64, 
    ClickEventID Int32, 
    ClickGoodEvent Int32, 
    ClickEventTime DateTime, 
    ClickPriorityID Int32, 
    ClickPhraseID Int32, 
    ClickPageID Int32, 
    ClickPlaceID Int32, 
    ClickTypeID Int32, 
    ClickResourceID Int32, 
    ClickCost UInt32, 
    ClickClientIP UInt32, 
    ClickDomainID UInt32, 
    ClickURL String, 
    ClickAttempt UInt8, 
    ClickOrderID UInt32, 
    ClickBannerID UInt32, 
    ClickMarketCategoryID UInt32, 
    ClickMarketPP UInt32, 
    ClickMarketCategoryName String, 
    ClickMarketPPName String, 
    ClickAWAPSCampaignName String, 
    ClickPageName String, 
    ClickTargetType UInt16, 
    ClickTargetPhraseID UInt64, 
    ClickContextType UInt8, 
    ClickSelectType Int8, 
    ClickOptions String, 
    ClickGroupBannerID Int32, 
    OpenstatServiceName String, 
    OpenstatCampaignID String, 
    OpenstatAdID String, 
    OpenstatSourceID String, 
    UTMSource String, 
    UTMMedium String, 
    UTMCampaign String, 
    UTMContent String, 
    UTMTerm String, 
    FromTag String, 
    HasGCLID UInt8, 
    FirstVisit DateTime, 
    PredLastVisit Date, 
    LastVisit Date, 
    TotalVisits UInt32, 
    TraficSource Nested(
        ID Int8, 
        SearchEngineID UInt16, 
        AdvEngineID UInt8, 
        PlaceID UInt16, 
        SocialSourceNetworkID UInt8, 
        Domain String, 
        SearchPhrase String, 
        SocialSourcePage String
    ), 
    Attendance FixedString(16), 
    CLID UInt32, 
    YCLID UInt64, 
    NormalizedRefererHash UInt64, 
    SearchPhraseHash UInt64, 
    RefererDomainHash UInt64, 
    NormalizedStartURLHash UInt64, 
    StartURLDomainHash UInt64, 
    NormalizedEndURLHash UInt64, 
    TopLevelDomain UInt64, 
    URLScheme UInt64, 
    OpenstatServiceNameHash UInt64, 
    OpenstatCampaignIDHash UInt64, 
    OpenstatAdIDHash UInt64, 
    OpenstatSourceIDHash UInt64, 
    UTMSourceHash UInt64, 
    UTMMediumHash UInt64, 
    UTMCampaignHash UInt64, 
    UTMContentHash UInt64, 
    UTMTermHash UInt64, 
    FromHash UInt64, 
    WebVisorEnabled UInt8, 
    WebVisorActivity UInt32, 
    ParsedParams Nested(
        Key1 String, 
        Key2 String, 
        Key3 String, 
        Key4 String, 
        Key5 String, 
        ValueDouble Float64
    ), 
    Market Nested(
        Type UInt8, 
        GoalID UInt32, 
        OrderID String, 
        OrderPrice Int64, 
        PP UInt32, 
        DirectPlaceID UInt32, 
        DirectOrderID UInt32, 
        DirectBannerID UInt32, 
        GoodID String, 
        GoodName String, 
        GoodQuantity Int32, 
        GoodPrice Int64
    ), 
    IslandID FixedString(16)
)
ENGINE = CollapsingMergeTree(Sign)
PARTITION BY toYYYYMM(StartDate)
ORDER BY (CounterID, StartDate, intHash32(UserID), VisitID)
SAMPLE BY intHash32(UserID)
SETTINGS index_granularity = 8192

```

__ВНИМАНИЕ__: не хватало прав в облаке

```bash
Received exception from server (version 20.8.9):
Code: 497. DB::Exception: Received from <HOST_NAME>.mdb.yandexcloud.net:9440, 84.201.135.196. DB::Exception: otus: Not enough privileges. To execute this query it's necessary to have the grant CREATE TABLE ON development.visits_v1. 

```

В веб-интерфейсе Yandex.Cloud добавил права пользователю `otus` на базу `development` и все пошло дальше.

#### Импорт набора

```text
cat visits_v1.tsv | clickhouse-client --host <HOST_NAME>.mdb.yandexcloud.net \
--secure \
--user otus \
--password nosql_2020 \
--database development \
--port 9440 \
--query "INSERT INTO development.visits_v1 FORMAT TSV" --max_insert_block_size=100000
```

#### Работа с импортированным набором

##### Число строк

```sqlite-sql
SELECT COUNT(*) FROM development.visits_v1
```

```text
#	COUNT()
0	1681077
```

```sqlite-sql
OPTIMIZE TABLE development.visits_v1 FINAL
SELECT COUNT(*) FROM development.visits_v1
```

```text
#	COUNT()
0	1676861
```

##### Выборка с группировкой по партициям

```sqlite-sql
SELECT StartDate, COUNT(CounterID) 
FROM development.visits_v1
GROUP BY (StartDate);
```

```text
#	StartDate	COUNT(CounterID)
0	"2014-03-17"	265120
1	"2014-03-18"	258925
2	"2014-03-19"	261624
3	"2014-03-20"	255336
4	"2014-03-21"	236290
5	"2014-03-22"	197354
6	"2014-03-23"	202212
```

##### Выборка с группировки и фильтацией

```sqlite-sql
SELECT StartDate, COUNT(CounterID) 
FROM development.visits_v1
WHERE  StartDate < toDate('2014-03-20')
GROUP BY (StartDate);
-- 
```

```text
#	StartDate	COUNT(CounterID)
0	"2014-03-17"	265120
1	"2014-03-18"	258925
2	"2014-03-19"	261624

```

## Сравнение с Postgres (пока в доработке, причина ниже)

Сделал отдельный скрипт импорта, который учитывает ["новый"](https://habr.com/ru/company/postgrespro/blog/353472/) подход в разбиении на партиции. Демонстрация ниже (даты партиций нам известны, с целью ускорения импортирую первые несколько столбцов, а не все), но она полностью с импортом включена в [скрипт](./019_CLICKHOUSE.files/pg_import.py).
 
```sqlite-sql
DROP TABLE development.visits CASCADE;

CREATE TABLE development.visits (
   counter_id bigint GENERATED BY DEFAULT AS IDENTITY,
   start_date date NOT NULL,
   sign integer, 
   isnew integer, 
   visit_id decimal, 
   user_id decimal, 
   start_time time, 
   duration integer
 ) PARTITION BY LIST (start_date);
 
CREATE TABLE visits_2014_03_17 PARTITION 
of development.visits FOR VALUES 
    IN ('2014-03-17');
CREATE TABLE visits_2014_03_18 PARTITION 
of development.visits FOR VALUES 
    IN ('2014-03-18');
CREATE TABLE visits_2014_03_19 PARTITION 
of development.visits FOR VALUES 
    IN ('2014-03-19');
CREATE TABLE visits_2014_03_20 PARTITION 
of development.visits FOR VALUES 
    IN ('2014-03-20');
CREATE TABLE visits_2014_03_21 PARTITION 
of development.visits FOR VALUES 
    IN ('2014-03-21');
CREATE TABLE visits_2014_03_22 PARTITION 
of development.visits FOR VALUES 
    IN ('2014-03-22');
CREATE TABLE visits_2014_03_23 PARTITION 
of development.visits FOR VALUES 
    IN ('2014-03-23');
```

### Сравнение скорости CH vs. PG

Создал PG-кластер на Яндексе. Минимальный.

https://cloud.yandex.ru/docs/managed-postgresql/operations/connect#configuring-an-ssl-certificate


```bash
yc managed-postgresql cluster create \
     --name mypg \
     --environment production \
     --network-name default \
     --resource-preset s2.micro \
     --host zone-id=ru-central1-c,subnet-id=b0ch9cjskbb29h0qdnpb \
     --disk-type network-ssd \
     --disk-size 10GB \
     --user name=user1,password=password1 \
     --database name=db1,owner=user1
```

```text
done (4m50s)
id: c9qhkok519g1ioqq6u0f
folder_id: b1gujct7m4g2klh9sne2
created_at: "2020-12-22T19:22:04.793341Z"
name: mypg
environment: PRODUCTION
monitoring:
- name: Console
  description: Console charts
  link: https://console.cloud.yandex.ru/folders/b1gujct7m4g2klh9sne2/managed-postgresql/cluster/c9qhkok519g1ioqq6u0f?section=monitoring
config:
  version: "10"
  postgresql_config_10:
    effective_config:
      max_connections: "400"
      shared_buffers: "2147483648"
      temp_buffers: "8388608"
      max_prepared_transactions: "0"
      work_mem: "4194304"
      maintenance_work_mem: "67108864"
      replacement_sort_tuples: "150000"
      autovacuum_work_mem: "-1"
      temp_file_limit: "-1"
      vacuum_cost_delay: "0"
      vacuum_cost_page_hit: "1"
      vacuum_cost_page_miss: "10"
      vacuum_cost_page_dirty: "20"
      vacuum_cost_limit: "200"
      bgwriter_delay: "200"
      bgwriter_lru_maxpages: "100"
      bgwriter_lru_multiplier: 2
      backend_flush_after: "0"
      old_snapshot_threshold: "-1"
      wal_level: WAL_LEVEL_LOGICAL
      synchronous_commit: SYNCHRONOUS_COMMIT_ON
      checkpoint_timeout: "300000"
      checkpoint_completion_target: 0.5
      max_wal_size: "1073741824"
      min_wal_size: "536870912"
      max_standby_streaming_delay: "30000"
      default_statistics_target: "1000"
      constraint_exclusion: CONSTRAINT_EXCLUSION_PARTITION
      cursor_tuple_fraction: 0.1
      from_collapse_limit: "8"
      join_collapse_limit: "8"
      force_parallel_mode: FORCE_PARALLEL_MODE_OFF
      client_min_messages: LOG_LEVEL_NOTICE
      log_min_messages: LOG_LEVEL_WARNING
      log_min_error_statement: LOG_LEVEL_ERROR
      log_min_duration_statement: "-1"
      log_checkpoints: false
      log_connections: false
      log_disconnections: false
      log_duration: false
      log_error_verbosity: LOG_ERROR_VERBOSITY_DEFAULT
      log_lock_waits: false
      log_statement: LOG_STATEMENT_NONE
      log_temp_files: "-1"
      search_path: '"$user", public'
      row_security: true
      default_transaction_isolation: TRANSACTION_ISOLATION_READ_COMMITTED
      statement_timeout: "0"
      lock_timeout: "0"
      idle_in_transaction_session_timeout: "0"
      bytea_output: BYTEA_OUTPUT_HEX
      xmlbinary: XML_BINARY_BASE64
      xmloption: XML_OPTION_CONTENT
      gin_pending_list_limit: "4194304"
      deadlock_timeout: "1000"
      max_locks_per_transaction: "64"
      max_pred_locks_per_transaction: "64"
      array_nulls: true
      backslash_quote: BACKSLASH_QUOTE_SAFE_ENCODING
      default_with_oids: false
      escape_string_warning: true
      lo_compat_privileges: false
      operator_precedence_warning: false
      quote_all_identifiers: false
      standard_conforming_strings: true
      synchronize_seqscans: true
      transform_null_equals: false
      exit_on_error: false
      seq_page_cost: 1
      random_page_cost: 1
      autovacuum_max_workers: "3"
      autovacuum_vacuum_cost_delay: "45"
      autovacuum_vacuum_cost_limit: "700"
      archive_timeout: "30000"
      enable_bitmapscan: true
      enable_hashagg: true
      enable_hashjoin: true
      enable_indexscan: true
      enable_indexonlyscan: true
      enable_material: true
      enable_mergejoin: true
      enable_nestloop: true
      enable_seqscan: true
      enable_sort: true
      enable_tidscan: true
      max_worker_processes: "8"
      max_parallel_workers: "8"
      max_parallel_workers_per_gather: "2"
      autovacuum_vacuum_scale_factor: 0.00001
      autovacuum_analyze_scale_factor: 0.0001
      default_transaction_read_only: false
      timezone: Europe/Moscow
      effective_io_concurrency: "1"
      effective_cache_size: "107374182400"
    user_config: {}
    default_config:
      max_connections: "400"
      shared_buffers: "2147483648"
      temp_buffers: "8388608"
      max_prepared_transactions: "0"
      work_mem: "4194304"
      maintenance_work_mem: "67108864"
      replacement_sort_tuples: "150000"
      autovacuum_work_mem: "-1"
      temp_file_limit: "-1"
      vacuum_cost_delay: "0"
      vacuum_cost_page_hit: "1"
      vacuum_cost_page_miss: "10"
      vacuum_cost_page_dirty: "20"
      vacuum_cost_limit: "200"
      bgwriter_delay: "200"
      bgwriter_lru_maxpages: "100"
      bgwriter_lru_multiplier: 2
      backend_flush_after: "0"
      old_snapshot_threshold: "-1"
      wal_level: WAL_LEVEL_LOGICAL
      synchronous_commit: SYNCHRONOUS_COMMIT_ON
      checkpoint_timeout: "300000"
      checkpoint_completion_target: 0.5
      max_wal_size: "1073741824"
      min_wal_size: "536870912"
      max_standby_streaming_delay: "30000"
      default_statistics_target: "1000"
      constraint_exclusion: CONSTRAINT_EXCLUSION_PARTITION
      cursor_tuple_fraction: 0.1
      from_collapse_limit: "8"
      join_collapse_limit: "8"
      force_parallel_mode: FORCE_PARALLEL_MODE_OFF
      client_min_messages: LOG_LEVEL_NOTICE
      log_min_messages: LOG_LEVEL_WARNING
      log_min_error_statement: LOG_LEVEL_ERROR
      log_min_duration_statement: "-1"
      log_checkpoints: false
      log_connections: false
      log_disconnections: false
      log_duration: false
      log_error_verbosity: LOG_ERROR_VERBOSITY_DEFAULT
      log_lock_waits: false
      log_statement: LOG_STATEMENT_NONE
      log_temp_files: "-1"
      search_path: '"$user", public'
      row_security: true
      default_transaction_isolation: TRANSACTION_ISOLATION_READ_COMMITTED
      statement_timeout: "0"
      lock_timeout: "0"
      idle_in_transaction_session_timeout: "0"
      bytea_output: BYTEA_OUTPUT_HEX
      xmlbinary: XML_BINARY_BASE64
      xmloption: XML_OPTION_CONTENT
      gin_pending_list_limit: "4194304"
      deadlock_timeout: "1000"
      max_locks_per_transaction: "64"
      max_pred_locks_per_transaction: "64"
      array_nulls: true
      backslash_quote: BACKSLASH_QUOTE_SAFE_ENCODING
      default_with_oids: false
      escape_string_warning: true
      lo_compat_privileges: false
      operator_precedence_warning: false
      quote_all_identifiers: false
      standard_conforming_strings: true
      synchronize_seqscans: true
      transform_null_equals: false
      exit_on_error: false
      seq_page_cost: 1
      random_page_cost: 1
      autovacuum_max_workers: "3"
      autovacuum_vacuum_cost_delay: "45"
      autovacuum_vacuum_cost_limit: "700"
      archive_timeout: "30000"
      enable_bitmapscan: true
      enable_hashagg: true
      enable_hashjoin: true
      enable_indexscan: true
      enable_indexonlyscan: true
      enable_material: true
      enable_mergejoin: true
      enable_nestloop: true
      enable_seqscan: true
      enable_sort: true
      enable_tidscan: true
      max_worker_processes: "8"
      max_parallel_workers: "8"
      max_parallel_workers_per_gather: "2"
      autovacuum_vacuum_scale_factor: 0.00001
      autovacuum_analyze_scale_factor: 0.0001
      default_transaction_read_only: false
      timezone: Europe/Moscow
      effective_io_concurrency: "1"
      effective_cache_size: "107374182400"
  resources:
    resource_preset_id: s2.micro
    disk_size: "10737418240"
    disk_type_id: network-ssd
  autofailover: true
  backup_window_start:
    hours: 22
  access: {}
  performance_diagnostics:
    sessions_sampling_interval: "60"
    statements_sampling_interval: "600"
network_id: enpro8qb0osobp7gmlg9
maintenance_window:
  anytime: {}

```

__ВНИМАНИЕ__: не выходит подключиться, так как хост `rc1c-p8y8xsux30mu6sb9.mdb.yandexcloud.net` не известен. Я хз почему не определяется его IP и оне не пингуется и пр.

```bash
psql "host=rc1c-7bo98d6h39ne64t8.mdb.yandexcloud.net \
      port=6432 \
      sslmode=verify-full \
      dbname=db1 \
      user=user1 \
      target_session_attrs=read-write"
```

```text
rc1c-7bo98d6h39ne64t8.mdb.yandexcloud.net: Неизвестное имя или служба

```

Чnо хотел сравнить, засекая время в питоне

CH:
```sqlite-sql
SELECT StartDate, COUNT(CounterID) 
FROM development.visits_v1
GROUP BY (StartDate);
```

vs. PG:
```sqlite-sql
SELECT start_date, COUNT(*) 
FROM development.visits
GROUP BY (start_date);
```