# MongoDB JOIN realization

Для разрешения возникшего с моей стороны непонимания как происходит JOIN выборка в MongoDB

(Официальный документ)[https://docs.mongodb.com/manual/reference/operator/aggregation/lookup/]

## DATA FROM EXAMPLE

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

## LEFT JOIN orders WITH inventory

Да, это действительно LEFT соединение (хотя и реализуется через конструкцию `IN`) , и для его 
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
 `
# отобралось, так как "item" == "almonds" и "sku" == "almonds" и "item" == "sku"
{ "_id" : 1, __"item" : "almonds"__, "price" : 12, "quantity" : 2, "inventories" : [ 
    { "_id" : 1, __"sku" : "almonds"__, "description" : "product 1", "instock" : 120 } 
] }

# отобралось, так как "item" == "pecans" и "sku" == "pecans" и "item" == "sku"
{ "_id" : 2, __"item" : "pecans"__, "price" : 20, "quantity" : 1, "inventories" : [ 
    { "_id" : 4, __"sku" : "pecans"__, "description" : "product 4", "instock" : 70 }, 
    { "_id" : 10, __"sku" : "pecans"__, "description" : "product 7", "instock" : 70 }, 
    { "_id" : 11, __"sku" : "pecans"__, "description" : "product 8", "instock" : 70 } 
] }

# оторалось, __так как__ "item" == NULL и "sku" == NULL и "item" == "sku"
{ "_id" : 3, "inventories" : [ 
    { "_id" : 5, "sku" : null, "description" : "Incomplete 5" }, 
    { "_id" : 6 } 
] }

# оторалось, так как "item" == test и "sku" == NULL и test == NULL (__NULL равен всему__, ведь к нему необходимо применять ISNULL)
{ "_id" : 4, "item" : "test", "price" : 25, "quantity" : 1, "inventories" : [ ] }

# оторалось, так как "item" == "pecans" и "sku" == "pecans" и "item" == "sku"
{ "_id" : 5, "item" : "pecans", "price" : 25, "quantity" : 1, "inventories" : [ 
    { "_id" : 4, "sku" : "pecans", "description" : "product 4", "instock" : 70 }, 
    { "_id" : 10, "sku" : "pecans", "description" : "product 7", "instock" : 70 }, 
    { "_id" : 11, "sku" : "pecans", "description" : "product 8", "instock" : 70 } 
] }

`
 
Если б это был INNER, то именно данная строка бы отсутствовала в выборке
 
 ```json
{ "_id" : 4, "item" : "test", "price" : 25, "quantity" : 1, "inventories" : [ ] }
```

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
Таким образом итоговый, "настоящий" INNER запрос будет выглядеть именно так (поправьте меня, пожалуйста, если я не прав): 
 
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
  
  когда подзапрос "посматривает в основной запрос"

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
