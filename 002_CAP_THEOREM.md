# CAP теорема - домашнее задание

от 2020.10.07

__Цель:__ в результате выполнения ДЗ вы научитесь работать с гитом.

__Необходимо:__ написать к каким системам по CAP теореме относятся перечисленные БД и почему: mongoDB, MSSQL, Cassandra. ДЗ сдается ссылкой на гит, где расположен миниотчет в маркдауне.

__Критерии оценки:__

- задание выполнено - 5 баллов
- предложено красивое решение - плюс 1 балл
- предложено рабочее решение, но не устранены недостатки, указанные преподавателем - минус 1 балл

__Рекомендуем сдать до:__ 09.10.2020

## Описание

CAP теорема - это описание наличия у системы хранения данных следующих свойств ([источник](https://ru.wikipedia.org/wiki/Теорема_CAP)):

* __согласованность__ (англ. _consistency_) данных — во всех вычислительных узлах в один момент времени данные не противоречат друг другу;
* __доступность__ (англ. _availability_) данных  — любой запрос к распределённой системе завершается корректным откликом, однако без гарантии, что ответы всех узлов системы совпадают;
* __устойчивость к разделению__ (англ. _partition tolerance_) данных — расщепление распределённой системы на несколько изолированных секций не приводит к некорректности отклика от каждой из секций.


## Решение (если коротко)


+/- | MongoDB | MSSQL | Cassandra
------------ | -------------| -------------| -------------
__согласованность данных__ | + | + | -
__доступность__ | - | + | +
__устойчивость к разделению__ | + | - | + | 


## Пояснение к решению

### MongoDB - это CP

(приступили к изучению на курсе). 

- (почему __C__) исходя из документации? высокая согласованность достигается с помощью "multi-document" механизма транзакций ([источник](https://www.mongodb.com/blog/post/multi-document-transactions)). 

_Мое примечание_: мне видится, вообще, где есть слово "транзакция", то это уже говорит о способности данных быть "согласованными", в том числе возможности реализации их строгой согласованности.

- (почему __P__) я так понял, что при принудительном физическом разделении хранилищ-"клонов" на независимые сегменты, есть вожмосность настройки автоматического перехода базы данных из Slave режима в режим Мастера для этого обособленного сегмента.  

- (почему все таки __не A__) главным посылом является то, что в случае физического разделения сети, система в целом прекратит принимать запросы, пока не убедится, что может безопасно завершить их. Она сможет продолжать работу, но без доступности выявленного узла со "сбоем".

_Мое примечание_: нашел отличное рассуждение о месте MongoDB в CAP "треугольнике" ([источник](https://stackoverflow.com/a/44440201)).

### Microsoft SQL - это CA

- (почему __C__) можно добиться согласованности даннных, настроив доставку журналов транзакции на реплики хранилища или задействовав механизм "зеркального отображения базы данных" ([источник](https://docs.microsoft.com/ru-ru/sql/database-engine/database-mirroring/database-mirroring-sql-server?view=sql-server-ver15)).

```text
В сценарии зеркального отражения базы данных каждое изменение в базе данных (основной базе данных) 
немедленно воспроизводится в ее полной автономной копии (зеркальной базе данных). 
Экземпляр основного сервера немедленно отсылает каждую запись журнала в экземпляр зеркального сервера, 
который применяет входящие записи к зеркальной базе данных, путем ее непрерывного наката. 
```

Что удивительно, исходя из описания:

```text
Зеркальное отображение базы данных — это решение, нацеленное на повышение доступности базы данных SQL Server. 
Зеркальное отображение каждой базы данных осуществляется отдельно и работает только с теми базами данных, 
которые используют модель полного восстановления.
```

оно ("зеркальное отображение") нацелено __не__ на согласованность данных, а на доступность, и:

```text
В будущей версии Microsoft SQL Server этот компонент будет удален. Избегайте использования этого компонента 
в новых разработках и запланируйте изменение существующих приложений, в которых он применяется. 
Вместо этого используйте Группы доступности AlwaysOn.
```

- (почему __A__) как описано выше, к высокой доступности MSSQL-хранилище стремится за счет использования "зеркального отображения базы данных" ([источник](https://docs.microsoft.com/ru-ru/sql/database-engine/database-mirroring/database-mirroring-sql-server?view=sql-server-ver15)) или "группы доступности AlwaysOn"([источник](https://docs.microsoft.com/ru-ru/sql/database-engine/availability-groups/windows/overview-of-always-on-availability-groups-sql-server?view=sql-server-ver15), [источник](https://docs.microsoft.com/ru-ru/sql/database-engine/availability-groups/windows/always-on-availability-groups-sql-server?view=sql-server-ver15)). 

_Мое примечание_: в действительности доступность узла MSSQL обычно обеспечивается не только какими-то внутренними механизмами самой базы данных, но и задействованием специальных кластерных служб Microsoft Server и определенной аппаратной инфраструктуры. Так, например, база данных может работать на кластерной службе Microsoft Server (дополнительное обеспечение "доступности" на программном уровне) и использовать отдельную дисковую корзину (дополнительное обеспечение "доступности" на аппаратном уровне) для нескольких физических серверов (да, еще у них будут диск кворума, сетевая служба и пр). При этом MSSQL имеет свой IP-адрес, отдельный от этих ЭВМ. И если выключить рабочую ноду (к которой прикреплены в текущий момент ресурсы кластерной службы), то сервис перейдет на резервную ноду кластера (и диск кворума, и корзина, и IP-адрес сетевой MSSQL), а при восстановлении первой - вернется на нее обратно (тут на самом деле большая _боль_ "внедряльщика", который бы как практик при абсолютной надежности сети отверг реализуемость __A__ в решении MSSQL).  

- (почему __не P__) расщепление распределённой системы на несколько изолированных секций __приводит__ к некорректности отклика от секций. При подключении к одному экземпляру MSSQL, чтобы сделать JOIN с таблицей другого экземпляра? необходимо использовать специальные SQL-конструкции внутри формируемого SQL запроса (по типу как DBLINK в PostgreSQL). Кроме этого репликация согласованности происходит в строгом направлении "мастер" -> "слейв", а значит и узлы не равнозначны - не независимости друг от друга.

### Cassandra - это AP

(на курсе еще не было) 

- (почему __A__) это самый главный посыл в ее реализации - узлы кластера кассандры равноценны, подключаясь к люому из них можно прозрачным образом поучать полные данные. 

_Мое примечание_: я для себя определил, что Cassanrdra это как "сетевой" RAID "на прикладном уровне". Такая ассоциация (назову ее "RAID-аллегория") очень способствует пониманию ее архитектуры, и используется мною в последующем.

- (почему __P__) исходя из описания ([источник](https://habr.com/ru/post/155115/)), система хранения Cassandra имеет возможность настройки стратегии распределения данных в зависимости от "ключа" данных. Новый узел для хранения (срабатывает моя "RAID-аллегория") добавляется также прозрачно, как диск в работоспособный (но не избыточный по дискам) RAID-массив - данные перераспределяются по узлам, как они распределяются по RAID-дискам. Кроме того имеется возможность настройки Master-Master.

- (почему все-таки __не C__) я вижу, что __строгая согласованность данных может быть обеспечена___. Так, для записи и чтения данных существует значение опции уровня согласованности — __ALL__ — когда координатор дожидается подтверждения от всех узлов-реплик, то есть когда так называемый "кворум" в Cassandra - это __абсолютное единогласие__. Но этот __ALL__ влияет на общую доступность, так как происходят блокировки, что сказывается на самом главном посыле (см. п __A__) в реализации Cassandra. Поэтому чаще применяют стратегию "кворума" (_N+1_ узлов из _2N+1_ должны ответить об успехе на чтение\запись), что уже никак не обеспечивает строгую согласованность данных. Это как (срабатывает моя "RAID-аллегория") достать диск из RAID-массива (только не RAID1, а RAID0 или RAID5 или пр.), ведь там фактически не будет данных с других дисков изначального массива, то есть данные - несогласованы.

## 
