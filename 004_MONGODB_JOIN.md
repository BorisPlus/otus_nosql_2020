# Реализация JOIN в MongoDB

Написано для разрешения возникшего с моей стороны непонимания, как происходит JOIN выборка в MongoDB.

- покажу, что `lookup` - это "не совсем LEFT"
- покажу, как из "не совсем LEFT" сделать INNER

[Официальный документ](https://docs.mongodb.com/manual/reference/operator/aggregation/lookup)

## Пример

Расширим пример из документации [https://docs.mongodb.com/manual/reference/operator/aggregation/lookup/#examples](https://docs.mongodb.com/manual/reference/operator/aggregation/lookup/#examples)

```json
db.orders.drop()
db.orders.insert([
    { "_id" : 1, "item" : "almonds", "price" : 12, "quantity" : 2 },
    { "_id" : 2, "item" : "pecans", "price" : 20, "quantity" : 1 },
    { "_id" : 3  },
    { "_id" : 4, "item" : "test", "price" : 25, "quantity" : 1 },
    { "_id" : 5, "item" : "pecans", "price" : 25, "quantity" : 1 },
])
db.orders.find()

db.inventory.drop()
db.inventory.insert([
        { "_id" : 1, "sku" : "almonds", "description": "product 1", "instock" : 120 },
        { "_id" : 2, "sku" : "bread", "description": "product 2", "instock" : 80 },
        { "_id" : 3, "sku" : "cashews", "description": "product 3", "instock" : 60 },
        { "_id" : 4, "sku" : "pecans", "description": "product 4", "instock" : 70 },
        { "_id" : 5, "sku": null, "description": "Incomplete 5" },
        { "_id" : 6 },
])
db.inventory.insert(
        { "_id" : 10, "sku" : "pecans", "description": "product 7", "instock" : 70 },
)
db.inventory.insert(
        { "_id" : 11, "sku" : "pecans", "description": "product 8", "instock" : 70 }
)
db.inventory.find()
```

## Осуществляем сопоставление `orders` и `inventory`

Да, это действительно __похоже__ на LEFT соединение (в документации приводится аналогия с IN в SQL):
 
```json
db.orders.aggregate([
    {
        $lookup: {
            from: "inventory",
            localField: "item",
            foreignField: "sku",
            as: "inventories"
        }
    }
])
```

Но это не совсем так, разберем выборку "строк" (документов), прокомментироваав каждую из них:

`

`отобралось, так как "item" == "almonds" и "sku" == "almonds" и "item" == "sku"`

{ "_id" : 1, __"item" : "almonds"__, "price" : 12, "quantity" : 2, "inventories" : [ 
    { "_id" : 1, __"sku" : "almonds"__, "description" : "product 1", "instock" : 120 } 
] }


`отобралось, так как "item" == "pecans" и "sku" == "pecans" и "item" == "sku"`

{ "_id" : 2, __"item" : "pecans"__, "price" : 20, "quantity" : 1, "inventories" : [ 
    { "_id" : 4, __"sku" : "pecans"__, "description" : "product 4", "instock" : 70 }, 
    { "_id" : 10, __"sku" : "pecans"__, "description" : "product 7", "instock" : 70 }, 
    { "_id" : 11, __"sku" : "pecans"__, "description" : "product 8", "instock" : 70 } 
] }


`отобралось, __так как__ "item" == NULL и "sku" == NULL и как бы "item" == "sku"
пожалуйста, запомните именно эту строку (*)
вот именно из-за ЭТОЙ строки эта выборка не является привычным LEFT соединением
в SQL значения NULL не сопоставляются, (__NULL не равен ничему, к нему необходимо применять ISNULL__) 
(см. пример для PostgreSQL ниже) `

{ "_id" : 3, "inventories" : [ 
    { "_id" : 5, "sku" : null, "description" : "Incomplete 5" }, 
    { "_id" : 6 } 
] }


`отобралось, так как "item" == test и "sku" == NULL, то есть нет сопоставления для значения test
вот из-за этой строки видится, что это именно LEFT соединение,
так как если б это был INNER, то именно данная строка бы и отсутствовала в результирующей выборке
но описанная выше "строка" вносит особенность и делает из LEFT - "не совсем LEFT"`

{ "_id" : 4, "item" : "test", "price" : 25, "quantity" : 1, "inventories" : [ ] }


`оторалось, так как "item" == "pecans" и "sku" == "pecans" и "item" == "sku"`

{ "_id" : 5, "item" : "pecans", "price" : 25, "quantity" : 1, "inventories" : [ 
    { "_id" : 4, "sku" : "pecans", "description" : "product 4", "instock" : 70 }, 
    { "_id" : 10, "sku" : "pecans", "description" : "product 7", "instock" : 70 }, 
    { "_id" : 11, "sku" : "pecans", "description" : "product 8", "instock" : 70 } 
] }

`

_Заметка по NULL-значениям в SQL_:

Обещанные примеры на SQL
```postgres-sql
SELECT 
    'x' as a, 
    NULL as nulled, 
    case when ('x' = NULL) then 'TRUE' else 'FALSE' end a__eq__nulled
UNION
SELECT 
    NULL as a, 
    NULL as nulled, 
    case when (NULL = NULL) then 'TRUE' else 'FALSE' end a__eq__nulled
```
Итог NULL не равен ничему, даже самому себе, а в выборке выше указанная строка (*) отобралась именно по этому принципу

a | nulled | a__eq__nulled
_ | _ | ________
'x' | _NULL_ | __FALSE__
_NULL_ | _NULL_ | __FALSE__


```postgres-sql
WITH 
ab AS (
	SELECT a, b 
	FROM 
	(
		SELECT 'a1' as a, 'b1' as b
		UNION
		SELECT 'a2' as a, NULL as b
	) as _ab
),
cd AS (
	SELECT c, d
	FROM 
	(
		SELECT 'c1' as c, NULL as d 
		UNION
		SELECT 'c1' as c, NULL as d 
	) as _cd
)
SELECT ab.a, ab.b, cd.c ,cd.d
FROM ab
LEFT JOIN cd
ON ab.b = cd.d
```

Не хочу форматировать вывод, но поверьте, в выборке будет отсутсвовать ("a2";NULL;"c1";NULL).

## Как сделать INNER 
        
Как в SQL из LEFT соединения получается INNER соединение путем отсечения строки с NULL значением сопоставлемой ячекий, 
так и тут это сделаем отсекая сопоставившееся по NULL, применив `$ne: null`

Повторю, кроме обычных "пустых" соединений, которые как и в SQL у LEFT не соотвествуют никаким строкам в сопоставляемлй таблице

```json
db.orders.aggregate([
    {
        $lookup:
            {
            from: "inventory",
            localField: "item",
            foreignField: "sku",
            as: "inventories"
        }
    },
    {
        $match: { inventories: [] } /* <-- */ 
    }
])
```
вот этим строкам 

```json
{ "_id" : 4, "item" : "test", "price" : 25, "quantity" : 1, "inventories" : [ ] }
```

нужно убрать еще и те "строки", у которых прошло сопоставление по принципу `NULL == NULL`

```json
db.orders.aggregate([
    {
        $lookup:
            {
            from: "inventory",
            localField: "item",
            foreignField: "sku",
            as: "inventories"
        }
    },
    {
        $match: { inventories: { $elemMatch : { sku: null } } } /* <-- */ 
    }
])
```

Вот эти строки нам тоже не нужны, так как не входят в привычное INNER JOIN соединение:

```json
{ "_id" : 3, "inventories" : [ 
  { "_id" : 5, "sku" : null, "description" : "Incomplete 5" }, 
  { "_id" : 6 } 
] }
```

Таким образом итоговый, __"настоящий" INNER запрос будет выглядеть именно так__ (поправьте меня, пожалуйста, если я не прав): 
 
```json
db.orders.aggregate([
    {
        $lookup:
            {
            from: "inventory",
            localField: "item",
            foreignField: "sku",
            as: "inventories"
        }
    },
    {
        $match: { inventories: { $elemMatch : { sku: { $ne:  null } } }} /* <-- */ 
    }
])
```

Выборка 

`
{ "_id" : 1, "item" : "almonds", "price" : 12, "quantity" : 2, "inventories" : [ 
  { "_id" : 1, "sku" : "almonds", "description" : "product 1", "instock" : 120 } 
] }

{ "_id" : 2, "item" : "pecans", "price" : 20, "quantity" : 1, "inventories" : [ 
  { "_id" : 4, "sku" : "pecans", "description" : "product 4", "instock" : 70 }, 
  { "_id" : 10, "sku" : "pecans", "description" : "product 7", "instock" : 70 }, 
  { "_id" : 11, "sku" : "pecans", "description" : "product 8", "instock" : 70 } 
] }

{ "_id" : 5, "item" : "pecans", "price" : 25, "quantity" : 1, "inventories" : [
  { "_id" : 4, "sku" : "pecans", "description" : "product 4", "instock" : 70 }, 
  { "_id" : 10, "sku" : "pecans", "description" : "product 7", "instock" : 70 }, 
  { "_id" : 11, "sku" : "pecans", "description" : "product 8", "instock" : 70 } 
] }
`

## На память

### Выборка по критерию из поддокументов

```json
db.orders.aggregate([
    {
        $lookup:
            {
            from: "inventory",
            localField: "item",
            foreignField: "sku",
            as: "inventories"
        }
    },
    {
        $match: { inventories: { $elemMatch : { sku:  "pecans" } } }
    }
])
```

### Обратный просмотр при выборке
  
когда подзапрос "подсматривает в основной запрос"

 ```
db.orders.aggregate([
    {
        $lookup: {
            from: "inventory",
            let: { orders_item: "$item" },
            pipeline: [
                { 
                    $match: { 
                        $expr: { 
                            $and: [
                                { $eq: [ "$$orders_item",  "$sku" ] }
                            ]
                        }
                    }
                }
           ],
           as: "inventories"
        }
    },
    {
        
        $match: { null: inventories:  {}  }
    }
])
```
